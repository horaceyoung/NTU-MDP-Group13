LOCALE = 'UTF-8'

# Tablet Bluetooth connection settings
RFCOMM_CHANNEL = 7
RPI_MAC_ADDR = 'B8:27:EB:3A:91:84'
UUID = '00001101-0000-1000-8000-00805f9b34fb'
TABLET_SOCKET_BUFFER_SIZE = 2048

# PC Wifi connection settings
# raspberryHotPotato: 192.168.3.1
WIFI_IP = '192.168.13.13'
WIFI_PORT = 22
PC_SOCKET_BUFFER_SIZE = 2048

# Arduino USB connection settings
# SERIAL_PORT = '/dev/ttyACM0'
# Symbolic link to always point to the correct port that arduino is connected to
# SERIAL_PORT = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75232303235351F091C0-if00'
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

# Image Recognition Settings
STOPPING_IMAGE = 'stop_image_processing.png'

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
IMAGE_FORMAT = 'bgr'

BASE_IP = 'tcp://192.168.13.'
PORT = ':22'

IMAGE_PROCESSING_SERVER_URLS = {
    'yinyi': BASE_IP + '00' + PORT,  # don't have ip address yet
    'zhenyan': BASE_IP + '00' + PORT,  # don't have ip address yet
}
