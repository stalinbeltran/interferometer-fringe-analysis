import redis
import base64

class Publisher:
    
    redis = None
    # initializing the redis instance

    def _init_(self, hostIP = '127.0.0.1', port = 6379):
        self.redis = redis.Redis(
            host=hostIP,
            port=port,
            decode_responses=True # <-- this will ensure that binary data is decoded
        )
        
    def publish(self, tag, message):
        self.redis.publish(tag, message)
        
    def publishImage(self, tag, image):
        print(type(image))
        exit()
        
        a0 = np.arange(64,dtype=np.uint16).reshape(8,8)
        print (a0)
        arbitrary_binary_data = a0
        base64_encoded_bytes = base64.b64encode(a0)

        r.set('foo', base64_encoded_bytes)
        self.redis.publish(tag, message)
        
