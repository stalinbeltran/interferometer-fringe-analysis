import serial
from publisher import Publisher

SERIAL_PORT_NAME = 'COM3'
s = serial.Serial(SERIAL_PORT_NAME)

pub = Publisher()
pub.init()
print(pub)
pub.subscribe('commandShutter')


while True:
    message = pub.get_message()
    if message:
        value = message["data"]
        s.write(value)                    #send command to serial
    if s.in_waiting: print(s.readline())            #always write data received from serial

