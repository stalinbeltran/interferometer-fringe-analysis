import redis
import time

# initializing the redis instance
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True # <-- this will ensure that binary data is decoded
)

time.sleep(3)
r.publish("phototaken", 'message')
while True:
    message = input("Enter the message you want to send to solders: ")
    r.publish("phototaken", message)
    if message == 'q': break
