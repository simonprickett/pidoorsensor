import RPi.GPIO as GPIO
import time
import sys
import signal

def cleanupLights(signal, frame):
	GPIO.output(LEFT_RED_LIGHT, False)
	GPIO.output(LEFT_GREEN_LIGHT, False)
	GPIO.output(RIGHT_RED_LIGHT, False)
	GPIO.output(RIGHT_YELLOW_LIGHT, False)
	GPIO.output(RIGHT_GREEN_LIGHT, False)
	GPIO.cleanup()
	sys.exit(0)

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# This is the GPIO pin number we have one of the door sensor
# wires attached to, the other should be attached to a ground pin.
LEFT_DOOR_SENSOR_PIN = 12
LEFT_RED_LIGHT = 19
LEFT_GREEN_LIGHT = 26
RIGHT_DOOR_SENSOR_PIN = 18
RIGHT_RED_LIGHT = 3
RIGHT_YELLOW_LIGHT = 2
RIGHT_GREEN_LIGHT = 4

# Initially we don't know if the door is open or closed...
leftIsOpen = None
leftOldIsOpen = None
rightIsOpen = None
leftIsOpen = None

# Set up the door sensor pins.
GPIO.setup(LEFT_DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(RIGHT_DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Set up the light pins.
GPIO.setup(LEFT_RED_LIGHT, GPIO.OUT)
GPIO.setup(LEFT_GREEN_LIGHT, GPIO.OUT)
GPIO.setup(RIGHT_RED_LIGHT, GPIO.OUT)
GPIO.setup(RIGHT_YELLOW_LIGHT, GPIO.OUT)
GPIO.setup(RIGHT_GREEN_LIGHT, GPIO.OUT)

# Make sure all lights are off.
GPIO.output(LEFT_RED_LIGHT, False)
GPIO.output(LEFT_GREEN_LIGHT, False)

# Set the cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, cleanupLights)

while True:
	if (GPIO.input(LEFT_DOOR_SENSOR_PIN)):
		leftOldIsOpen = leftIsOpen
		leftIsOpen = True
	else:
		leftOldIsOpen = leftIsOpen
		leftIsOpen = False

	if (GPIO.input(RIGHT_DOOR_SENSOR_PIN)):
		rightOldIsOpen = rightIsOpen
		rightIsOpen = True
	else:
		rightOldIsOpen = rightIsOpen
		rightIsOpen = False

	if (leftIsOpen and (leftIsOpen != leftOldIsOpen)):
		print "Left space is unoccupied!"
		GPIO.output(LEFT_RED_LIGHT, False)
		GPIO.output(LEFT_GREEN_LIGHT, True)
	elif (leftIsOpen != leftOldIsOpen):
		print "Left space is occupied!"
		GPIO.output(LEFT_GREEN_LIGHT, False)
		GPIO.output(LEFT_RED_LIGHT, True)

	if (rightIsOpen and (rightIsOpen != rightOldIsOpen)):
		print "Right space is unoccupied!"
		GPIO.output(RIGHT_RED_LIGHT, False)
		GPIO.output(RIGHT_GREEN_LIGHT, True)
	elif (rightIsOpen != rightOldIsOpen):
		print "Right space is occupied!"
		GPIO.output(RIGHT_GREEN_LIGHT, False)
		GPIO.output(RIGHT_RED_LIGHT, True)
	
	time.sleep(0.1)
