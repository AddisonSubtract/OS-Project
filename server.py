import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.46"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(player, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()  # set conn and addr to socket
    print("Connected to:", addr)  # prints what address it is connected to

    idCount += 1  # increment number of players
    player = 0  # sets player to player 1
    gameId = (idCount - 1) // 2  # sets gameID as # of players -1 / 2
    if idCount % 2 == 1:  # checks for odd number of players
        games[gameId] = Game(gameId)  # creates game for player without opponent
        print("Creating a new game...")
    else:  # if there are 2 players
        games[gameId].ready = True  # sets ready to true
        player = 1  # sets current player as palyer 2

    start_new_thread(threaded_client, (conn, player, gameId))  # creates new thread for each player
