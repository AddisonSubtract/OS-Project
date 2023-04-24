import pygame
import socket
import pickle

# Alvin Zheng 001266528
# Addison Zheng 001266527

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.47"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def getPlayer(self):  # gets which player is playing
        return self.player

    def connect(self):  # connect players to server
        try:
            self.client.connect(self.addr)  # set client to connect to server
            return self.client.recv(2048).decode()  # get player ID
        except:
            pass

    def send(self, data):  # sends data to server
        try:
            self.client.send(str.encode(data))  # sends data to server
            return pickle.loads(self.client.recv(4096))  # receive info from server
        except socket.error as e:
            print(e)


# Window Screen
pygame.font.init()

width = 700
height = 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150

    def draw(self, window):  # draws buttons and text
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))  # draws rectangle
        font = pygame.font.SysFont("", 1)  # set font style and size
        text = font.render(self.text, 1, (72, 4, 115))  # set font color
        window.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2)
                           - round(text.get_height() / 2)))  # draws text and set text center

    def click(self, pos):  # check for location of clicks
        x1 = pos[0]  # get x of mouse
        y1 = pos[1]  # get y of mouse
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True  # if click was inside of button return true
        else:  # if click was not inside button return false
            return False


def redrawWindow(window, game, player):
    window.fill((72, 4, 115))
    bg = pygame.image.load("background.png")  # load background img
    rk = pygame.image.load("Rock.png")  # load rock img
    sc = pygame.image.load("Scissor.png")  # load scissor img
    pa = pygame.image.load("Paper.png")  # load paper img
    window.blit(bg, (0, 0))  # draw background

    if not (game.connected()):  # if both players are not connected draw "waiting for player"
        font = pygame.font.SysFont("", 80)
        text = font.render("Waiting", 1, (255, 0, 0), True)
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:  # both players are connected and draw text to screen
        font = pygame.font.SysFont("", 60)
        text = font.render("Player 1", 1, (0, 255, 0))
        window.blit(text, (380, 100))

        text = font.render("Player 2", 1, (255, 0, 0))
        window.blit(text, (380, 400))

        move1 = game.getMove(0)  # get move for player 1
        move2 = game.getMove(1)  # get move for player 2
        if game.bothPlayed():  # if both players made a move
            text1 = font.render(move1, 1, (255, 255, 255))  # set player 1 move as text 1
            text2 = font.render(move2, 1, (255, 255, 255))  # set player 2 move as text 2
        else:
            if game.p1Played and player == 0:  # if player 1 went and the client is player 1 and set text1 as move
                text1 = font.render(move1, 1, (255, 255, 255))  # draw player 1's move under your move
            else:  # player 1 has not made a move
                text1 = font.render("Waiting...", 1, (255, 255, 255))  # draw waiting under your move

            if game.p2Played and player == 1:  # if player 2 went and the client is player 2 and set text2 as move
                text2 = font.render(move2, 1, (255, 255, 255))  # draw player 2's move under your move
            else:  # player 2 has not made a move
                text2 = font.render("Waiting...", 1, (255, 255, 255))  # draw waiting under your move

        if player == 1:  # if the client is player 2
            window.blit(text2, (380, 200))  # text 2 is drawn under your move
            window.blit(text1, (380, 500))
        else:  # if client is player 1
            window.blit(text1, (380, 200))  # text 1 is drawn under your move
            window.blit(text2, (380, 500))  # text 2 is drawn under opponent move

        for btn in btns:  # draw every button to screen
            btn.draw(window)
        window.blit(rk, (50, 100))  # draw rock
        window.blit(sc, (50, 300))  # draw scissor
        window.blit(pa, (50, 500))  # draw paper
    pygame.display.update()  # update display


btns = [Button("Rock", 50, 100, (25, 171, 160)), Button("Scissors", 50, 300, (179, 204, 51)),
        Button("Paper", 50, 500, (226, 18, 44))]  # arguments for each button


def main():
    run = True
    clock = pygame.time.Clock()  # set up refresh rate
    n = Network()  # setup network
    player = int(n.getPlayer())  # set which player is playing
    print("You are player", player)  # tells client which player they are

    while run:
        clock.tick(60)  # refresh rate set to 60fps
        try:
            game = n.send("get")  # sends server "get"
        except:  # if get could not be sent
            run = False  # end loop
            print("Couldn't get game")
            break

        if game.bothPlayed():  # if both players have gone
            redrawWindow(window, game, player)  # redraw both clients
            pygame.time.delay(500)  # wait .5sec
            try:
                game = n.send("reset")  # send reset to server
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("", 150)
            if (game.getWinner() == 1 and player == 1) or (game.getWinner() == 0 and player == 0):  # check which player won
                # and if the client is that player
                text = font.render("You Won!", 1, (255, 0, 0), True)  # set text as won
            elif game.getWinner() == -1:  # if game was tied
                text = font.render("Tie Game!", 1, (255, 0, 0), True)  # set text as Tie
            else:  # if player did not win
                text = font.render("You Lost...", 1, (255, 0, 0), True)  # set text to Lost

            window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))  # draw text
            pygame.display.update()  # update display of player
            pygame.time.delay(5000)  # wait 2 sec for next loop

        for event in pygame.event.get():  # checks events in pygames
            if event.type == pygame.QUIT:  # if player clicks the X
                run = False  # set run to false and end loop
                pygame.quit()  # close game

            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed down
                pos = pygame.mouse.get_pos()  # gets x and y of mouse position
                for btn in btns:  # check all buttons
                    if btn.click(pos) and game.connected():  # if click was inside a button and game was connected
                        if player == 0:  # if player was player 1
                            if not game.p1Played:  # player 1 has not gone yet
                                n.send(btn.text)  # send text of the button to server as choice
                        else:
                            if not game.p2Played:  # player 2 has not gone yet
                                n.send(btn.text)  # send text of the button to server as choice

        redrawWindow(window, game, player)  # redraw window for each client


main()
