
import asyncio
from publisher import Publisher

pub = Publisher()
asyncio.run(pub.init())
print(pub)
pub.subscribe('phototaken')

for message in pub.listen():
    print(len(msg))
