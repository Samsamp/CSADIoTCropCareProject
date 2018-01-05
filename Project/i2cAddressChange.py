# This script should be used to change the address of a Chirp! i2c Soil Moisture
# Sensor. Just enter the current address and the address you want to change to 
# in the fields below.

# Part of the CSAD IoT Crop Care Project
# Aidan Taylor 5th January 2018

import chirp

sensorAddress = 0x20 
sensorNewAddress = 0x21 # change this to the address you want to use

soilSens = chirp.Chirp(address=sensorAddress, read_moist=True, read_temp=True,
        read_light=True, min_moist=200, max_moist=500, temp_scale='celsius',
        temp_offset=0)

soilSens.sensor_address = sensorNewAddress
print 'Sensor reassigned to...'
print sensorNewAddress
print 'done!'
