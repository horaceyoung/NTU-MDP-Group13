import socket
import sys
import time
from colors import *
from config import WIFI_IP, WIFI_PORT, PC_SOCKET_BUFFER_SIZE, LOCALE


class pcComm(object):
    def __init__(self, port=WIFI_PORT, wifi_ip="127.0.0.1"):
        self.port = 22
        self.wifi_ip = wifi_ip
        self.pc_is_connected = False

    def close_pc_socket(self):
        if self.client:
            self.client.close()
            print("Terminating client socket..")

        if self.conn:
            self.conn.close()
            print("Terminating server socket..")

        self.pc_is_connected = False
        if not self.pc_is_connected:
            print("Successfully Disconected PC!")

    def connect_pc(self):
        while True:
            retry = False
            try:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.conn.bind((self.wifi_ip, self.port))
                self.conn.listen(1)
                print(
                    "Listening for incoming PC connection on "
                    + self.wifi_ip
                    + ":"
                    + str(self.port)
                    + ".."
                )
                (self.client, self.addr) = self.conn.accept()
                cprint(
                    BOLD + GREEN,
                    "Successfully connected to PC! WIFI IP Address: " + str(self.addr),
                )
                self.pc_is_connected = True
                retry = False
            except Exception as error:
                print("PC Connection Failed: %s" % str(error))
                retry = True
            if not retry:
                break
            print("Retrying PC connection..")
            time.sleep(1)
        ###################### Testing####################################
        print("Testing sending data from PC:")
        string = "SDATA:2:3:1:4:5:2"
        self.write_PC(string)
        counter = 0
        while True:
            string = "b'SDATA:-1:2:-1:0:0:2\\r\\n\'"
            self.write_PC(string)
            print("Testing reading data from PC:")
            self.read_PC()
            counter += 1
            if(counter == 11):
                counter = 0
        #####################################################################

    def pc_connected(self):
        return self.pc_is_connected

    def read_PC(self):
        try:
            pc_data = self.client.recv(PC_SOCKET_BUFFER_SIZE)
            pc_data = pc_data.decode(LOCALE)
            if not pc_data:
                self.close_pc_socket()
                cprint(
                    BOLD + RED,
                    "PC disconnected.. PC read failed.. Retrying PC connection..",
                )
                self.connect_pc()
                return pc_data
            print("Read from PC: " + pc_data.rstrip())
            return pc_data
        except Exception as error:
            print("pcMod/PC Read Failed: %s" % str(error))
            if "Broken pipe" in str(error) or "Connection reset by peer" in str(error):
                self.close_pc_socket()
                cprint(
                    BOLD + RED,
                    "PC broken pipe.. PC read failed.. Retrying PC connection..",
                )
                self.connect_pc()

    def write_PC(self, message):
        try:
            if not self.pc_is_connected:
                cprint(BOLD + RED, "PC is not connected! PC write failed..")
                return
            message = message + "\n"
            message = message.encode(LOCALE)
            self.client.sendto(message, self.addr)
            print("Write to PC: " + message)
        except Exception as error:
            print("pcMod/PC Write Failed: %s" % str(error))
