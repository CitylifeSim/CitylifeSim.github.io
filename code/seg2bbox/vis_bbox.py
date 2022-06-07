import os
import numpy as np
import torch
import torchvision
import csv
import cv2
import json
import ast
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F
from natsort import os_sorted
import argparse
from PIL import Image
from torchvision.io import read_image
from torchvision.ops import masks_to_boxes
from torchvision.utils import draw_bounding_boxes

plt.rcParams["savefig.bbox"] = "tight"

def show(imgs):
	if not isinstance(imgs, list):
		imgs = [imgs]
	fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
	for i, img in enumerate(imgs):
		img = img.detach()
		img = F.to_pil_image(img)
		axs[0, i].imshow(np.asarray(img))
		axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Visualize bbox')
	parser.add_argument('--folder', type=str, default='')
	parser.add_argument('--image_id', type=int, default=0)

	args = parser.parse_args()
	
	datasetDir = args.folder
	imageDir = os.path.join(datasetDir, 'rgb')
	segDir = os.path.join(datasetDir, 'seg')

	imgs_list = os_sorted(os.listdir(imageDir))
	masks_list = os_sorted(os.listdir(segDir))

	peds_bbox_path = os.path.join(datasetDir, "peds_bbox.json")
	with open(peds_bbox_path) as json_data:
		peds_bbox = json.load(json_data)

	#nanosec as id
	image_id = args.image_id

	target_id = 0;
	for idx, img_name in enumerate(imgs_list):
		if str(image_id) in img_name:
			target_id = idx
			break

	timestamp =  int(os.path.splitext(masks_list[target_id])[0].split("_")[3])
	print(timestamp)

	img_cam_id = int(os.path.splitext(imgs_list[target_id])[0].split("_")[1])
	img_frame_id = int(os.path.splitext(imgs_list[target_id])[0].split("_")[2])

	for i in range(len(peds_bbox)):
		if int(peds_bbox[i]['frame_id']) == timestamp:
			print ("test")
			img_name = "rgb_"+str(img_cam_id)+"_"+str(img_frame_id)+"_"+ str(image_id) + ".png"
			img_path = os.path.join(imageDir, img_name)
			img = read_image(img_path, mode=torchvision.io.image.ImageReadMode.RGB)
			print(img_name)
			boxes =  torch.empty(len(peds_bbox[i]["ped_bboxes"]), 4, dtype=torch.long)
			print(peds_bbox[i]["ped_bboxes"])
			for idx, ped in enumerate(peds_bbox[i]["ped_bboxes"]):
				box_np = np.array(ped["bbox"])
				boxes[idx] = torch.from_numpy(box_np)
			drawn_boxes = draw_bounding_boxes(img, boxes, colors="red")
			break	

	show(drawn_boxes)
	plt.show()
