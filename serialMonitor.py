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
        if isinstance(value, str):
            print('is string')
            value = value.encode('ascii', 'ignore')
        s.write(value)                    #send command to serial
        break
    if s.in_waiting: print(s.read())            #always write data received from serial


