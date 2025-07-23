import globals
import serial
from publisher import Publisher
import time

s = serial.Serial(globals.SERIAL_PORT_NAME)

for i in range(0, 0):
 time.sleep(5)
 s.write('hide'.encode('ascii', 'ignore'))
 time.sleep(5)
 s.write('show'.encode('ascii', 'ignore'))
#time.sleep(10)

pub = Publisher()
pub.init()
print(pub)
pub.subscribe('commandShutter')


while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key): break
    message = pub.get_message()
    if message:
        value = message["data"]
        if isinstance(value, str):
            print('is string')
            value = value.encode('ascii', 'ignore')
        s.write(value)                    #send command to serial
    if s.in_waiting: 
        value = s.readline()
        text = value.decode('utf-8')
        print(text)            #always write data received from serial


