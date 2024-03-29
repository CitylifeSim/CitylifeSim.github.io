
## The CityLife Simluation A High-Fidelity Pedestrian and Vehicle Simulation with Complex Behaviors
This is the official code repository to accompany the paper "CityLifeSim: A High-Fidelity Pedestrian and Vehicle Simulation with Complex Behaviors".
Here we provide python code for generating and running scenarios using the simulation environment as well as links to the datasets and code used for running our experiments

CityLife is a flexible, high-fidelity simulation that allows users to define complex scenarios with essentially unlimited actors, including both pedestrians and vehicles. 
This tool allows each vehicle and pedestrian to operate with basic intelligence that governs the \emph{low-level} controls needed to maneuver, avoiding collisions, navigating corners, stopping at traffic lights, etc. The high-level controls for each agent then allows the user to define behaviors in an abstract form controlling their sequence of actions (e.g., hurry to this intersection, then cross the road, turn left at the park, following that wait for a bus at the stop, etc.), their speed changes in different legs of the journey, their stopping distances, their susceptibility to be influenced by their environment and their risk taking behavior.

[Paper](https://github.com/CitylifeSim/CitylifeSim.github.io/blob/main/CityLifeSim_A_High-Fidelity_Pedestrian_and_Vehicle_Simulation_with_Complex_Behaviors.pdf)
Cheng Yao Wang,  Eyal Ofek, Daniel McDuff, Oron Nir, Sai Vemprala,  Ashish Kapoor,  Mar Gonzalez-Franco (2022)" CityLifeSim: A High-Fidelity Pedestrian and Vehicle Simulation with Complex Behaviors," 2022 IEEE 2nd International Conference on Intelligent Reality (ICIR), Piscataway, NJ, USA, 2022, pp. 11-16, doi: 10.1109/ICIR55739.2022.00018(https://ieeexplore.ieee.org/abstract/document/10070899)

Video
<iframe src="https://drive.google.com/file/d/1HzDDNNBiDJH3pginjnWD6ZoLsC5pzE-l/preview" width="560" height="315" allow="autoplay"></iframe>

### Dataset
The dataset contains videos (RGB, depth, segmentation frames) of six scenarios. There a total of 128 pedestrians in each video. One of the scenarios is captured from 17 different points of view (i.e., cameras) to simulate static view points, the others are captured from cameras on moving autonomous vehicles. 
Here are the download link for each scenario: 

* 17 cameras covering different waypoints and points of interest. [CCTV](https://drive.google.com/file/d/1lZWYIObz4HGp87YTetgoMrbIn-jfflgW/view?usp=sharing)
* the front camera on a car during sunny weather. [car_sunny](https://drive.google.com/file/d/1MakOLo3e2XHk3hDgmuIZDAl5dwpQYSeo/view?usp=sharing)
* the front camera on a car during rainy weather. [car_weather](https://drive.google.com/file/d/1KtDhfqQaPbNx4BcbdCLG5DKuc0Uf0361/view?usp=sharing)
* the front cameras on a car during snowy weather. [car_snowy](https://drive.google.com/file/d/1by29iSKW6X943yHjvJVFepo2JDp7Ep42/view?usp=sharing)
* the front camera on a drone.[drone_front](https://drive.google.com/file/d/19fVTnfQiY-_YHoBQR7-qbsyrSLnPJZK3/view?usp=sharing)
* a camera pointing down from a drone. [drone_downward](https://drive.google.com/file/d/1S7sFj7MWWvWAP_B-pgRmoVxcqtoI1j4I/view?usp=sharing)


## CityLifeSim Download
You can download the CityLifeSim executable [here](https://1drv.ms/u/s!AsGKWIA1OsCvpVjc4_8OckZMVUKN?e=9Lum0t)


## Generate Your Own Pedestrians Scenarios:
* [code/generate_scenario.py](https://github.com/CitylifeSim/CitylifeSim.github.io/blob/main/code/generate_scenario.py) provides an example of how to programmatically create scenarios. (TRAVERSE_TYPE: random, a_star)
```bash
$ python generate_scenario.py --traverse_type <TRAVERSE_TYPE> --out_file <SCENARIO_FILE_NAME>.csv
```
* [CityLife_randomwalk_128_v6.csv](https://github.com/CitylifeSim/CitylifeSim.github.io/blob/main/code/CityLife_randomwalk_128_v6.csv) shows an example of the CSV output that is generated.

## Run the CityLifeSim
* Set up CityLifeSim python client environment
  * Install Anaconda and Open Anaconda Prompt
  * Create the conda env for CityLifeSim
   ```bash
   conda env create -f \CityLife_v1\citylifesim.yml
   conda activate citylifesim
  ```
* CityLifeSim python client currently runs on **AirSim 1.5.0 verion**. Newer version won't work due to the syntx change for some AirSim API.

* Run the CityEnv.exe
  * Please check [AirSim guide](https://microsoft.github.io/AirSim/settings/) on how to move around in the enviroment in different modes(ComputerVision, Car, Multirotor)
  * Modify the settings.json in Documents\AirSim based on your needs. (Use ComputerVision mode in the setting.json for cctv mode)
  * **ComputerVision** mode in the setting.json for testing cctv camera mode, **Car** mode in the setting.json for car camera mode, **Multirotor** mode in the setting for drome cam mode 

* Prepare pedestrians scenarios
  * Put the scenario csv file in the \CityLifeSim\WindowsNoEditor\CityEnv\Saved folder

* Run the pedestrian scenarios simluation (CAM_MODE: cctv, car, drone)
 ```bash
  $ python run_scenario.py --ped_scenario <SCENARIO_FILE_NAME> --cam_mode <CAM_MODE> --recording
 ```
 * You can add --car_scenario <SCENARIO_FILE_NAME> to run the car scenario at the same time. We currently provide Scenario_[1-100] for testing. 
 * Please check the [CausalCity](https://github.com/CitylifeSim/causalcity.github.io) for generating car scenarios.
 * The recorded RBB-D images folder is by default present in the Documents folder (or specified in settings) with the timestamp of when the recording started in %Y-%M-%D-%H-%M-%S format.

## Controlling Environment
  * Environmental variables (e.g weather, Timne of Day) that can act as confounders in a dataset can be controlled using the AirSim APIs. Please check [AirSim Documentation](https://microsoft.github.io/AirSim/apis/)
  * [code/control_trafficlight.py](https://github.com/CitylifeSim/CitylifeSim.github.io/blob/main/code/control_trafficlight.py) provides an example of how to programmatically control the traffic lights to override the default one.

## Generating Bouding Boxes from Segmentation Images
 * To generate bounding boxes:
 ```bash
  $ python seg2bbox.py --folder <RGB-D FOLDER> --seg_rgbs <FILE_PATH> --save_image
 ```
 * Read the peds_bbox.json and plot the bboxes
 ```bash
  $ python vis_bbox.py --folder <RGB-D FOLDER> --image_id <RGB_IMAGE_ID>
 ``` 

## Multi-object Tracking (MOT) using ByteTrack and MOTChallenge evaluation
The following Colab downloads CityLifeSim into your drive, applies a SoTA MOT and evaluate it. 
We leverage the work of (Zhang et al., 2021).
For more details please refer to the paper or dive into the code...


## Contributors
Cheng Yao Wang,  Eyal Ofek, Daniel McDuff, Oron Nir, Sai Vemprala,  Ashish Kapoor,  Mar Gonzalez-Franco 
Microsoft Research
