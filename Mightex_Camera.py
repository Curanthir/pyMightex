#!/usr/bin/python
# Mightex Python Program
# Joshua Brake

# Importing libraries
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
import os
import sys

if(sys.platform!='win32'):
	import pwd
	import grp

# Set start time to time stamp frames
starttime = time.time()

def arduinoenable():
	arduinoEnableInput = raw_input('Arduino enable? [y/n]: ')
	arduinoEnableInput = arduinoEnableInput.lower()
		
	while arduinoEnableInput not in ['y','n']:
		print("Invalid input. Please try again.")
		arduinoEnableInput = raw_input('Arduino enable? [y/n]: ')
		arduinoEnableInput = arduinoEnableInput.lower()
		
	if arduinoEnableInput == 'y':
		arduinoStatus = True
		print(arduinoEnableInput)
	else:
		arduinoStatus = False
	
	return arduinoStatus
		

# Arduino class to control laser diodes
class Arduino:
	def __init__(self):
		self.ser = serial.Serial('COM7',115200)
		self.serin = self.ser.readline()
		print self.serin.strip('\n')
		self.ser.write('0 0 0')
	
	def turn_on_laser_diode(self,ldnum):
		if ldnum == 0:
			self.ser.write('1 0 0')
			imagetag = '1'
		if ldnum == 1:
			self.ser.write('0 1 0')
			imagetag = '2'
		if ldnum == 2:
			self.ser.write('0 0 1')
			imagetag = '3'
		self.writeconfirmation = self.ser.readline()
		print self.writeconfirmation.strip('\n')
		return imagetag

			
