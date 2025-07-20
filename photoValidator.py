


mobile = r.pubsub()

# use .subscribe() method to subscribe to topic on which you want to listen for messages
mobile.subscribe('army-camp-1')

# .listen() returns a generator over which you can iterate and listen for messages from publisher

for message in mobile.listen():
    print(message) # <-- you can literally do any thing with this message i am just printing it

