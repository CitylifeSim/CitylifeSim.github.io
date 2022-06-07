import pandas as pd
import random
import argparse
import map


def init_POIs():
	crosswalk_corners = ["TL_TR", "TR_TL", "TL_BL", "BL_TL", "TR_BR", "BR_TR", "BL_BR", "BR_BL"]
	blockers_prefix = ["AC_POIBlocker", "AD_POIBlocker", "BC_POIBlocker", "BD_POIBlocker"]
	POI_blockers = dict()
	for prefix in blockers_prefix:
		for corner in crosswalk_corners:
			POI_blockers[prefix+corner] = 1.0

	#print(POI_blockers)

	#POIAttractor1 - bench
	#POIAttractorQueue2 - Forming the line at bus stop
	#POIAttractor2 - Forming crowd around a street dance
	POI_Attractors = dict()
	POI_Attractors["POIAttractor1"] = 1.0
	POI_Attractors["POIAttractor2"] = 1.0
	POI_Attractors["POIAttractorQueue2"] = 1.0

	#POIRepellor1 -  Move away from a person who is angry on the phone
	POI_Repellors = dict()
	POI_Repellors["POIRepellor1"] = 1.0

	all_POIs = dict()
	all_POIs["blockers"] = POI_blockers
	all_POIs["attractors"] = POI_Attractors
	all_POIs["Repellors"] = POI_Repellors

	#print (all_POIs["blockers"])
	return all_POIs

