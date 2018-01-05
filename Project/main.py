# This is the top level script for the CSAD IoT Crop Care system. This script will send
# data collected from sensors to a Thingspeak channel and will also test the soil moisture
# readings from the sensors to determine when watering is needed.
# 
# Part of the CSAD IoT Crop Care Project
# Aidan Taylor 28th December 2017

from Hologram.HologramCloud import HologramCloud
from time import sleep
import urllib2
from sensorReading import getSoilSensor1, getSoilSensor2, getSoilSensor3, reservoirLevel
from watering import waterPot1, waterPot2, waterPot3, end

# Hologram Setup
credentials = {'devicekey': 'xxxxxxxx'} # replace with your unique Sim device key
cloud = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')

# Thingspeak Setup:
myAPI = "xxxxxxxxxxxxxxxx" # replace with your ThingSpeak Write API Key

# Control variables:
# The following values set the soil moisture point that triggers a watering cycle
pot1SoilThresh = 30.0
pot2SoilThresh = 30.0
pot3SoilThresh = 30.0

cycleTime = 900 # this sets the refresh timer for the entire script - 900 for normal 15 minutes 

def main():
    print 'Welcome to the CSAD IoT Crop Care project, press ctrl-c to make a clean exit'
    print 'Please allow a little time for the Cellular interface to start'
    sleep(10) # lets allow a little time for the cellular interface to start - just in case :)
    startMsg = cloud.sendSMS("xxxxxxxxxxxxx", "Starting Program, maybe the Pi restarted?")
    # enter your mobile number in the space above, area code required
    sleep(60) # lets allow a little time for the cellular interface to restart

    print 'Program will now run! See Thingspeak channel for live sensor data...'
    sleep(1)

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    sleep(1)
    
    SMSSent = 0 # latch to prevent SMS spam

    while True:
        try:
           # Every 15 minutes Sensors take a reading (sleep is at the end of script)
           
            pot1Soil, pot1TempC, pot1Light = getSoilSensor1()
            pot2Soil, pot2TempC, pot2Light = getSoilSensor2()
            pot3Soil, pot3TempC, pot3Light = getSoilSensor3()
    
            print('Pot 1 Moisture: '+repr(pot1Soil)+'% Pot 2 Moisture: '+repr(pot2Soil)+'% Pot 3 Moisture: '+repr(pot3Soil)+'%')

            tempAVG = (pot1TempC+pot2TempC+pot3TempC)/3 # average temperature
            lightAVG = (pot1Light+pot2Light+pot3Light)/3 # average light

            # Send the sensor reading to ThingSpeak:
            try:
                f = urllib2.urlopen(baseURL+"&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s"%(pot1Soil, pot2Soil, pot3Soil, tempAVG, lightAVG))
                
                f.close() # I'm not sure this is needed, test it!
                print 'sensor data uploaded to cloud'

            except:
                print 'connection failed, continuing anyway...'

            # Test Sensor Readings:
            # First check if any pots need watering...
            if(pot1Soil<pot1SoilThresh) or (pot2Soil<pot2SoilThresh) or (pot3Soil<pot3SoilThresh):
                print 'Watering Required, checking reservoir level'
                waterLevel = reservoirLevel()
                if(waterLevel == 0): # reservoirLevel returns logic-low if the reservoir has enough water to run the pump
                    SMSSent = 0 # reset the SMS latch
                    # lets determine which pots to water
                    if(pot1Soil<pot1SoilThresh):
                        print 'Start pot 1 watering routine'
                        waterPot1()
                        print 'End pot 1 watering routine'
                    if(pot2Soil<pot2SoilThresh): 
                        print 'Start pot 2 watering routine'
                        waterPot2()
                        print 'End pot 2 watering routine'
                    if(pot3Soil<pot3SoilThresh): 
                        print 'Start pot 3 watering routine'
                        waterPot3()
                        sleep(2)
                        print 'End pot 3 watering routine' 
                    print 'Watering done'
                    sleep(2)
                else:
                    print 'Warning! Reservoir too low, unable to water'
                    if(SMSSent != 1):
                        # send an SMS to alert user that the reservoir needs topping up
                        SMSSent = 1 # this is just to prevent the program spamming SMS
                        resLVL = cloud.sendSMS("xxxxxxxxxxxxx", "Warning! Reservoir too low, unable to water")
			# replace the blank space with your mobile number, area code required
            else:
                print 'No action required'

            sleep(cycleTime) # 900 seconds is the normal sleep cycle

        except KeyboardInterrupt:
            # exit routine if ctrl-c is pressed:
            print 'ending program'
            end()
            print 'GPIO cleanup done!'
            print 'goodbye!'
            break
    
# call main
if __name__ == '__main__':
    main()
