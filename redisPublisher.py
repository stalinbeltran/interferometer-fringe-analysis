import redis

# initializing the redis instance
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True # <-- this will ensure that binary data is decoded
)


while True:
    message = input("Enter the message you want to send to solders: ")
    if message == 'q': break
    r.publish("army-camp-1", message)
