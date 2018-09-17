#!/usr/bin/python3
#Authors Christopher Hill and Max Gobel
import RPi.GPIO as GPIO
import time
import os
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from time import localtime, strftime


SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
clear = lambda: os.system('clear') #clear()    clears the console screen
GPIO.setmode(GPIO.BCM)
startTime=0
moniSpeed=0.5
timer = 0.35


switch1 = 4
switch2 = 17
switch3 = 27
switch4 = 22
values = ["Time\t  Timer\t    Pot\t  Temp\tLight"]

def switchSetup():
	GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def timeClock():
	secs = int(time.time()-startTime)
	hours=secs//(60*60)
	min=(secs-hours*60*60)//60
	seconds=secs%60
	#print('{:02d}:{:02d}:{:02d}'.format(hours,min,seconds))
	return '{:02d}:{:02d}:{:02d}'.format(hours,min,seconds)


def sw1():
	#startTime = time.time()
	clear()
	print("Time\t  Timer\t    Pot\t  Temp\tLight")
	return time.time()

def sw2(moniSpeed):
	if moniSpeed == 2:
		moniSpeed=0.5
	else:
		moniSpeed=moniSpeed+moniSpeed
	return moniSpeed


def sw4(values):
	num = 6
	if len(values)<6:
		num = len(values)
	for x in range(0,num):
		print(values[x])

def printer():
	return (str(strftime("%H:%M:%S",localtime()))+"  "+str(timeClock())+"  "+str(round((3.3*(mcp.read_adc(0))/1023),1))+"V  "+str(int(mcp.read_adc(2)//14.61428))+"C   "+str((mcp.read_adc(1)*100)/1023)+"%")


#def getPot():


switchSetup()
startTime=time.time()
tempTime1=startTime
print("Time\t  Timer\t    Pot\t  Temp\tLight")

while True:
	if (time.time()-tempTime1)>moniSpeed:
		tempTime1=time.time()
		print(printer())
		#print(timeClock())
	Digital_switch1 = GPIO.input(switch1)
        Digital_switch2 = GPIO.input(switch2)
        Digital_switch3 = GPIO.input(switch3)
        Digital_switch4 = GPIO.input(switch4)
	#time.sleep(1)
	#print(timeClock())
	#print(moniSpeed)
	#moniSpeed=sw2(moniSpeed) #run when sw2 is pressed
	#tempTime = time.time()

	if Digital_switch1==0:
		startTime=sw1()
		time.sleep(timer)

	if Digital_switch2==0:
		moniSpeed = sw2(moniSpeed)
		print ("The monitor Speed is "+str(moniSpeed))
		time.sleep(timer)


	if Digital_switch3 == 0:
		time.sleep(timer)
		tempTime = time.time()
		Digital_switch3 = GPIO.input(switch3)
		while Digital_switch3 ==1:
			Digital_switch3 = GPIO.input(switch3)
			Digital_switch4 = GPIO.input(switch4)
			if math.floor((time.time()-tempTime)*10)/10  == moniSpeed:
				tempTime = time.time()
				values.append(printer()) #add others in
			if Digital_switch4 == 0:
				sw4(values)
				time.sleep(timer)
				tempTime=tempTime+0.35
		time.sleep(timer)
	del values[:]
	values = ["Time\t  Timer\t    Pot\t  Temp\tLight"]


