from bluetooth import * #conda install 'pip install PyBluez'
from colors import *
from config import LOCALE, RFCOMM_CHANNEL, RPI_MAC_ADDR, UUID, TABLET_SOCKET_BUFFER_SIZE


class tabletComm(object):

    def __init__(self):
        print ('')
        self.server_socket = None
        self.client_socket = None
        self.tablet_is_connected = False
        
    def connect_tablet(self):
        while True:
            retry = False
            try:
                self.server_sock = BluetoothSocket(RFCOMM)
                self.server_sock.bind(('', RFCOMM_CHANNEL))
                self.server_sock.listen(1)
                self.port = self.server_sock.getsockname()[1]
                advertise_service(self.server_sock, 'MDP-Server',service_id=UUID, service_classes=[UUID,SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])
                print ('Waiting for Bluetooth connection on RFCOMM channel %d..' % self.port)
                (self.client_sock, addr) = self.server_sock.accept()
                cprint(BOLD + GREEN, 'Successfully connected to Tablet! Tablet Bluetooth Address: ' + str(addr))
                self.tablet_is_connected = True
                retry = False
            except Exception as error:
                print ('Bluetooth Connection Failed: %s ' % str(error))
            if (not retry):
                break
            print ('Retrying Bluetooth Connection with Tablet..')

    def tablet_connected(self):   
        return self.tablet_is_connected

    def disconnect_tablet(self):
        try:
            if not (self.client_sock is None):
                self.client_socket.close()
                print ('Closing bluetooth client socket..')

            if not (self.server_socket is None):
                self.server_socket.close()
                print ('Closing bluetooth server socket..')

        except Exception as error:
            print ('Tablet Disconnect Failed: ' + str(error))
            pass

        self.tablet_is_connected = False

        if (not self.tablet_is_connected):
            print ('Successfully Disconected Tablet!')

    def read_tablet(self):
        try:
            data = self.client_sock.recv(TABLET_SOCKET_BUFFER_SIZE).decode(LOCALE)
            print ('Read from Tablet: ' + data.rstrip())
            return data
        except BluetoothError as error:
            print ('tabletMod/Tablet Read Failed: ' + str(error))
            if ('Connection reset by peer' in str(error)):
                self.disconnect_tablet()
                cprint(BOLD + RED, 'Bluetooth disconnected.. Tablet read failed.. Retrying bluetooth connection..')
                self.connect_tablet()

    def write_tablet(self, message):
        try:
            if (not self.tablet_is_connected):
                cprint(BOLD + RED, 'Bluetooth is not connected! Tablet write failed..')
                return
            print('Write to Tablet: ')
            self.client_sock.send(str(message))
        except BluetoothError as error:
            print ('tabletMod/Tablet Write Failed: ' + str(error))