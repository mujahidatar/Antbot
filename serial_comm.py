import serial
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
s = serial.Serial("/dev/ttyUSB0",9600)
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,1)
read=0
C=['P','Q','R']
def blink(pin):
    GPIO.output(pin,0)
    sleep(1)
    GPIO.output(pin,1)
    sleep(1)
    return
m=0
while(m<=2):
    data_encode= C[m].encode('utf-8')
    s.write(data_encode)
    sleep(3)
    m=m+1
blink(11)
