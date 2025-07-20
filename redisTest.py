#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/redisTest.py

import numpy as np
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
a0 = np.arange(64,dtype=np.uint16).reshape(8,8)
arbitrary_binary_data = a0
base64_encoded_bytes = base64.b64encode(a0)

r.set('foo', base64_encoded_bytes)
getted = r.get('foo')
print(getted)


b = np.frombuffer(getted, dtype='<f4') # or dtype=np.dtype('<f4'), or np.float32 on a little-endian system (which most computers are these days)
print (b)
# Or, if you want big-endian:

# >>> np.frombuffer(b'\x00\x00\x80?\x00\x00\x00@\x00\x00@@\x00\x00\x80@', dtype='>f4') # or dtype=np.dtype('>f4'), or np.float32  on a big-endian system
# array([  4.60060299e-41,   8.96831017e-44,   2.30485571e-41,
         # 4.60074312e-41], dtype=float32)



# safe_string_base64 = base64.b64decode(getted)
# print('safe_string_base64')
# print(safe_string_base64)








import struct
import redis

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