# Camera class to control Mightex SCE-BG04-U CMOS Camera
class Camera:
	def __init__(self,res=(752,480),exposure_time=4,gain=8,fps=10):
		
		self.dev = usb.core.find(idVendor=0x04B4, idProduct=0x0228)
		
		# If no device is found
		if self.dev is None:
			raise ValueError('Device not found')
		else:
			pass
			
		# Sets camera to default configuration
		self.dev.set_configuration()
		
		# make sure we can read and write
		# not sure why this is necessary, but without this commands timeout
		r = self.dev.write(0x01,[0x21])
		r = self.dev.write(0x01,[0x21])
		r = self.dev.write(0x01,[0x21])
		r = self.dev.read(0x81,0x2E)

		self.get_device_info()
		
		self.set_mode(0x00)
		self.res = res
		self.exposure_time = exposure_time
		self.gain = gain
		self.fps = fps
		self.set_gain(self.gain)
		self.set_resolution(self.res)
		self.set_exposure_time(self.exposure_time)
		self.set_fps(self.fps)
		self.set_sensor_Hblanking()
		self.set_main_clock_freq()
		time.sleep(2)
		
	def get_device_info(self):
		self.dev.write(0x01,[0x21,0x01,0x00])
		info = self.dev.read(0x81,0x2E)
		#print("Info: " + str(info))
		
	def get_firmware_version(self):
		self.dev.write(0x01,[0x01])
		res = self.dev.read(0x81,0x05)
		return res.tolist()
		
	def set_mode(self,mode):
		self.dev.write(0x01, [0x30,0x01,mode])
			
	def set_resolution(self,res):
		xres = self.int2hexlist(res[0])
		yres = self.int2hexlist(res[1])
		result = self.dev.write(0x01, [0x60, 0x07, xres[0], xres[1], yres[0], yres[1], 0x00])
		self.res = res
		return result
			
	def set_gain(self,gain):
		if getattr(gain,'__iter__',False):
			if not len(gain) == 3:
				raise ValueError("Gain tuple must consist of exactly three values")
			res = self.dev.write(0x01,[0x62,0x03,gain[0],gain[1],gain[2]])
		else:
			res = self.dev.write(0x01,[0x62,0x03,gain,gain,gain])
			
		self.gain = gain
		
	def set_exposure_time(self,time):
		time_mult = int(time/0.05)
		time_mult = self.int2hexlist(time_mult)
		#print("Exposure time set to: " + str(time_mult) + "*0.05ms")
		self.dev.write(0x01, [0x63, 0x02, time_mult[0],time_mult[1]])
		self.exposure_time = float(time)
		self.set_fps(float(1.0/(self.exposure_time/1000)))
			
	def set_fps(self,frame_rate):
		time_mult = int(1./float(frame_rate)*float(1000)/0.05)
		time_mult = self.int2hexlist(time_mult)
		self.dev.write(0x01,[0x64,0x02,time_mult[0],time_mult[1]])
		self.fps = frame_rate
	
	def set_main_clock_freq(self):
		self.dev.write(0x01,[0x32,0x01,0x01])
		time.sleep(0.2)
		
	def set_sensor_Hblanking(self):
		self.dev.write(0x01,[0x36,0x01,0x02])
		
	def get_frame(self):
		img_len = self.res[0]*self.res[1]/2
			
		while True:
			array1=[]
			array2=[]

			# Get Camera Trigger State - Checks to see if settings match those set
			self.dev.write(0x01, [0x35, 0x01, 0x00])
			triggerS = self.dev.read(0x81, 0x08)
        
			# Get Image Data - Asks for data to be prepared
			self.dev.write(0x01, [0x34, 0x01, 0x01])
			# By now data was ready so reading of data is begun
			for x in xrange(0, img_len/512+1):
				array1.extend(self.dev.read(0x82,0x200))
				array2.extend(self.dev.read(0x86,0x200))
			
			# Get Current Frame Property
			self.dev.write(0x01, [0x33, 0x01, 0x00])
			frameP = self.dev.read(0x81, 0x18)
			
			if frameP[16] == 0:
				break
			
		SSAT = []

		for x in xrange(0,self.res[1]/2):
			arrayStart = x*self.res[0]
			arrayEnd = arrayStart+self.res[0]
			SSAT.extend(array1[arrayStart:arrayEnd])
			SSAT.extend(array2[arrayStart:arrayEnd])	
	
		image = np.reshape(SSAT,[self.res[1],self.res[0]])
		return image
			
	def saveimage(self,directory,framenum,imagetag,image):
		filename = directory + os.sep + str(framenum)+"_" + imagetag + '.png'
		f = open(filename,'wb')
		w = png.Writer(self.res[0],self.res[1],greyscale=True,bitdepth=8)
		w.write(f,image)
		if(sys.platform!='win32'):
			setpermissions(filename)
		f.close()
			
	def write(self,command,parameters):
		command_list = [command,len(parameters)]
		for i in parameters:
			command_list.append(i)
		return self.dev.write(0x01,command_list)

	def read(self,length,endpoint=0x81):
		return self.dev.read(endpoint,length)
			
	def int2hexlist(self,num):
		lsb = num & 0xFF
		msb = (num & 0xFF00) >> 0x8
		return [msb,lsb]
			
	def hexlist2int(self,hexlist):
		return (hexlist[0] << 0x8 + hexlist[1])
		
	def analyzeframe(self,image):
		imavg = np.average(image)
		immax = np.amax(image)
		print('Image average = ' + str(imavg) + ' ' + 'Image maximum = ' + str(immax))
		if immax == 255:
			saturation_flag = -1
			print('Image saturated!')
		else:
			saturation_flag = 0
		#return imavg, saturation_flag
		
	def getandsaveframe(self,directory):
		currenttime = time.time()-starttime
		if arduinoenabled is True:
			ldnum = i%3
			imagetag = arduino.turn_on_laser_diode(ldnum) + "_" + '%08.2f'%currenttime
				
		else:
			imagetag = 'Camera_Only'
		
		img = camera.get_frame()
		camera.saveimage(directory,i,imagetag,img)
		print("Got frame #" + str(i))
		self.analyzeframe(img)

		
def createworkingdir(foldername):
	currentdir = os.getcwd()
	directory = currentdir + os.sep + foldername
	
	if not os.path.exists(directory):
		os.mkdir(directory)
	
	setpermissions(directory)
	
	return directory

def setpermissions(path):
	uid = pwd.getpwnam("joshbrake").pw_uid
        gid = grp.getgrnam("user").gr_gid

	os.chmod(path,0755)
        os.chown(path,uid,gid)

def getuserinput():
	print("Folder name?")
	foldername = raw_input()
	directory = createworkingdir(foldername)
	
	print("How many frames?")
	numframes = raw_input()
	print("----------------------")
	return numframes,directory
			
if __name__ == "__main__":

	arduinoenabled = arduinoenable()
	if arduinoenabled is True:
		arduino = Arduino()
		
	camera = Camera()
	[numframes,directory] = getuserinput()
	
	if numframes == 'go':
		i = 0
		while True:
			camera.getandsaveframe(directory)
			i +=1
		
	else:
		for i in xrange(0,int(numframes)):
			camera.getandsaveframe(directory)
