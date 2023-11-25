from sense_hat import SenseHat
import time
import socketio

senseHat = SenseHat()
senseHat.clear()
socket = socketio.Client()

@socket.event
def connect():
    print('Connected to the server')
    name = input("Enter your name: ")
    socket.emit('joinGame', name)

@socket.on('startGame')
def startGame():
    print('Game started')

@socket.on('getMovement')
def getMovement(snakeMovementDelay):
    movement = "none"

    for i in range(0, round(snakeMovementDelay / .05)):
        o = senseHat.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]

        if pitch > 20 and pitch < 270 and movementX != 1:
            movement = "left"
        elif pitch < 340 and pitch > 270 and movementX != -1:
            movement = "right"
        elif roll < 340 and roll > 270 and movementY != 1:
            movement = "up"
        elif roll > 20 and roll < 270 and movementY != -1:
            movement = "down"
        time.sleep(.05)

    socket.emit('sendMovement', movement)

while True:
    isMediator = input("Is your Pi connected to the internet? (y/n): ")
    if (isMediator == 'y'):
        ip = input("Please enter the server IP you wish to connect to (leave blank for default server):")
        if ip == '':
            url = 'http://35.209.28.30:3000'
        else:
            url = 'http://' + ip + ':3000'
        #url = 'http://35.223.19.176:3000/'
        print(url)
        break
    elif (isMediator == 'n'):
        url = 'http://localhost:3000'
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

try:
    socket.connect(url)
    socket.wait()
except:
    print("Could not connect to the server")
    exit()
