import sys
import time
# import Queue
import threading
import json
from colors import *

from arduinoMod import *
from pcMod import *
from tabletMod import *
'''
from colors import *
import cv2 #conda install 'pip install opencv-python'
import imagRecogMod
from Queue import Queue

from picamera.array import PiRGBArray #conda install 'pip install "picamera[array]"'
from picamera import PiCamera #conda install 'pip install picamera'
import numpy as np
'''
counter=0
class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.debug = False

        # #Queue to receive obstacles info before scanning for images
        # self.imag_Queue = Queue()

        # #initialize PiCamera
		# self.camera = PiCamera()
		# self.camera.resolution = (640,480)
		# self.camera.framerate = 30
		# #self.rawCapture = PiRGBArray(self.camera, size=(1024, 768))
		# self.imagTaken = 0
		# #self.make_imag_brighter = True

        #initialize all the thread with each component class file
        self.arduino_thread = arduinoComm() #communication with arduino using threading
        self.pc_thread = pcComm() #communication with pc using threading
        self.tablet_thread = tabletComm() #communication with tablet using threading

        arduinoInitThread = threading.Thread(target = self.arduino_thread.connect_arduino, name = "arduino_init_thread")
        pcInitThread = threading.Thread(target = self.pc_thread.connect_pc, name = "pc_init_thread")
        tabletInitThread = threading.Thread(target = self.tablet_thread.connect_tablet, name = "tablet_init_thread")

        arduinoInitThread.daemon = True
        pcInitThread.daemon = True
        tabletInitThread.daemon = True

        #start all threading
        arduinoInitThread.start()
        pcInitThread.start()
        tabletInitThread.start()

        time.sleep(1)

        while not (self.arduino_thread.arduino_connected() and self.pc_thread.pc_connected() and self.tablet_thread.tablet_connected()):
            time.sleep(0.1)

    # #write function for image recognition
    # def imageRecognition(self):
	# 	try:
	# 		while True:
	# 			if not (self.imag_Queue.empty()):
	# 				thisJob = self.imag_Queue.get()
	# 				print("Image Recog: Processing job at robot center X=" + str(thisJob[0]) + ", center Y=" + str(thisJob[1]))
	# 				detect = imagRecogMod.ScanImage(self.debug, thisJob[9]) ###the function in the color reco mod thisjob[9] == imag taken


	# 				print("Image Recog: Detection results %s" % detect)
	# 				detectSplit = detect.split('|')
	# 				detectSplit = [int(i) for i in detectSplit]

	# 				if (detectSplit[0] == 1):
	# 					Image_ID = detectSplit[1]
	# 					if (detectSplit[2] == 0):
	# 						position = [thisJob[2], thisJob[3]] ####front left
	# 					elif(detectSplit[2] == 1):
	# 						position = [thisJob[4], thisJob[5]]  ####front center
	# 					else:
	# 						position = [thisJob[6], thisJob[7]] ####front right

	# 					###i dun know what i am doing
	# 					if(position[0] == -1 or position[1]== -1):
	# 						facing = thisJob[8]
	# 						x = thisJob[0]
	# 						y = thisJob[1]

	# 						if(facing==0):  #UP
	# 							position = [x,min(y+4,19)]

	# 						elif(facing==1): #down
	# 							position = [x, max(y-4,0)]

	# 						elif(facing==2): #Left
	# 							position = [max(x-4,0),y]

	# 						else:			 #Right
	# 							position = [min(x+4,19),y]

	# 					cprint(BOLD + GREEN, str(self.imagTaken) + " th image at: X=" + str(position[0]) + ", Y=" + str(position[1]) + ", ID=" + str(Image_ID))
	# 					detectResult = self.parse_json(position[0], position[1], Image_ID)
	# 					print(detectResult)
	# 					self.writeTablet(detectResult + "\r\n")
	# 			time.sleep(0.1)
	# 	except Exception as e:
	# 		print("main/arrowRecog Error: %s" % str(e))

	# def parse_json(self, x, y, image_ID):
	# 	data = {"x": x, "y": y, "ID": image_ID}
	# 	to_send = {"Image": [data]}
	# 	return json.dumps(to_send)

	# def takePicture(self):
	# 	# resol = (640,480)

	# 	# camera = PiCamera()
	# 	# camera.resolution = resol

	# 	output = PiRGBArray(self.camera)
	# 	self.camera.capture(output,'bgr')
	# 	src = output.array
	# 	self.imagTaken += 1
	# 	#print 'Capture %dx%d image' %(src.shape[1], src.shape[0])

	# 	return src

    #write functions for arduino board communication
    def readArduino(self):
        try:
            while True:
                readArduinoMessage = self.arduino_thread.read_arduino()
                if (readArduinoMessage is None):
                    print("No data read from Arduino!")
                    continue
                readArduinoMessage = readArduinoMessage.lstrip()
                if (len(readArduinoMessage) == 0):
                    print("No data read from Arduino!")
                    continue

                #read data from arduino to pc
                if (str(readArduinoMessage[0]).upper() == 'X'):
                    print("Successfully read data from Arduino to PC: %s" % readArduinoMessage[1:].rstrip())
                    self.writePC(readArduinoMessage[1:] + "\r\n")

                #read data from arduino to tablet
                elif (str(readArduinoMessage[0]).upper() == 'B'):
                    print("Successfully read data from Arduino to Tablet: %s" % readArduinoMessage[1:].rstrip())
                    self.writeTablet(readArduinoMessage[1:])

        except socket.error as error:
            print("Arduino disconnected! Arduino Read Failed!")

    def writeArduino(self, messageToArduino):
        #write data to arduino
        self.arduino_thread.write_arduino(messageToArduino)
        print("Successfully written data to Arduino: %s \r\n" % messageToArduino.rstrip())

    #write functions for PC communication via wifi
    def processMessage(self, readPCMessage):
        if (readPCMessage is None):
            print("No data read from PC!")
            return

        readPCMessage = readPCMessage.lstrip()

        if (len(readPCMessage) == 0):
            print("No data read from PC!")
            return

        if(readPCMessage[0].upper() == 'A'):
            print("Successfully read data from PC to Arduino: %s" % readPCMessage[1:].rstrip())
            self.writeArduino(readPCMessage[1:] + "\r\n")
        elif(readPCMessage[0].upper() == 'B'):
            print("Successfully read data from PC to Tablet: %s" % readPCMessage[1:].rstrip())
            self.writeTablet(readPCMessage[1:])
        elif(readPCMessage[0].upper() == 'R'):
            print("Successfully read data from PC to Algorithm: %s" % readPCMessage[1:].rstrip())
            self.writeArduino(readPCMessage[1:] + "\r\n")
        # elif(readPCMessage[0].upper()=='P'):
        #     imag = self.takePicture()
		# 	cv2.imwrite('images/'+str(self.imagTaken)+'.png', imag)
		# 	msgSplit = readPCMessage[1:].split('|')


			# if (msgSplit[8].upper().rstrip() == 'UP'):
			# 	robotFace = 0
			# elif (msgSplit[8].upper().rstrip() == 'DOWN'):
			# 	robotFace = 1
			# elif (msgSplit[8].upper().rstrip() == 'LEFT'):
			# 	robotFace = 2
			# elif (msgSplit[8].upper().rstrip() == 'RIGHT'):
			# 	robotFace = 3

            #             #newCmd = [int(msgSplit[0]), int(msgSplit[1]), int(msgSplit[2]), int(msgSplit[3]), int(msgSplit[4]),robotFace, imag]
			# newCmd = [int(msgSplit[0]), int(msgSplit[1]), int(msgSplit[2]), int(msgSplit[3]), int(msgSplit[4]), int(msgSplit[5]),int(msgSplit[6]), int(msgSplit[7]), robotFace, imag]
			# ##x|y|xl|yl|xm|ym|xr|xl|face|imag
			# self.imag_Queue.put(newCmd)

			# print("Scanning for image with front at: X=" + str(newCmd[0]) + ", Y=" + str(newCmd[1]))

        else:
            print("Incorrect header from PC (expecting 'B' for Android, 'A' for Arduino, 'R' for Algorithm, or 'P' for Image Recog.): [%s]" % readPCMessage[0])

    def readPC(self):
        try:
            while True:
                readPCMessage = self.pc_thread.read_PC()
                if (readPCMessage is None):
                    print("No data read from PC!")
                    continue
                readPCMessage = readPCMessage.split('\n')
                for msg in readPCMessage:
                    self.processMessage(msg)
        except Exception as error:
            print("main/PC Read Failed: %s" % str(error))

    def writePC(self, messageToPC):
        #write data to pc
        self.pc_thread.write_PC(messageToPC)
        print("Successfully written data to PC: %s \r\n" % messageToPC.rstrip())

    #write function for tablet communication via bluetooth
    def writeTablet(self, messageToTablet):
        self.tablet_thread.write_tablet(messageToTablet)
        print("Successfully written data to Tablet: %s" % messageToTablet.rstrip())

    def readTablet(self):
        while True:
            retry = False
            try:
                while True:
                    readTabletMessage = self.tablet_thread.read_tablet()
                    print("Tablet Message: %s" %readTabletMessage)
                    if (readTabletMessage is None):
                        print("No data read from Tablet!")
                        continue
                    readTabletMessage = readTabletMessage.lstrip()
                    if (len(readTabletMessage) == 0):
                        print("No data read from Tablet!")
                        continue
                    print("Tablet Message: %s" %readTabletMessage)
                    if (str(readTabletMessage[0]).upper() == 'X'):
                        print("Successfully read data from Tablet to PC: %s" % readTabletMessage[1:].rstrip())
                        self.writePC(readTabletMessage[1:]+ "\r\n")
                    elif (str(readTabletMessage[0]).upper() == 'A'):
                        print("Successfully read data from Tablet to Arduino: %s" % readTabletMessage[1:].rstrip())
                        self.writeArduino(readTabletMessage[1:]+"\r\n")
                    else:
                        print("Incorrect header from Tablet (expecting 'X' for PC, 'A' for Arduino): [%s]" % readTabletMessage[0])
            except Exception as error:
                print("main/Tablet Read Failed: %s" % str(error))
                retry = True
            if (not retry):
                break
            self.tablet_thread.disconnect_tablet()
            print ('Re-establishing tablet bluetooth connection..')
            self.tablet_thread.connect_tablet()

    def initialize_threads(self):
        # self.imagRecogThread = threading.Thread(target = self.imageRecognition, name = "imag_recog_thread")
        self.readPCThread = threading.Thread(target = self.readPC, name = "pc_read_thread")
        self.readArduinoThread = threading.Thread(target = self.readArduino, name = "ar_read_thread")
        self.readTabletThread = threading.Thread(target = self.readTablet, name = "tb_read_thread")

        # self.imagRecogThread.daemon = True
        self.readPCThread.daemon = True
        self.readArduinoThread.daemon = True
        self.readTabletThread.daemon = True
        print ("All daemon threads initialized successfully!")

        # self.imagRecogThread.start()
        self.readPCThread.start()
        self.readArduinoThread.start()
        self.readTabletThread.start()
        print ("All daemon threads started successfully!")

    def close_all_sockets(self):
        arduino_thread.close_all_sockets()
        pc_thread.close_all_sockets()
        tablet_thread.close_all_sockets()
        print ("All threads killed!")

    def keep_main_alive(self):
        while(1):
            if not (self.readPCThread.is_alive()):
                cprint(BOLD + RED, 'Fatal: PC thread is not running!')
            if not (self.readArduinoThread.is_alive()):
                cprint(BOLD + RED, 'Fatal: Arduino thread is not running!')
            if not (self.readTabletThread.is_alive()):
                cprint(BOLD + RED, 'Fatal: Tablet thread is not running!')

            # if not (self.imagRecogThread.is_alive()):
			# 	cprint(BOLD + RED, 'Fatal: Image Recognition thread is not running!')
			# 	self.imagRecogThread = threading.Thread(target = self.imageRecognition, name = "imag_recog_thread")
			# 	self.imagRecogThread.daemon = True
			# 	self.imagRecogThread.start()
			# 	cprint(BOLD + BLUE, 'Resolution: Image Recognition thread has been restarted.')

            time.sleep(1)


if __name__ == "__main__":
    mainThread = Main()
    mainThread.initialize_threads()
    #mainThread.readPC()
    mainThread.keep_main_alive()
    mainThread.close_all_sockets()
