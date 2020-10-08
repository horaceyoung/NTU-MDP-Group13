import socket
import multiprocessing
import json
import threading
import time
import re
from configurations import *


class TcpClient:
    def __init__(self, ip, port, buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_queue = multiprocessing.Queue()
        self.recv_json_queue = multiprocessing.Queue()
        self.recv_string_queue = multiprocessing.Queue()
        self.sensor_value_queue = multiprocessing.Queue()
        self.android_command_queue = multiprocessing.Queue()

    def run(self):
        self.connect()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def connect(self):
        print("connect called")
        self.client_socket.connect((self.ip, self.port))
        self.connected = True
        print("TcpClient - Connected on {}:{}".format(self.ip, self.port))

    def recv(self):
        data = None
        if self.connected:
            try:
                self.client_socket.settimeout(3)
                print("Receiving from client socket......")
                data = self.client_socket.recv(self.buffer_size)
                #print("successfully called client socket receive command")
                if not data:
                    print("Error: Not data")
                data_s = data.decode("utf-8")
                data_arr = data_s.splitlines()

                data_arr = list(filter(bool,data_arr))
                # print("TcpClient - Received data: {}".format(data_str))
                # self.recv_string_queue.put(data_str)
                for data_str in data_arr:
                    print("TcpClient - Received data: {}".format(data_str))
                    self.recv_string_queue.put(data_str)
                #print("Data Received: " + data)
            except Exception as inst:
                print("Error Receiving:",inst)
                # self.close_conn()

            #For handling of json if ever there is a need for it
            '''
            if data_str[0] == "{":
                self.recv_json_queue.put(data_str)
            else:
                self.recv_string_queue.put(data_str)

            '''

    #For debugging purpose
    '''
    def print_queue(self):
        while(not self.recv_string_queue.empty()):
            temp = self.recv_string_queue.get()
            print("data currently in queue:" ,temp)
    '''

    def send(self):
        # while self.connected:
        data = 'null'
        while not self.send_queue.empty():
            try:
                data = self.send_queue.get()
                print("Data to send:",data)
                self.client_socket.send((data + "\n").encode("utf-8"))
                print("TcpClient - Sent data: {}".format(data))
            except:
                print("TcpClient - Error sending data: {}".format(data))

    def disconnect(self):
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        print("Client socket disconnected")

    def get_android_command(self):
        if(self.android_command_queue.empty()):
            print("Queue is empty")
            return 0
        return self.android_command_queue.get()

    def get_sensor_value(self):
        if(self.sensor_value_queue.empty()):
            print("Queue is empty")
            return 0
        print(self.sensor_value_queue)
        return self.parse_sensor_value(self.sensor_value_queue.get())

    def send_mapdescriptor(self,map,obstacle,x,y,direction):
        '''
        message_header = "{\\\"map\\\":[{"
        message_tail = "}]}"
        explored_field = "\\\"explored\\\":\\\""+str(map)+"\\\""
        length_field = "\\\"length\\\":"+str(300)
        obstacle_field = "\\\"obstacle\\\":\\\""+str(obstacle)+"\\\""
        message = "B"+message_header + explored_field +","+length_field+","+obstacle_field+message_tail
        #jsonObj = json.loads(message)
        self.send_command(message)
        self.send()
        #print("Map Descriptor for Android:" + message)
        '''
        '''
        self.send_queue.put(json.dumps({"map": arena.to_mdf_part1(), "gridP2": arena.to_mdf_part2()}))
        '''
        #message = {"map":[{"explored":map, "length":300, "obstacle":obstacle}], "robotPosition":[int(x-1),convertY(int(y-1)),direction]}
        message = {"map":[{"explored":map[2:], "length":300, "obstacle":obstacle[2:]}], "robotPosition":[int(x-1),int(y-1),direction]}
        #message={"map":[{"explored":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","length":300,"obstacle":"1000000040008071002600600e00101820100034000000000"}],"robotPosition":[int(x),int(y),direction]}
        jsonObj=json.dumps(message)
        command = "B"+jsonObj
        self.send_command(command)
        self.send()


    def send_command(self, command):
        # self.send_queue.put(convertString.stringToList(command))
        print("In send queue function")
        self.send_queue.put(command)

    def send_status(self, status):
        self.send_queue.put(json.dumps({"status": status}))

    def send_event(self, event):
        self.send_queue.put(json.dumps({"event": event}))

    def send_robot_pos(self, pos):
        self.send_queue.put(json.dumps({"robotPos": pos}))



    def close_conn(self):
        try:
            self.client_socket.close()
            self.connected = False
            print("TcpClient - Disconnected")
        except:
            pass

    def send_movement_forward(self, step=1, calibrate=True):
        self.send_command("AA" + str(step))
        if calibrate:
            self.send_movement_calibrate()


    def send_movement_rotate_left(self, calibrate=True):
        self.send_command("AL")
        if calibrate:
            self.send_movement_calibrate()


    def send_movement_rotate_right(self, calibrate=True):
        self.send_command("AR")
        if calibrate:
            self.send_movement_calibrate()

    def send_movement_rotate_back(self, calibrate=True):
        self.send_command("AR")
        self.send_command("AR")
        if calibrate:
            self.send_movement_calibrate()

    def only1inqueue(self):
        length = self.sensor_value_queue.qsize()-1
        for i in range(length):
            self.sensor_value_queue.get()


    def send_movement_calibrate(self):
        self.send_command("AC")
        self.send()

    def send_ready(self):
        print("In send ready function")
        self.send_command("AS")
        self.send()

    #This method is used to get value stored in multiprocessing queue
    def update_queue(self):
        #data = 0
        print("Updating android command queue & sensor value queue....")
        counter = 0
        try:
            while(self.recv_string_queue.empty()):
                print("Update Attempt: ",counter)
                if(counter == 2):
                    print("Have called socket recv command 5 times but still no data coming from RPI")
                    return 0
                #if(self.recv_string_queue.empty()):
                self.recv()
                if(not self.recv_string_queue.empty()):
                    break
                #print("Finished calling receive command")
                #data = self.get_string()
                counter += 1
            self.organise_data()
        except Exception as inst:
            print("Update Queue Error:",inst)
        #return self.determine_type(data)

    def parse_sensor_value(self,data):
        try:
            sensorVal = data.split(":")  # 1:SRFL,2:SRFC,3:SRFR,4:SRTR,5:SRBR,6:SRL
            last = sensorVal[-1]
            idx = last.find("\\")
            last = last[:idx]
            sensorVal = sensorVal[1:-1] + [last]
        except Exception as err:
            print("Error parsing:", err)
        return sensorVal


    #Organise receive string queue to android command only queue or sensor value only queue
    def organise_data(self):
        try:
            while(not self.recv_string_queue.empty()):
                data = self.recv_string_queue.get()
                clean = data.strip()
                matchObj = re.match(r'b',clean,re.I)
                if matchObj:
                    self.sensor_value_queue.put(data)
                else:
                    self.android_command_queue.put(data)
            self.only1inqueue()
        except Exception as err:
            print("Something gone wrong at organising data:", err)

    #Need ask android how they want to send the coordinate
    def take_picture(self,coordinate=None):
        print("Taking Picture.....")
        try:
            string = "P"
            self.send_command(string)
            self.send()
            print("Successfully send")
            #self.send_command("BP:" + str(coordinate))
        except Exception as inst:
            print("Error sending take picture commands to RPI:", inst)

    '''
    def get_android_command(self):
        print("Listening for Android command...")
        try:
            self.recv()
            data = self.get_string()
            command = data.strip()
            print("Receive Android command:"+command)
        except Exception as inst:
            print("Error receiving Android command:", inst)
        return command
    '''

    #For debug or future use
    def empty_sensor_queue(self):
        while(not self.sensor_val_queue.empty()):
            self.sensor_val_queue.get()



    def get_json(self):
        while self.recv_json_queue.empty() and self.connected:
            pass
        return self.recv_json_queue.get()

    def get_string(self):
        #For debug purpose
        '''
        start = time.time()
        end = time.time() + 3
        printed = 0
        counter = 3
        while self.recv_string_queue.empty() and start < end:
            self.recv()
            start = time.time()
            diff = int(end - start)
            if(printed != diff):
                print("Waiting to receive command for 3 sec:", counter)
                printed = diff
                counter -= 1
        '''

        if(self.recv_string_queue.empty()):
            print("Queue is empty")
            return 0
        return self.recv_string_queue.get()

    def send_arena(self, arena):
        self.send_queue.put(
            json.dumps({"gridP1": arena.to_mdf_part1(), "gridP2": arena.to_mdf_part2()})
        )

    '''
    def real_sense(self):
        try:
            sensor_val = self.get_sensor_value()
            print(sensor_val)
            for i in range(1,7,1):
                if(int(sensor_val[i])>-1):
                    self.take_picture()
        except Exception as inst:
            print("error in real sense", inst)
    '''
