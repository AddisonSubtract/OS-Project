import pygame
import socket
import pickle


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
            return self.client.recv(2048).decode()  # get
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
        self.height = 100

    def draw(self, window):  # draws buttons and text
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))  # draws rectangle
        font = pygame.font.SysFont("", 40)  # set font style and size
        text = font.render(self.text, 1, (255, 255, 255))  # set font color
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
    window.fill((128, 128, 128))

    if not (game.connected()):  # if both players are not connected draw "waiting for player"
        font = pygame.font.SysFont("", 80)
        text = font.render("Waiting for Player", 1, (255, 0, 0), True)
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:  # both players are connected and draw text to screen
        font = pygame.font.SysFont("", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        window.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)  # get move for player 1
        move2 = game.get_player_move(1)  # get move for player 2
        if game.bothWent():  # if both players made a move
            text1 = font.render(move1, 1, (0, 0, 0))  # set player 1 move as text 1
            text2 = font.render(move2, 1, (0, 0, 0))  # set player 2 move as text 2
        else:
            if game.p1Went and player == 0:  # if player 1 went and the client is player 1 and set text1 as move
                text1 = font.render(move1, 1, (0, 0, 0))  # draw player 1's move under your move
            elif game.p1Went:  # if player 1 went and client is not player 1 and set text1 as Locked in
                text1 = font.render("Locked In", 1, (0, 0, 0))  # draw player 1's move under opponent move
            else:  # player 1 has not made a move
                text1 = font.render("Waiting...", 1, (0, 0, 0))  # draw waiting under your move

            if game.p2Went and player == 1:  # if player 2 went and the client is player 2 and set text2 as move
                text2 = font.render(move2, 1, (0, 0, 0))  # draw player 2's move under your move
            elif game.p2Went:  # if player 2 went and client is not player 2 and set text2 as Locked in
                text2 = font.render("Locked In", 1, (0, 0, 0))  # draw player 2's move under opponent move
            else:  # player 2 has not made a move
                text2 = font.render("Waiting...", 1, (0, 0, 0))  # draw waiting under your move

        if player == 1:  # if the client is player 2
            window.blit(text2, (100, 350))  # text 2 is drawn under your move
            window.blit(text1, (400, 350))
        else:  # if client is player 1
            window.blit(text1, (100, 350))  # text 1 is drawn under your move
            window.blit(text2, (400, 350))  # text 2 is drawn under opponent move

        for btn in btns:  # draw every button to screen
            btn.draw(window)

    pygame.display.update()  # update display


btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),
        Button("Paper", 450, 500, (0, 255, 0))]  # arguments for each button


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

        if game.bothWent():  # if both players have gone
            redrawWindow(window, game, player)  # redraw both clients
            pygame.time.delay(500)  # wait .5sec
            try:
                game = n.send("reset")  # send reset to server
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):  # check which player won
                # and if the client is that player
                text = font.render("You Won!", 1, (255, 0, 0))  # set text as won
            elif game.winner() == -1:  # if game was tied
                text = font.render("Tie Game!", 1, (255, 0, 0))  # set text as Tie
            else:  # if player did not win
                text = font.render("You Lost...", 1, (255, 0, 0))  # set text to Lost

            window.blit(text, (width / 2 - text.get_width() / 2, height / 8 - text.get_height() / 8))  # draw text
            pygame.display.update()  # update display of player
            pygame.time.delay(2000)  # wait 2 sec for next loop

        for event in pygame.event.get():  # checks events in pygames
            if event.type == pygame.QUIT:  # if player clicks the X
                run = False  # set run to false and end loop
                pygame.quit()  # close game

            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed down
                pos = pygame.mouse.get_pos()  # gets x and y of mouse position
                for btn in btns:  # check all buttons
                    if btn.click(pos) and game.connected():  # if click was inside a button and game was connected
                        if player == 0:  # if player was player 1
                            if not game.p1Went:  # player 1 has not gone yet
                                n.send(btn.text)  # send text of the button to server as choice
                        else:
                            if not game.p2Went:  # player 2 has not gone yet
                                n.send(btn.text)  # send text of the button to server as choice

        redrawWindow(window, game, player)  # redraw window for each client


main()
