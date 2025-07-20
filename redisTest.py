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
print (a0)
arbitrary_binary_data = a0
base64_encoded_bytes = base64.b64encode(a0)

r.set('foo', base64_encoded_bytes)
getted = r.get('foo')
print(getted)
safe_string_base64 = base64.b64decode(getted)

b = np.frombuffer(safe_string_base64, dtype=np.uint16)
print (b)
b = b.reshape(8, 8)
print (b)
