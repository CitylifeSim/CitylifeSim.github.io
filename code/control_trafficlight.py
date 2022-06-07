#########################################################################################
# Testing script to change traffic lights and weathers
#########################################################################################

import sys
import setup_path
import airsim
import logging
import numpy as np
import asyncio
import time
import os 
import datetime
import math


LIGHT_DURATION = 15
TURN_LIGHT_DURATION = LIGHT_DURATION // 2
YELLOW_DURATION = 4

# Set up car client:
c = airsim.client.CarClient()
c.simEnableWeather(True)
# disable the default traffic light control 
c.simRunConsoleCommand('ce ToggleTrafiicLights ')


async def main():
  
  future = asyncio.ensure_future(LoopTrafficLightsOriginal())
  #Uncomment for running the peds sceneraio
  await WeatherControl()
  await asyncio.sleep(600)


async def LoopTrafficLightsOriginal():
  global LIGHT_DURATION, TURN_LIGHT_DURATION, YELLOW_DURATION
  EastBoundStopsLeft = set(['A0y', 'A1y', 'B0y', 'B1y'])
  EastBoundStopsRight = set(['A0z', 'A1z', 'B0z', 'B1z'])
  WestBoundStopsRight = set(['A1w', 'A2w', 'B1w', 'B2w'])
  WestBoundStopsLeft = set(['A1x', 'A2x', 'B1x', 'B2x'])
  NorthBoundStopsLeft = set(['C1y', 'C2y', 'D1y', 'D2y'])
  NorthBoundStopsRight = set(['C1z', 'C2z', 'D1z', 'D2z'])
  SouthBoundStopsRight = set(['C0w', 'C1w', 'D0w', 'D1w'])
  SouthBoundStopsLeft = set(['C0x', 'C1x', 'D0x', 'D1x'])
  
  EastBoundStops = EastBoundStopsLeft.union(EastBoundStopsRight)
  WestBoundStops = WestBoundStopsLeft.union(WestBoundStopsRight)
  NorthBoundStops = NorthBoundStopsLeft.union(NorthBoundStopsRight)
  SouthBoundStops = SouthBoundStopsLeft.union(SouthBoundStopsRight)

  EW = EastBoundStops.union(WestBoundStops)
  NS = NorthBoundStops.union(SouthBoundStops)

  while True:
    #east/west lights green; north/south lights red.
    SetLights(EW, 'Straight', 'Green')
    #SetLights(EW, 'Left', 'Green')
    SetLights(NS, 'Straight', 'Red')
    await asyncio.sleep(LIGHT_DURATION)
    
    #east/west goes yellow, then red.
    SetLights(EW, 'Straight', 'Yellow')
    SetLights(EW, 'Left', 'Yellow')
    await asyncio.sleep(YELLOW_DURATION)
    SetLights(EW, 'Straight', 'Red')
    SetLights(EW, 'Left', 'Red')
    
    #NSTURNS: north/south left turns activate for a short time, then go yellow, then red.
    SetLights(NS, 'Left', 'Green')
    await asyncio.sleep(TURN_LIGHT_DURATION)
    SetLights(NS, 'Left', 'Yellow')
    await asyncio.sleep(YELLOW_DURATION)
    SetLights(NS, 'Left', 'Red')
    
    #north/south green.
    SetLights(NS, 'Straight', 'Green')
    #SetLights(NS, 'Left', 'Green')
    await asyncio.sleep(LIGHT_DURATION)
    
    #Turn north/south yellow, then red.
    SetLights(NS, 'Straight', 'Yellow')
    SetLights(NS, 'Left', 'Yellow')
    await asyncio.sleep(YELLOW_DURATION)  
    SetLights(NS, 'Straight', 'Red')
    SetLights(NS, 'Left', 'Red')
    
    #EWTURNS: east/west left turns activate for a short time, then go yellow, then red.
    SetLights(EW, 'Left', 'Green')
    await asyncio.sleep(TURN_LIGHT_DURATION)
    SetLights(EW, 'Left', 'Yellow')
    await asyncio.sleep(YELLOW_DURATION)
    SetLights(EW, 'Left', 'Red')
    
  
def SetLights(startingLanes, direction, color):
  global c #airsim client
  for lane in startingLanes:
    c.simRunConsoleCommand('ce SetLightState ' + lane + ' ' + direction + ' ' + color)


async def WeatherControl():
  weather_idx = 0
  weather_duration = 10
  t_end = time.time() + weather_duration
  while True:
    if time.time() > t_end:
      if weather_idx % 3== 0:
        print("weather_rain")
        c.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.0);
        c.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.5);
      
      elif weather_idx % 3 == 1:
        print("weather_snow")
        c.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.0);
        c.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.5);
        
      elif weather_idx % 3 == 2:
        c.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.0);
        c.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.0);

      weather_idx += 1
      t_end = time.time() + weather_duration
      await asyncio.sleep(0.01)  


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())