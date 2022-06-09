#########################################################################################
# Testing script to record pedestrians 3D locations and pixel locations 
#########################################################################################

import sys
import setup_path
import argparse
import airsim
import logging
import numpy as np
import pandas as pd
import asyncio
import os
import time
import datetime
import math


## LOGGING:
NPEDS = 128  # TBD
NATTRIBUTES = 8  # x, y, z, x_pixel, y_pixel, roll, pitch, yaw
peds = ["PedestrianBase_" + str(i) for i in range(NPEDS)] # List of all ped names
ped_list_names = ["Ped_" + str(i) for i in range(NPEDS)]                      
ped_list = [ped_name for ped_name in ped_list_names for i in range(NATTRIBUTES)] # Repeated list to match list of attributes
attributes = ["x", "y", "z", "x_pixel", "y_pixel", "pitch", "roll", "yaw"]                    # What we want to log
attributes_all_peds = attributes * NPEDS

NCAMS = 18
cams = ["PedsCamera" + str(i) for i in range(1, NCAMS)] # List of all ped names
cams[0] = "PedsCamera_4" #Unreal generate this ID name for the first cam
NFRAME = 20

saveDir = os.path.join(os.path.dirname(__file__), "RGBD_"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
isRecording = False
useAirSimRecord = True

def RunScenarios(pedScenario, carScenario=""):

	## Run a scenario:
	print("ped scenario: ", pedScenario)
	c.simRunConsoleCommand('ce LoadPedsCSV ' + pedScenario)

	 ## Run a scenario:
	if carScenario is not "":
		print("car scenario: ", pedScenario)
		c.simRunConsoleCommand('ce RunScenario ' + carScenario)


def DroneControl(c, duration=20):
	z = -4
	waypoints = [(-3 , -29, z), (30 , -30, z), (30 , -3, z),(0 , 0, z)] 

	print("arming the drone...")
	c.armDisarm(True)

	state = c.getMultirotorState()
	if state.landed_state == airsim.LandedState.Landed:
		print("taking off...")
		c.takeoffAsync().join()
	else:
		c.hoverAsync().join()

	time.sleep(1)

	state = c.getMultirotorState()
	if state.landed_state == airsim.LandedState.Landed:
		print("take off failed...")
		sys.exit(1)

	# AirSim uses NED coordinates so negative axis is up.
	# z of -4 is 4 meters above the original launch point.
	print("make sure we are hovering at 4+ meters...")
	c.moveToZAsync(z, 1).join()

	cam_idx = 0
	wp_idx = 0
	if isRecording and useAirSimRecord:
		c.startRecording()
	while wp_idx < len(waypoints):
		ind = 0
		t_end = time.time() + duration
		result = c.moveToPositionAsync(waypoints[wp_idx][0] , waypoints[wp_idx][1], z , 3, 120, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), 20, 1).join()
		while time.time() < t_end:
			if isRecording and not useAirSimRecord:
				SaveRGBD("0", ind) # "0": front_center camera, # "3": downward camera
				ind += 1
		wp_idx += 1
	if isRecording and useAirSimRecord:
		c.stopRecording()


def CCTVCameraControl(c, duration=15):
	cam_idx = 0
	if isRecording and useAirSimRecord:
		c.startRecording()
	while cam_idx < len(cams):
		ind = 0
		t_end = time.time() + duration
		came_pose = c.simGetObjectPose(cams[cam_idx])
		c.simSetCameraPose(0, came_pose)
		while time.time() < t_end:
			if isRecording and not useAirSimRecord:			
				SaveRGBD("0", ind) # "0": default camera
				ind += 1
		cam_idx += 1
	if isRecording and useAirSimRecord:
		c.stopRecording()

# ComputerVision or Car mode
def UserControl(c, duration=15):
	cam_idx = 0
	ind = 0
	t_end = time.time() + duration
	if isRecording and useAirSimRecord:
		c.startRecording()
	while time.time() < t_end:
		if isRecording and not useAirSimRecord:
			SaveRGBD("0", ind)
			ind += 1
	if isRecording and useAirSimRecord:
		c.stopRecording()


