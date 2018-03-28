import RPi.GPIO as GPIO
import time
import signal

GPIO.setmode(GPIO.BOARD)

def execute(var):
    GPIO.output(var,1)
    time.sleep(0.1)
    GPIO.output(var,0)
    
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
    
signal.signal(signal.SIGINT, signal_handler)

interrupted = False

TRIG = 16
ECHO = 18

GREEN_LED = 37
YELLOW_LED = 38
RED_LED = 40

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(GREEN_LED,GPIO.OUT)
GPIO.output(GREEN_LED,0)

GPIO.setup(YELLOW_LED,GPIO.OUT)
GPIO.output(YELLOW_LED,0)

GPIO.setup(RED_LED,GPIO.OUT)
GPIO.output(RED_LED,0)

GPIO.setup(ECHO,GPIO.IN)

time.sleep(0.1)

print ("============================")
print ("Starting Measurements...")

while True:
    execute(TRIG)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    result = (stop-start) * 17000

    if result > 15:
        execute(GREEN_LED)
    elif result < 15 and result > 7:
        execute(YELLOW_LED)
    else:
        execute(RED_LED)

    print result
    
    time.sleep(1.0)
    
    if interrupted:
        print("...Gotta go")
        break

GPIO.cleanup()