def get_avatars():
	rocketbox_avatars = []
	rocketbox_avatars_female = []
	rocketbox_avatars_male = []
	for i in range (1, 18):
	  rocketbox_avatars_female.append("Female_Adult_"+ str(i).zfill(2))

	for i in range (1, 3):
	  rocketbox_avatars_female.append("Female_Party_"+ str(i).zfill(2))

	#for i in range (1, 3):
	#  rocketbox_avatars_female.append("Female_Child_"+ str(i).zfill(2))

	for i in range (1, 5):
	  rocketbox_avatars_female.append("Business_Female_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_female.append("Chef_Female_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_female.append("Construction_Female_"+ str(i).zfill(2))

	for i in range (1, 4):
	  rocketbox_avatars_female.append("Fire_Female_"+ str(i).zfill(2))

	for i in range (1, 4):
	  rocketbox_avatars_female.append("Medical_Female_"+ str(i).zfill(2))

	for i in range (1, 3):
	  rocketbox_avatars_female.append("Military_Female_"+ str(i).zfill(2))

	for i in range (1, 3):
	  rocketbox_avatars_female.append("Pilot_Female_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_female.append("Police_Female_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_female.append("Security_Female_"+ str(i).zfill(2))

	for i in range (1, 3):
	  rocketbox_avatars_female.append("Sports_Female_"+ str(i).zfill(2))



	for i in range (1, 22):
	  rocketbox_avatars_male.append("Male_Adult_"+ str(i).zfill(2))

	#for i in range (1, 3):
	#  rocketbox_avatars_male.append("Male_Child_"+ str(i).zfill(2))

	for i in range (1, 8):
	  rocketbox_avatars_male.append("Business_Male_"+ str(i).zfill(2))

	for i in range (1, 9):
	  rocketbox_avatars_male.append("Construction_Male_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_male.append("Delivery_Male_"+ str(i).zfill(2))

	for i in range (1, 8):
	  rocketbox_avatars_male.append("Fire_Male_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_male.append("Gardener_Male_"+ str(i).zfill(2))

	for i in range (1, 6):
	  rocketbox_avatars_male.append("Medical_Male_"+ str(i).zfill(2))

	for i in range (1, 7):
	  rocketbox_avatars_male.append("Military_Male_"+ str(i).zfill(2))

	for i in range (1, 4):
	  rocketbox_avatars_male.append("Pilot_Male_"+ str(i).zfill(2))

	for i in range (1, 8):
	  rocketbox_avatars_male.append("Police_Male_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_male.append("Security_Male_"+ str(i).zfill(2))

	for i in range (1, 5):
	  rocketbox_avatars_male.append("Sports_Male_"+ str(i).zfill(2))

	for i in range (1, 2):
	  rocketbox_avatars_male.append("Wood_Male_"+ str(i).zfill(2))

	rocketbox_avatars = rocketbox_avatars_female + rocketbox_avatars_male

	avatar_exclude_list = ["Female_Adult_06", "Female_Adult_10", "Female_Adult_16", "Male_Adult_15", "Male_Adult_19",
	"Male_Adult_21", "Female_Party_01", "Fire_Female_01", "Fire_Female_02", "Fire_Female_03", "Fire_Male_01",
	"Fire_Male_04", "Fire_Male_05", "Fire_Male_06", "Fire_Male_07", "Military_Male_01", "Military_Male_03","Military_Male_04",
	"Military_Male_05", "Military_Male_06", "Military_Female_01", "Military_Female_02", "Police_Female_01", "Police_Male_02",
	"Police_Male_04", "Police_Male_05", "Police_Male_06", "Pilot_Male_01", "Pilot_Male_02", "Pilot_Male_03", "Pilot_Female_01", 
	"Sports_Male_01", "Sports_Female_01", "Chef_Female_01", "Construction_Male_01", "Construction_Male_03","Construction_Male_04",
	"Construction_Male_06", "Medical_Male_04","Medical_Male_05"]

	for avatar in rocketbox_avatars:
		if avatar in avatar_exclude_list:
			rocketbox_avatars.remove(avatar)

	print("all: " + str(len(rocketbox_avatars)) +" female: " + str(len(rocketbox_avatars_female)) + " male:"+ str(len(rocketbox_avatars_male)))

	return rocketbox_avatars

def init_map():
	# For better demo, don't connect to the end point in each road
	_map = map.Map()

	#map.add_edge('A0_top', 'AC_topleft', 1)
	_map.add_edge('AC_topleft', 'AC_topright', 1)
	_map.add_edge('AC_topright', 'A1_top', 1)
	_map.add_edge('A1_top', 'AD_topleft', 1)
	_map.add_edge('AD_topleft', 'AD_topright', 1)
	#_map.add_edge('AD_topright', 'A2_left', 1)

	#_map.add_edge('A0_bottom', 'AC_bottomleft', 1)
	_map.add_edge('AC_bottomleft', 'AC_bottomright', 1)
	_map.add_edge('AC_bottomright', 'A1_bottom', 1)
	_map.add_edge('A1_bottom', 'AD_bottomleft', 1)
	_map.add_edge('AD_bottomleft', 'AD_bottomright', 1)
	#_map.add_edge('AD_bottomright', 'A2_right', 1)

	#_map.add_edge('B0_top', 'BC_topleft', 1)
	_map.add_edge('BC_topleft', 'BC_topright', 1)
	_map.add_edge('BC_topright', 'B1_top', 1)
	_map.add_edge('B1_top', 'BD_topleft', 1)
	_map.add_edge('BD_topleft', 'BD_topright', 1)
	#_map.add_edge('BD_topright', 'B2_top', 1)

	#_map.add_edge('B0_bottom', 'BC_bottomleft', 1)
	_map.add_edge('BC_bottomleft', 'BC_bottomright', 1)
	_map.add_edge('BC_bottomright', 'B1_bottom', 1)
	_map.add_edge('B1_bottom', 'BD_bottomleft', 1)
	_map.add_edge('BD_bottomleft', 'BD_bottomright', 1)
	#_map.add_edge('BD_bottomright', 'B2_bottom', 1)

	#_map.add_edge('C0_left', 'AC_topleft', 1)
	_map.add_edge('AC_topleft', 'AC_bottomleft', 1)
	_map.add_edge('AC_bottomleft', 'C1_left', 1)
	_map.add_edge('C1_left', 'BC_topleft', 1)
	_map.add_edge('BC_topleft', 'BC_bottomleft', 1)
	#_map.add_edge('BC_bottomleft', 'C2_left', 1)

	#_map.add_edge('C0_right', 'AC_topright', 1)
	_map.add_edge('AC_topright', 'AC_bottomright', 1)
	_map.add_edge('AC_bottomright', 'C1_right', 1)
	_map.add_edge('C1_right', 'BC_topright', 1)
	_map.add_edge('BC_topright', 'BC_bottomright', 1)
	#_map.add_edge('BC_bottomright', 'C2_right', 1)

	#_map.add_edge('D0_left', 'AD_topleft', 1)
	_map.add_edge('AD_topleft', 'AD_bottomleft', 1)
	_map.add_edge('AD_bottomleft', 'D1_left', 1)
	_map.add_edge('D1_left', 'BD_topleft', 1)
	_map.add_edge('BD_topleft', 'BD_bottomleft', 1)
	#_map.add_edge('BD_bottomleft', 'D2_left', 1)

	#_map.add_edge('D0_right', 'AD_topright', 1)
	_map.add_edge('AD_topright', 'AD_bottomright', 1)
	_map.add_edge('AD_bottomright', 'D1_right', 1)
	_map.add_edge('D1_right', 'BD_topright', 1)
	_map.add_edge('BD_topright', 'BD_bottomright', 1)
	#_map.add_edge('BD_bottomright', 'D2_right', 1)

	return _map


def random_traverse_sp(wp_map, spawn_wps=[], num_peds_sp=8, num_dest=20):
	all_waypoints = wp_map.get_all_nodes()
	all_peds = []
	waypoints = []

	#default randomly select 10 spawn points
	if len(spawn_wps) == 0:
		for i in range(10):
			spawn_idx = random.randrange(0, len(all_waypoints)-1)
			spawn_wps.append(all_waypoints[spawn_idx])

	for idx, sp in enumerate(spawn_wps):
		for i in range(num_peds_sp):
			ped_idx = i + idx*num_peds_sp
			ped_data = dict()
			ped_data["Key"] = "Ped_" + str(ped_idx)
			ped_data["Id"] = "Ped_" + str(ped_idx)
			ped_data["Spawn"] = sp
			ped_data["SpawnRadius"] = 250

			waypoints = wp_map.random_traverse(sp, num_dest)
			waypoints_str = ",".join(waypoints[1:])
			ped_data["Waypoints"] = waypoints_str

			ped_data["WalkSpeed"] =random.randrange(100, 180)

			#AppearanceIdx all: 115 female: 41 male:74 
			avatar_idx = random.randint(0, len(rocketbox_avatars)-1)
			
			if "Male" in rocketbox_avatars[avatar_idx]:
			  AnimType = "Male"
			elif "Female" in rocketbox_avatars[avatar_idx]:
			  AnimType = "Female"
			else:
			  AnimType = "Male"
			
			ped_data["AnimType"] = AnimType

			POITypes = []
			POIProbs = []
			for key in all_POIs["blockers"].keys():
			  POITypes.append(key)
			  POIProbs.append(1.0)
			for key in all_POIs["attractors"].keys():
			  POITypes.append(key)
			  POIProbs.append(random.uniform(0.5, 1.0)) # make it larger chance
			for key in all_POIs["Repellors"].keys():
			  POITypes.append(key)
			  POIProbs.append(1.0)

			POITypes_str = ",".join(POITypes)
			POIProbs_str = ",".join([str(i) for i in POIProbs])
			ped_data["POITypes"] = POITypes_str
			ped_data["POIProbs"] = POIProbs_str

			ped_data["AppearanceIdx"] = rocketbox_avatars[avatar_idx]

			all_peds.append(ped_data)

	return all_peds

def a_star_traverse(wp_map, path_lists, num_peds = 80):
	all_waypoints = wp_map.get_all_nodes()

	all_peds = []
	for i in range(num_peds):
		#path_idx = random.randint(0, len(path_lists)-1)
		path_idx = i % len(path_lists)
		ped_data = dict()
		ped_data["Key"] = "Ped_" + str(i)
		ped_data["Id"] = "Ped_" + str(i)
		ped_data["Spawn"] = path_lists[path_idx][0]
		ped_data["SpawnRadius"] = 250
		
		#debug
		if not path_lists[path_idx][0] in all_waypoints:
			print(path_lists[path_idx][0])
		if not path_lists[path_idx][1] in all_waypoints:
			print(path_lists[path_idx][1])


		waypoints =  wp_map.find_path_a_star(path_lists[path_idx][0], path_lists[path_idx][1])
		print(path_idx)
		waypoints_str = ",".join(waypoints[1:])
		ped_data["Waypoints"] = waypoints_str

		ped_data["WalkSpeed"] =random.randrange(100, 155)

		#AppearanceIdx all: 115 female: 41 male:74 
		avatar_idx = random.randint(0, len(rocketbox_avatars)-1)
	  

		if "Male" in rocketbox_avatars[avatar_idx]:
			AnimType = "Male"
		elif "Female" in rocketbox_avatars[avatar_idx]:
			AnimType = "Female"
		else:
			AnimType = "Male"

		ped_data["AnimType"] = AnimType

		POITypes = []
		POIProbs = []
		for key in all_POIs["blockers"].keys():
			  POITypes.append(key)
			  POIProbs.append(1.0)
		for key in all_POIs["attractors"].keys():
			POITypes.append(key)
			POIProbs.append(random.uniform(0.5, 1.0)) # make it larger chance
		for key in all_POIs["Repellors"].keys():
			POITypes.append(key)
			POIProbs.append(1.0)

		POITypes_str = ",".join(POITypes)
		POIProbs_str = ",".join([str(i) for i in POIProbs])
		ped_data["POITypes"] = POITypes_str
		ped_data["POIProbs"] = POIProbs_str
		ped_data["AppearanceIdx"] = rocketbox_avatars[avatar_idx]

		all_peds.append(ped_data)
	return all_peds


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Visualize bbox')
	parser.add_argument('--traverse_type', type=str, default='random') # random or a_star
	parser.add_argument('--out_file', type=str, default="cityLife_paths.csv")

	args = parser.parse_args()

	all_POIs = init_POIs()
	rocketbox_avatars = get_avatars()
	wp_map = init_map()
	# print(wp_map.graph['AC_bottomleft'])
	# print(wp_map.get_all_nodes())
	# print(wp_map.get_neighbor_random("AC_topright"))
	# print(wp_map.find_path_a_star("AC_topleft", "BD_topright"))

	wp_map.init_heuristic_func()
	wp_map.random_traverse("AC_topright", 5)

	if args.traverse_type == "random":

		spwan_wps = ["BC_topleft", "BC_topright", "BC_bottomleft", "BC_bottomright", "B1_top", "B1_bottom", "BD_topleft", "BD_bottomleft",
								"C1_left", "C1_right", "AC_bottomleft", "AC_bottomright", "AC_topleft", "AC_topright", "A1_top", "A1_bottom"]

		all_peds = random_traverse_sp(wp_map, spwan_wps)
		#print(len(all_peds))
	else:

		# (start_node, end_node)
		path_lists = [("BC_topleft", "AD_bottomright"), ("BC_topleft", "D1_right"), 
				   ("BC_topleft", "A1_top"), ("BC_topleft", "BD_topright"),
				  ("BC_topright", "AC_topleft"), ("BC_topright", "D1_right"), 
				   ("BC_topright", "AC_topleft"), ("BC_topright", "BD_bottomright"),
				  ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "D1_right"), 
				   ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "BD_bottomright"),
				   ("BC_bottomright", "AC_topleft"), ("BC_bottomright", "AD_topleft"), 
				   ("BC_bottomright", "D1_right"), ("BC_bottomright", "AC_topleft"),
				  ("BC_topleft", "AD_bottomright"), ("BC_topleft", "D1_right"), 
				   ("BC_topleft", "A1_top"), ("BC_topleft", "BD_topright"),
				  ("BC_topright", "AC_topleft"), ("BC_topright", "D1_right"), 
				   ("BC_topright", "AC_topleft"), ("BC_topright", "BD_bottomright"),
				  ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "D1_right"), 
				   ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "BD_bottomright"),
				   ("BC_bottomright", "AC_topleft"), ("BC_bottomright", "AD_topleft"), 
				   ("BC_bottomright", "D1_right"), ("BC_bottomright", "AC_topleft"),
				  ("BC_topleft", "AD_bottomright"), ("BC_topleft", "D1_right"), 
				   ("BC_topleft", "A1_top"), ("BC_topleft", "BD_topright"),
				  ("BC_topright", "AC_topleft"), ("BC_topright", "D1_right"), 
				   ("BC_topright", "AC_topleft"), ("BC_topright", "BD_bottomright"),
				  ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "D1_right"), 
				   ("BC_bottomleft", "AC_topleft"), ("BC_bottomleft", "BD_bottomright"),
				   ("BC_bottomright", "AC_topleft"), ("BC_bottomright", "AD_topleft"), 
				   ("BC_bottomright", "D1_right"), ("BC_bottomright", "AC_topleft")]

		all_peds = a_star_traverse(wp_map, path_lists)
		#print(len(all_peds))


	df = pd.DataFrame(all_peds)
	#print(df)
	df.to_csv(args.out_file, encoding='utf-8', index=False)