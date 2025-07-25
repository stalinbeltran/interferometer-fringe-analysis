
from gpiozero import Button
from signal import pause

cont = 0
def say_hello():
    global cont
    cont +=1
    print("Hello! " + str(cont))

button = Button(26)

button.when_pressed = say_hello

pause()