def write_pfm(file, image, scale=1):
	""" Write a pfm file """
	file = open(file, 'wb')

	color = None

	if image.dtype.name != 'float32':
		raise Exception('Image dtype must be float32.')

	if len(image.shape) == 3 and image.shape[2] == 3: # color image
		color = True
	elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1: # grayscale
		color = False
	else:
		raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

	file.write('PF\n'.encode('utf-8')  if color else 'Pf\n'.encode('utf-8'))
	temp_str = '%d %d\n' % (image.shape[1], image.shape[0])
	file.write(temp_str.encode('utf-8'))

	endian = image.dtype.byteorder

	if endian == '<' or endian == '=' and sys.byteorder == 'little':
		scale = -scale

	temp_str = '%f\n' % scale
	file.write(temp_str.encode('utf-8'))

	image.tofile(file)

#TODO- fix issue: Function 'simGetImages' was called with an invalid number of arguments. Expected: 3, got: 2. Might be AirSim version issue.
def SaveRGBD(cam_id, ind):
	if not isRecording:
		return

	timestamp = time.time_ns()
	rgbSaveDir = os.path.join(saveDir, 'rgb')
	segSaveDir = os.path.join(saveDir, 'seg')
	depthSaveDir = os.path.join(saveDir, 'depth')

	# GET images:
	segResponse = c.simGetImages([airsim.ImageRequest(cam_id, airsim.ImageType.Scene, False, False),
		airsim.ImageRequest(cam_id, airsim.ImageType.Segmentation, False, False),
		airsim.ImageRequest(cam_id, airsim.ImageType.DepthPerspective, True, False)])


	rgb = np.fromstring(segResponse[0].image_data_uint8, dtype=np.uint8) #get numpy array
	img_rgb = rgb.reshape(segResponse[0].height, segResponse[0].width, 3) #reshape array to 3 channel image array H X W X 3
	rgbFilename = "rgb_frame_" + str(cam_id) + "_" + str(ind) + "_" + timestamp + ".png"
	rgb = Image.fromarray(img_rgb)
	rgb.save(os.path.join(rgbSaveDir, rgbFilename))

	seg = np.fromstring(segResponse[1].image_data_uint8, dtype=np.uint8) #get numpy array
	img_seg = seg.reshape(segResponse[1].height, segResponse[1].width, 3) #reshape array to 3 channel image array H X W X 3
	segFilename = "seg_frame_" + str(cam_id) + "_" + str(ind) +  "_" + timestamp + ".png"
	seg = Image.fromarray(img_seg)
	seg.save(os.path.join(segSaveDir, segFilename))

	depthFilename = "depth_frame_"+ str(cam_id) + "_" + str(ind) + "_" + timestamp + ".png"
	depth_img_in_meters = airsim.list_to_2d_float_array(segResponse[2].image_data_float, segResponse[2].width, segResponse[2].height)
	write_pfm(os.path.join(depthSaveDir, depthFilename), depth_img_in_meters)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--ped_scenario', type=str, default='CityLife_randomwalk_128_v6')
	parser.add_argument('--car_scenario', type=str, default='')
	parser.add_argument('--cam_mode', type=str, default='user') #mode: cctv, drone, user
	parser.add_argument('--recording', default=False, action='store_true')
	parser.add_argument('--no-recording', dest='recording', action='store_false')
	
	args = parser.parse_args()


	# Set up car client:
	if args.cam_mode == "drone":
		c = airsim.MultirotorClient()
	else:
		c = airsim.client.CarClient()
	
	c.confirmConnection()
	#c.enableApiControl(True)

	## Define weather/road wetness and correlate with the scenario:
	c.simEnableWeather(True)

	##Ucomment below for futher environment control
	#c.simSetWeatherParameter(airsim.WeatherParameter.Rain, 1.0);
	#c.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.25);
	#c.simSetTimeOfDay(True, '17-33-31', False, 1, 60, True)

	RunScenarios(args.ped_scenario, args.car_scenario)

	## Set the segmentation color
	found = c.simSetSegmentationObjectID("[\w]*", 0, True)
	# Loop through peds and get IDs:
	for i in range(NPEDS):
		success = c.simSetSegmentationObjectID(peds[i], i+1, True)

	isRecording = args.recording
	if isRecording and not useAirSimRecord:
		if not os.path.exists(saveDir):
			os.makedirs(saveDir)
			rgbSaveDir = os.path.join(saveDir, 'rgb')
			os.mkdir(rgbSaveDir)
			depthSaveDir = os.path.join(saveDir, 'depth')
			os.mkdir(depthSaveDir)
			segSaveDir = os.path.join(saveDir, 'seg')
			os.mkdir(segSaveDir)

	if(args.cam_mode == "drone"):
		c.enableApiControl(True)
		DroneControl(c)
	elif(args.cam_mode == "cctv"):
		CCTVCameraControl(c)
	else:
		UserControl(c)