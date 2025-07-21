
import redis

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)

# pubsub() method creates the pubsub object

mobile = r.pubsub()

# use .subscribe() method to subscribe to topic on which you want to listen for messages
mobile.subscribe('phototaken')

# .listen() returns a generator over which you can iterate and listen for messages from publisher

for message in mobile.listen():
    print(message) # <-- you can literally do any thing with this message i am just printing it
    if message['data'] == 'qc': exit()

