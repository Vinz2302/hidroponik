import serial
import time

arduino = serial.Serial(port = 'COM8', timeout=0)
arduino.baudrate = 9600
time.sleep(2)

def buka():
    arduino.write(str.encode('1'))
    time.sleep(2)
    print("buka")

def tutup():
    arduino.write(str.encode('0'))
    time.sleep(2)
    print("tutup")

# buka()
# tutup()