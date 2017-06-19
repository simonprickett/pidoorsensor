import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	if GPIO.input(18):
		print "Door open!"
	else:
		print "Door closed!"
	
	time.sleep(0.1)
