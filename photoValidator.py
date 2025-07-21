
import time
from publisher import Publisher

pub = Publisher()
pub.init()
time.sleep(3)
print(pub)
pub.subscribe('phototaken')

for message in pub.listen():
    print((message))
    if message['data'] == 'qc': exit()
