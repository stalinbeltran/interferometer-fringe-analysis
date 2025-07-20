#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/redisTest.py

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('foo', 'bar')
# True
getted = r.get('foo')
print(getted)
# bar

