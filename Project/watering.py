# This script contains the watering routines for the planter, first a solenoid valve is activated (opened)
# which will route water to the associated pot, then after a short pause the pump will activate for a 
# set period. There is also an exit routine to deactivate the GPIO pins.

# This is part of the CSAD IoT Crop Care Project
# by Aidan Taylor 27th December 2017

import RPi.GPIO as GPIO
from time import sleep

# GPIO setup:
GPIO.setmode(GPIO.BCM) # use the BCM pin numbering system

pumpPin = 23
valve1Pin = 14
valve2Pin = 15
valve3Pin = 18

GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(valve1Pin, GPIO.OUT)
GPIO.setup(valve2Pin, GPIO.OUT)
GPIO.setup(valve3Pin, GPIO.OUT)

def waterPot1():
    print "pot 1 routine"
    GPIO.output(valve1Pin, GPIO.HIGH) # open the solenoid valve
    sleep(2)
    GPIO.output(pumpPin, GPIO.HIGH) # turn on the DC Pump
    sleep(15)
    GPIO.output(pumpPin, GPIO.LOW) # turn off the DC Pump
    sleep(2)
    GPIO.output(valve1Pin, GPIO.LOW) # close the solenoid valve
    sleep(2)

def waterPot2():
    print "pot 2 routine"
    GPIO.output(valve2Pin, GPIO.HIGH) # open the solenoid valve
    sleep(2)
    GPIO.output(pumpPin, GPIO.HIGH) # turn on the DC Pump
    sleep(15)
    GPIO.output(pumpPin, GPIO.LOW) # turn off the DC Pump
    sleep(2)
    GPIO.output(valve2Pin, GPIO.LOW) # close the solenoid valve
    sleep(2)

def waterPot3():
    print "pot 3 routine"
    GPIO.output(valve3Pin, GPIO.HIGH) # open the solenoid valve
    sleep(2)
    GPIO.output(pumpPin, GPIO.HIGH) # turn on the DC Pump
    sleep(15)
    GPIO.output(pumpPin, GPIO.LOW) # turn off the DC Pump
    sleep(2)
    GPIO.output(valve3Pin, GPIO.LOW) # close the solenoid valve
    sleep(2)

def end():
    print "end"
    GPIO.cleanup()
    sleep(1)

testMode = 0 # set this to 1 to test the actuators

if(testMode==1):
    waterPot1()
    waterPot2()
    waterPot3()
    end()
