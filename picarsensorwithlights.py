import RPi.GPIO as GPIO
import time
import sys
import signal

def cleanupLights(signal, frame):
	GPIO.output(RED_LIGHT, False)
	GPIO.output(YELLOW_LIGHT, False)
	GPIO.output(GREEN_LIGHT, False)
	GPIO.cleanup()
	sys.exit(0)

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# This is the GPIO pin number we have one of the door sensor
# wires attached to, the other should be attached to a ground pin.
DOOR_SENSOR_PIN = 18
RED_LIGHT = 9
YELLOW_LIGHT = 10
GREEN_LIGHT = 11

# Initially we don't know if the door is open or closed...
isOpen = None
oldIsOpen = None

# Set up the door sensor pin.
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Set up the light pins.
GPIO.setup(RED_LIGHT, GPIO.OUT)
GPIO.setup(YELLOW_LIGHT, GPIO.OUT)
GPIO.setup(GREEN_LIGHT, GPIO.OUT)

# Make sure all lights are off.
GPIO.output(RED_LIGHT, False)
GPIO.output(YELLOW_LIGHT, False)
GPIO.output(GREEN_LIGHT, False)

# Set the cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, cleanupLights)

while True:
	oldIsOpen = isOpen
	isOpen = GPIO.input(DOOR_SENSOR_PIN)

	if (isOpen and (isOpen != oldIsOpen)):
		print "Space is unoccupied!"
		GPIO.output(RED_LIGHT, False)
		GPIO.output(GREEN_LIGHT, True)
	elif (isOpen != oldIsOpen):
		print "Space is occupied!"
		GPIO.output(GREEN_LIGHT, False)
		GPIO.output(RED_LIGHT, True)
	
	time.sleep(0.1)
