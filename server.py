import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.47"  # ip address of the server
port = 5555  # port number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket

try:
    s.bind((server, port))  # binds socket to ip and port
except socket.error as e:  # if binding does not work return error
    str(e)

s.listen(2)  # set socket to listen from 2 clients
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount  # counts number of players
    conn.send(str.encode(str(player)))  # sends players to client

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()  # receive data from client

            if gameId in games:  # checks which game is running
                game = games[gameId]  # set current game with gameID as game

                if not data:  # if data was not received, break
                    break
                else:
                    if data == "reset":  # if data was reset, reset Went for both player
                        game.resetWent()
                    elif data != "get":  # if data does not equal get, send if player has went
                        game.play(player, data)

                    conn.sendall(pickle.dumps(game))  # if not reset or get send player info to clients
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]  # delete game to make room for next game
        print("Closing Game", gameId)  # prints game that was closed
    except:
        pass
    idCount -= 1  # reduce player count
    conn.close()  # close socket


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
        player = 1  # sets current player as player 2

    start_new_thread(threaded_client, (conn, player, gameId))  # creates new thread for each player
