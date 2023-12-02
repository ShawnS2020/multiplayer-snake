from sense_hat import SenseHat
import time
import socketio

senseHat = SenseHat()
senseHat.clear()
socket = socketio.Client()

playerId = None
movX = 0
movY = 0

def trackMovement():
    global playerId
    global movX
    global movY
    while True:
        o = senseHat.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]

        if pitch > 20 and pitch < 270:
            movX = -1
            movY = 0
        elif pitch < 340 and pitch > 270:
            movX = 1
            movY = 0
        elif roll < 340 and roll > 270:
            movY = -1
            movX = 0
        elif roll > 20 and roll < 270:
            movY = 1
            movX = 0
        socket.emit('movement', { 'playerId': playerId, 'movX': movX, 'movY': movY })
        time.sleep(0.5)

@socket.event
def connect():
    print('Connected to the server')
    name = input("Enter your name: ")
    socket.emit('joinSlitherio', name)

@socket.on('playerId')
def setPlyaerId(newId):
    global playerId
    playerId = newId

@socket.on('startSlitherio')
def startGame():
    print('Game started')
    global playerId
    global movX
    global movY
    while True:
        o = senseHat.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]

        if pitch > 20 and pitch < 270:
            movX = -1
            movY = 0
        elif pitch < 340 and pitch > 270:
            movX = 1
            movY = 0
        elif roll < 340 and roll > 270:
            movY = -1
            movX = 0
        elif roll > 20 and roll < 270:
            movY = 1
            movX = 0
        socket.emit('movement', { 'playerId': playerId, 'movX': movX, 'movY': movY })
        time.sleep(0.05)

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