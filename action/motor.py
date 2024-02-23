import serial
import time
import sys

try:
    port = 'COM5'
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
    time.sleep(20)

    arduino.write(str.encode('$21=0' + '\n'))
    print('limit switch off')
    time.sleep(2)

def segment1():

    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X-5.000Y-32.500F100000' + '\n'))
    print('motor segment 1')          #segment 1
    time.sleep(6)

def pos1():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X-9.000Y7.500F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z+10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z-10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91X-70.000Y20.000F100000'  + '\n'))
    time.sleep(8)


def pos2():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X9.000Y7.500F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z+10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z-10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91X-79.000Y20.000F100000'  + '\n'))
    time.sleep(8)

def pos3():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X-9.000Y-7.500F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z+10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z-10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91X-70.000Y35.000F100000'  + '\n'))
    time.sleep(8)

def pos4():
    arduino.write(str.encode('$X' + '\n'))
    time.sleep(2)

    arduino.write(str.encode('$J=G21G91X9.000Y-7.500F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z+10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91Z-10F100000'  + '\n'))
    time.sleep(3)

    arduino.write(str.encode('$J=G21G91X-79.000Y35.000F100000'  + '\n'))
    time.sleep(8)

arduino.write(str.encode('$X' + '\n'))