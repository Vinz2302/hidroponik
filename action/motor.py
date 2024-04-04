import serial
import time
import sys

try:
    port = 'COM7'
    arduino = serial.Serial(port=port, timeout=0)
    print(f'Serial port connected on {port}')
except serial.SerialException as e:
    print(f"Failed to open serial port: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

arduino.baudrate = 115200
arduino.write("\r\n\r\n".encode())
time.sleep(2)


arduino.write(str.encode('$X' + '\n'))

def home():
    arduino.write(str.encode('$21=1' + '\n'))
    print('limit switch on')
    time.sleep(2)

    arduino.write(str.encode('$H' + '\n'))   
    print('homing')                       #homing
    time.sleep(30)

    arduino.write(str.encode('$21=0' + '\n'))
    print('limit switch off')
    time.sleep(2)

def segment1():

    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X-50.000Y-22.500Z-50.000F100000' + '\n'))
    print('motor segment 1')          #segment 1
    time.sleep(10)

def pos1():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91Z-20.000F100000'  + '\n'))
    print('jalan ke lubang 1')
    time.sleep(8)

    arduino.write(str.encode('$J=G21G91X-5.000Y-12.500F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91Z20.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91X-5.000F100000'  + '\n'))
    time.sleep(8)


def pos2():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91Z-20.000F100000'  + '\n'))
    print('jalan ke lubang 2')
    time.sleep(8)

    arduino.write(str.encode('$J=G21G91X-27.000Y-12.500F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91Z20.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91X-5.000F100000'  + '\n'))
    time.sleep(8)

def pos3():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91Z-20.000F100000'  + '\n'))
    print('jalan ke lubang 3')
    time.sleep(8)

    arduino.write(str.encode('$J=G21G91X-5.000Y-30.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91Z20.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91X-5.000F100000'  + '\n'))
    time.sleep(8)

def pos4():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91Z-20.000F100000'  + '\n'))
    print('jalan ke lubang 4')
    time.sleep(8)

    arduino.write(str.encode('$J=G21G91X-27.000Y-30.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91Z20.000F100000'  + '\n'))
    time.sleep(5)

    arduino.write(str.encode('$J=G21G91X-5.000F100000'  + '\n'))
    time.sleep(8)

def naik():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91Z-20.000F100000'  + '\n'))
    time.sleep(4)

arduino.write(str.encode('$X' + '\n'))