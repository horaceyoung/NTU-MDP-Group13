import serial  # conda install 'python -m pip install pyserial'
import time
from colors import *
from config import SERIAL_PORT, BAUD_RATE, LOCALE


class arduinoComm(object):
    def __init__(self, serial_port=SERIAL_PORT, baud_rate=BAUD_RATE):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.arduino_is_connected = False

    def connect_arduino(self):
        print("Waiting for Arduino serial connection..")
        while True:
            retry = False
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate)
                cprint(BOLD + GREEN, "Successfully Connected to Arduino!")
                self.arduino_is_connected = True
                retry = False
            except Exception as error:
                print("Arduino Connection Failed: %s" % str(error))
                retry = True
            if not retry:
                break
            print("Retrying Arduino Connection..")
            time.sleep(1)

    def arduino_connected(self):
        return self.arduino_is_connected

    def disconnect_arduino(self):
        if self.ser:
            self.ser.close()
            print("Disconnecting Arduino..")
        self.arduino_is_connected = False
        if not self.arduino_is_connected:
            print("Successfully Disconected Arduino!")

    def read_arduino(self):
        try:
            self.ser.flush()
            get_data = self.ser.readline()
            print("Read from Arduino: %s" % get_data.rstrip())
            return get_data
        except Exception as error:
            print("arduinoMod/Arduino Read Failed: %s" % str(error))
            if "Input/output error" in str(error):
                self.disconnect_arduino()
                cprint(
                    BOLD + RED,
                    "Arduino disconnected.. Arduino read failed.. Retrying Arduino connection..",
                )
                self.connect_arduino()

    def write_arduino(self, message):
        try:
            if not self.arduino_is_connected:
                cprint(BOLD + RED, "Arduino is not connected! Arduino write failed..")
                return
            message = message.encode(LOCALE)
            self.ser.write(message)
            print("Write to Arduino: %s" % message)
        except Exception as error:
            print("arduinoMod/Arduino Write Failed: %s" % str(error))
