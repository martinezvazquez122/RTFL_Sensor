import RPi.GPIO as GPIO
import time
import logging

GPIO.setmode(GPIO.BOARD)

TRIG = 37
ECHO = 38

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/home/pi/Desktop/Scripts/myapp.txt', mode='w')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO,GPIO.IN)

time.sleep(0.1)

print ("Starting Measurements...")

GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,0)

while GPIO.input(ECHO) == 0:
    pass
start = time.time()

while GPIO.input(ECHO) == 1:
    pass
stop = time.time()

result = (stop-start) * 17000

print result
logger.info(result)

GPIO.cleanup()
