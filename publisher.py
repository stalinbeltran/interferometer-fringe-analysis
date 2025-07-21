import redis
import base64
import numpy as np

class Publisher:
    
    redisdb = None
    pubsub = None
    # initializing the redis instance

    def init(self, hostIP = '127.0.0.1', port = 6379):
        self.redisdb = redis.Redis(
            host=hostIP,
            port=port,
            decode_responses=True # <-- this will ensure that binary data is decoded
        )
        
    def publish(self, tag, message):
        self.redisdb.publish(tag, message)
        
    def publishImage(self, tag, image):
        print(type(image))
        base64_encoded_bytes = base64.b64encode(image)
        self.publish(tag, base64_encoded_bytes)
        
    def subscribe(self, tag):
        print('self.redisdb')
        print(self.redisdb)
        self.pubsub = self.redisdb.pubsub()
        self.pubsub.subscribe(tag)
        
    def listen(self):
        return self.pubsub.listen()
        
    def getImage(self, imageStringBase64, width, height):
        bytesbase64 = base64.b64decode(imageStringBase64)
        img = np.frombuffer(bytesbase64, dtype=np.uint8)
        img = img.reshape((height, width))
        return img