import RPi.GPIO as GPIO
import time
import signal
import logging
import sys

GPIO.setmode(GPIO.BOARD)

def execute(var):
    GPIO.output(var,1)
    time.sleep(0.1)
    GPIO.output(var,0)
    
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
    
signal.signal(signal.SIGINT, signal_handler)

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/home/pi/Desktop/Scripts/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

interrupted = False
minimum = sys.maxint
yellowFlag = 0

TRIG = 7
ECHO = 12
TRIG1 = 16
ECHO1 = 18

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(TRIG1,GPIO.OUT)
GPIO.output(TRIG1,0)

GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(ECHO1,GPIO.IN)

time.sleep(0.1)

execute(TRIG)

while GPIO.input(ECHO) == 0:
	pass
start = time.time()

while GPIO.input(ECHO) == 1:
	pass
stop = time.time()

result = (stop-start) * 17000

execute(TRIG1)

while GPIO.input(ECHO1) == 0:
	pass
start = time.time()

while GPIO.input(ECHO1) == 1:
	pass
stop = time.time()

result1 = (stop-start) * 17000

size = result if result < result1 else result1

start = stop = result = result1 = 0 

print ("===============================")
print ("-   Starting Measurements...  -")
print ("===============================")

logger.info('======================================')
logger.info('-      Starting new measurements     -')
logger.info('======================================')

while True:

    execute(TRIG)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    result = (stop-start) * 17000
    
    execute(TRIG1)

    while GPIO.input(ECHO1) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO1) == 1:
        pass
    stop = time.time()

    result1 = (stop-start) * 17000
    
    finalResult = result if result < result1 else result1

    if finalResult < 0.5*size and finalResult > 0.20*size:
	if yellowFlag == 0:
	    logger.warning('Level is between 50% and 80% of total capacity!!!!!')
	    yellowFlag = 1
    elif finalResult < 0.20*size:
	logger.warning('Level is behond 80% of total capacity!!!!')
	logger.info('Powering down sensor to save battery')
	break        

    print("==========================")
    print("Sensor 1:")
    print(result)
    print("Sensor 2:")
    print(result1)
    print("Minumim value registred:")
    print(minimum)
    print("==========================")
    print("\n")
    
    if finalResult < minimum:
	minimum = finalResult
	logger.info('Minimum reading so far:')
	logger.info(minimum)
    
    time.sleep(2.0)
    
    if interrupted:
        print("...Gotta go")
        break

GPIO.cleanup()
