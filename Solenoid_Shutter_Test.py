import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
offset = 23
LD1 = 23
LD2 = 24
LD3 = 25
GPIO.setup(LD1, GPIO.OUT)
GPIO.setup(LD2, GPIO.OUT)
GPIO.setup(LD3, GPIO.OUT)
delay = 0.0100

def turnondiode(diodenum):
        if(LD1==diodenum+offset):
                GPIO.output(LD1,GPIO.HIGH)
        if(LD1!=diodenum+offset):
                GPIO.output(LD1,GPIO.LOW)
        if(LD2==diodenum+offset):
                GPIO.output(LD2,GPIO.HIGH)
        if(LD2!=diodenum+offset):
                GPIO.output(LD2,GPIO.LOW)
        if(LD3==diodenum+offset):
                GPIO.output(LD3,GPIO.HIGH)
        if(LD3!=diodenum+offset):
                GPIO.output(LD3,GPIO.LOW)

def cycle():
        turnondiode(0)
        time.sleep(delay)
        turnondiode(1)
        time.sleep(delay)
        turnondiode(2)
        time.sleep(delay)

while True:
        cycle()
