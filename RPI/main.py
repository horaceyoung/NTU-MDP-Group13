import sys
import time

from arduinoMod import *
from pcMod import *
from tabletMod import *

from colors import *
import cv2 #conda install 'pip install opencv-python'

from picamera.array import PiRGBArray #conda install 'pip install "picamera[array]"'
from picamera import PiCamera #conda install 'pip install picamera'
import numpy as np

counter=0
class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.debug = False
        
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
        elif(readPCMessage[1].upper()=='P'):
            print("Taking image..")
            start_time=time.time()
            camera=PiCamera()
            time.sleep(0.001)
            i=readPCMessage[2:]
            global counter
            if counter%2==0:
                st="/home/pi/Desktop/Images/"+i+".jpg"
                camera.capture(st)
                print("Image captured successfully!")
            else:
                st="/home/pi/Desktop/Images1/"+i+".jpg"
                camera.capture(st)
                print("Image captured sucessfully!")
            counter= counter+1
            camera.close()
            end_time=time.time()
            print(end_time-start_time)

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

    #write function for tablet commnuication via bluetooth
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
            print ('Re-establishing tablet bluetooh connection..')
            self.tablet_thread.connect_tablet()

    def initialize_threads(self):
        self.readPCThread = threading.Thread(target = self.readPC, name = "pc_read_thread")
        self.readArduinoThread = threading.Thread(target = self.readArduino, name = "ar_read_thread")
        self.readTabletThread = threading.Thread(target = self.readTablet, name = "tb_read_thread")
        
        self.readPCThread.daemon = True
        self.readArduinoThread.daemon = True
        self.readTabletThread.daemon = True
        print ("All daemon threads initialized successfully!")

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
            time.sleep(1)


if __name__ == "__main__":
    mainThread = Main()
    mainThread.initialize_threads()
    mainThread.keep_main_alive()
    mainThread.close_all_sockets()
