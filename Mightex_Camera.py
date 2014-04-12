# Mightex Python Program
# Joshua Brake

# Importing Libraries
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


rowsize = 752
colsize = 480
arraySize = (rowsize*colsize)/2
loop = arraySize/512
starttime = time.time()

# Arduino class to control laser diodes
class Arduino:
	def __init__(self):
		self.arduinoenable()
	
	def arduinoenable(self):
		print('Arduino enable? [1/0]')
		arduinoEnableInput = input()
		if arduinoEnableInput == 1:
			arduinoStatus = True
		else:
			arduinoStatus = False
		
		if arduinoStatus is True:
			ser = self.serial.Serial('COM7',9600)
			serin = self.ser.readline()
			print serin
			self.ser.write('0 0 0 ')
		return arduinoStatus
	
	def turn_on_laser_diode(self,ldnum):
		if ldnum == 0:
			self.ser.write('0 0 1')
			imagetag = '3'
		if ldnum == 1:
			self.ser.write('1 0 0')
			imagetag = '1'
		if ldnum == 2:
			self.ser.write('0 1 0')
			imagetag = '2'
			
# Camera class to control Mightex SCE-BG04-U		
class Camera:
	def __init__(self,res=(752,480),exposure_time=0.05,gain=8,fps=10):
		
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
		
	def set_mode(self,mode=0x00):
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
		img_len = self.res[0]*self.res[1]
			
		while True:
			array1=[]
			array2=[]

			# Get Camera Trigger State - Checks to see if settings match those set
			self.dev.write(0x01, [0x35, 0x01, 0x00])
			triggerS = self.dev.read(0x81, 0x08)
        
			# Get Image Data - Asks for data to be prepared
			self.dev.write(0x01, [0x34, 0x01, 0x01])
			# By now data was ready so reading of data is begun
			for x in xrange(0, loop+1):
				array1.extend(self.dev.read(0x82,0x200))
				array2.extend(self.dev.read(0x86,0x200))
			
			timestamp = t.time() - starttime
			# Get Current Frame Property
			self.dev.write(0x01, [0x33, 0x01, 0x00])
			frameP = self.dev.read(0x81, 0x18)
			
			if frameP[16] == 0:
				break
			
		SSAT = []

		for x in xrange(0,colsize/2):
			arrayStart = x*rowsize
			arrayEnd = arrayStart+rowsize
			SSAT.extend(array1[arrayStart:arrayEnd])
			SSAT.extend(array2[arrayStart:arrayEnd])	
	
		image = np.reshape(SSAT,[480,752])
		return image
			
	def saveimage(self,framenum,imagetag,image):
		filename = str(framenum)+"_" + imagetag
		f = open(filename + '.png','wb')
		w = png.Writer(752,480,greyscale=True,bitdepth=8)
		w.write(f,image)
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
			
if __name__ == "__main__":

	arduino = Arduino()
	camera = Camera()
	print("How many frames?")
	numframes = input()
	
	for i in xrange(0,numframes):
		img = camera.get_frame()
		camera.saveimage(i,'test',img)	