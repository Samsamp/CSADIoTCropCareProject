# This script gets all input data from the planters sensors, including the reservoir water level sensor. At present we are using
# Catnip Electronics i2c Soil Moisture sensors for soil moisture, temperature and light level data. We use 3 sensors over i2c using
# address 0x20, 0x21 and 0x22. The moisture sensors default to 0x20, so they need to be configured to the address you want to use.
# I take an average temperature and light reading from across the sensors, but soil moisture reading is per planter.

# Please check out Catnip Electronics Tindie store:
# https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/
# https://github.com/ageir/chirp-rpi - library reference and python class

# Aidan Taylor 20/12/17
# Part of the IoT Crop Care Project

import chirp # this is the Catnip Electronics python class for the Chirp! sensor 
from time import sleep # not needed as timing is handled in main.py
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM) # use the BCM pin numbering system

# Sensor Address and Manual Calibration, min/max values determine percentage approximation:
soilSens1_addr = 0x20
soilSens2_addr = 0x21
soilSens3_addr = 0x22

soilSens1_min = 238 # calibrations were made by testing the sensor in open air vs dunked in water
soilSens1_max = 540
soilSens2_min = 244
soilSens2_max = 500
soilSens3_min = 232
soilSens3_max = 550

# Initialise the soil sensors
soilSens1 = soilSens1 = chirp.Chirp(address=soilSens1_addr, read_moist=True, read_temp=True,
        read_light=True, min_moist=soilSens1_min, max_moist=soilSens1_max, temp_scale='celsius',
        temp_offset=0)
soilSens2 = soilSens2 = chirp.Chirp(address=soilSens2_addr, read_moist=True, read_temp=True,
        read_light=True, min_moist=soilSens2_min, max_moist=soilSens2_max, temp_scale='celsius',
        temp_offset=0)
soilSens3 = soilSens3 = chirp.Chirp(address=soilSens3_addr, read_moist=True, read_temp=True,
        read_light=True, min_moist=soilSens3_min, max_moist=soilSens3_max, temp_scale='celsius',
        temp_offset=0)

# Reservoir sensor setup
waterSensPin = 25 # rain sensor attached to BCM pin 16, we only need a digital reading
GPIO.setup(waterSensPin, GPIO.IN)

def lightConversion(n):
    # The light sensing on the Chirp! returns a range between 65535 (dark) and 0 (light)
    # let's make it a % range
    sensorMin = 65535
    sensorMax = 0
    outMin = 0
    outMax = 100
    output = (((n-sensorMin)*(outMax-outMin))/(sensorMax-sensorMin))+outMin

    return (output)

def getSoilSensor1():
    # call this to read from soil sensor 1
    soilSens1.trigger() 
    soilSens1.trigger() # the chirp! reference says you need to trigger the sensor twice to get an up to date reading
    ss1Moisture = soilSens1.moist_percent
    ss1TempC = soilSens1.temp
    ss1Light = soilSens1.light

    ss1Light = lightConversion(ss1Light)

    return (ss1Moisture, ss1TempC, ss1Light)

def getSoilSensor2():
    # call this to read from soil sensor 2
    soilSens2.trigger() 
    soilSens2.trigger() # the chirp! reference says you need to trigger the sensor twice to get an up to date reading
    ss2Moisture = soilSens2.moist_percent
    ss2TempC = soilSens2.temp
    ss2Light = soilSens2.light
     
    ss2Light = lightConversion(ss2Light)
    
    return (ss2Moisture, ss2TempC, ss2Light)

def getSoilSensor3():

    # call this to read from soil sensor 3
    soilSens3.trigger() 
    soilSens3.trigger() # the chirp! reference says you need to trigger the sensor twice to get an up to date reading
    ss3Moisture = soilSens3.moist_percent
    ss3TempC = soilSens3.temp
    ss3Light = soilSens3.light

    ss3Light = lightConversion(ss3Light)

    return (ss3Moisture, ss3TempC, ss3Light)

def reservoirLevel():
    # we are currently using a cheap "rain sensor" to test water level - this is less than ideal as the PCB will definitely degrade
    # over time, an epoxy covered capacitive sensor like the soil sensors would possibly be a better choice in the future.

    waterLevel = GPIO.input(waterSensPin)
   # waterLevel = 1 # for testing only

    return (waterLevel) # easy peezy right?! n.b. the cheap rain sensors from eBay/Amazon go LOW/FALSE/0 when water is detected


testMode = 0 # change this to 1 to test this script or sensor readings

while (testMode==1):
    sensor1Output = getSoilSensor1()
    print sensor1Output
    sensor2Output = getSoilSensor2()
    print sensor2Output
    sensor3Output = getSoilSensor3()
    print sensor3Output
    waterLevel = reservoirLevel()
    print waterLevel

    sleep(1)
