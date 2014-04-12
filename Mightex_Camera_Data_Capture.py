# Mightex Python Program
# Joshua Brake and Josue Ortiz
# Importing Libraries - using special ones for usb interaction
import usb.core
import usb.util
import sys
import binascii
import png
import time
import serial
import numpy as np
from array import *
import time as t


rowb1 = 0x02
rowb2 = 0xF0
rowsize = 752
colb1 = 0x01
colb2 = 0xE0
colsize = 480
arraySize = (rowsize*colsize)/2
loop = arraySize/512
starttime = time.time()

print('Arduino enable? [1/0]')
arduinoEnableInput = input()
if arduinoEnableInput == 1:
	arduinoEnable = True
else:
	arduinoEnable = False
	

#Arduino Initialized
if arduinoEnable is True:
	ser = serial.Serial("COM7",9600)
	serin = ser.readline()
	print serin
	ser.write("0 0 0 ")

# Finding camera and creating an object
dev = usb.core.find(idVendor=0x04B4, idProduct=0x0228)

# If no device is found
if dev is None:
	raise ValueError('Device not found')

# Print out location
print(dev)

# Sets camera to default configuration
dev.set_configuration()

# Device Version
dev.write(0x01, [0x01])
version = dev.read(0x81, 0x2E)
print("Version:")
print(version)

# Device Info
##dev.write(0x01, [0x21, 0x01, 0x00])
##info = dev.read(0x81, 0x2D)
##print("info:")
##print(info)

#EEPROM Write - for testing
dev.write(0x01, [0x25, 0x34, 0x3C, 0x00, 0xFA, 0xCE])
wtest = dev.read(0x81, 0x03)
print("Write Test:")
print(wtest)

#EEPROM Read - for testing
dev.write(0x01, [0x26, 0x3, 0x3C, 0x00, 0x02])
rtest = dev.read(0x81, 0x0A)
print("Read Test:")
print(rtest)

# Set Camera Work Mode - Normal Mode
dev.write(0x01, [0x30, 0x01, 0x00])

# Set Main Clock Frequency
dev.write(0x01, [0x32, 0x01, 0x01])
time.sleep(.21)

# Get current frame property
dev.write(0x01, [0x33, 0x01, 0x00])
frameP = dev.read(0x81, 0x18)
print("Frame Properties: 1 | 18 | r(2) | c(2) | Bin | exp(2) | RGB | X(2) | Y(2) | IF | Time ")
print(frameP)

### Blanking
dev.write(0x01, [0x36, 0x01, 0x00])

# Set Resolution
dev.write(0x01, [0x60, 0x07, rowb1, rowb2, colb1, colb2, 0x00])

# Set Exposure Time - to 0.05ms ?????
dev.write(0x01, [0x63, 0x02, 0x00, 0x28])

Thecounted = 0

print("How many Pictures?")
end = input()

time.sleep(2);
while True:

	pickDiode = Thecounted % 3	
	if arduinoEnable is True:
		#print("mode: "+str(pickDiode))
		if pickDiode == 0:
			ser.write("0 0 1")
			imageTag = "3"
			#print("Turned on " + imageTag)
		if pickDiode == 1:
			ser.write("1 0 0")
			imageTag = "1"
			#print("Turned on " + imageTag)
		if pickDiode == 2:
			ser.write("0 1 0")
			imageTag = "2"
			#print("Turned on " + imageTag)
		time.sleep(2)
	if arduinoEnable is False:
		imageTag = ''
	

	while True:
							
		array1=[]*4608
		array2=[]*4608

		# Get Camera Trigger State - Checks to see if settings match those set
		dev.write(0x01, [0x35, 0x01, 0x00])
		triggerS = dev.read(0x81, 0x08)
		#print("Trigger State: 1 | 6 | r(2) | c(2) | Bin")
		#print(triggerS)
        
		# Get Image Data - Asks for data to be prepared
		dev.write(0x01, [0x34, 0x01, 0x01])
		# By now data was ready so reading of data is begun
		for x in xrange(0, loop+1):
			array1.extend(dev.read(0x82, 0x200))
			array2.extend(dev.read(0x86, 0x200))
			
		# First frame is always garbage, so throw if it is the first capture, throw it out and get a new one
		if Thecounted == 0:
			dev.write(0x01, [0x35, 0x01, 0x00])
			triggerS = dev.read(0x81, 0x08)
			dev.write(0x01, [0x34, 0x01, 0x01])
			for x in xrange(0, loop+1):
				array1.extend(dev.read(0x82, 0x200))
				array2.extend(dev.read(0x86, 0x200))
			
		
		timestamp = t.time() - starttime
		# Get Current Frame Property
		dev.write(0x01, [0x33, 0x01, 0x00])
		frameP = dev.read(0x81, 0x18)
		#print("Frame Properties: 1 | 18 | r(2) | c(2) | Bin | exp(2) | RGB | X(2) | Y(2) | IF | Time ")
		#print(frameP)
		if frameP[16] == 0:
			break
			
	SSAT = []

	for x in xrange(0,colsize/2):
		arrayStart = x*rowsize
		arrayEnd = arrayStart+rowsize
		SSAT.extend(array1[arrayStart:arrayEnd])
		SSAT.extend(array2[arrayStart:arrayEnd])	
        #print("Length SSAT: " + str(len(SSAT)))
	
	image = np.reshape(SSAT,[480,752])
	filename = str(Thecounted)+"_" + imageTag
	#np.savetxt(filename + '.txt',image,fmt='%-3.3i',delimiter=' ',newline='\n',header='%08.2f'%timestamp)
	
	f = open(filename + '.png','wb')
	w = png.Writer(752,480,greyscale=True,bitdepth=8)
	w.write(f,image)
	f.close()
	
	print("Image #" + str(Thecounted) + " Time: " + '%08.2f'%timestamp)
	Thecounted += 1
	if Thecounted == end:
		print("Done!")
		break
