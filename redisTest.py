#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/redisTest.py

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('foo', 'bar')
# True
getted = r.get('foo')
print(getted)
# bar




r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})
# True

getted = r.hgetall('user-session:123')
print(getted)
# {'surname': 'Smith', 'name': 'John', 'company': 'Redis', 'age': '29'}




import base64

arbitrary_binary_data = b'\x01\x02\x03\x04\xffasd'
base64_encoded_bytes = base64.b64encode(arbitrary_binary_data)
safe_string_base64 = base64_encoded_bytes.decode('utf-8')
print(safe_string_base64)








import struct
import redis
import numpy as np

def toRedis(r,a,n):
   """Store given Numpy array 'a' in Redis under key 'n'"""
   h, w = a.shape
   shape = struct.pack('>II',h,w)
   print('shape', shape)
   encoded = shape + a.tobytes()

   # Store encoded data in Redis
   r.set(n,encoded)
   return

def fromRedis(r,n):
   """Retrieve Numpy array from Redis key 'n'"""
   encoded = r.get(n)
   h, w = struct.unpack('>II',encoded[:8])
   # Add slicing here, or else the array would differ from the original
   a = np.frombuffer(encoded[8:]).reshape(h,w)
   return a

# Create 80x80 numpy array to store
a0 = np.arange(6400,dtype=np.uint16).reshape(80,80) 

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Store array a0 in Redis under name 'a0array'
toRedis(r,a0,'a0array')

# Retrieve from Redis
a1 = fromRedis(r,'a0array')

np.testing.assert_array_equal(a0,a1)


