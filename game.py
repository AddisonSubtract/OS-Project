class Game:
    def __init__(self, id):
        self.p1Played = False  # check if player 1 made a move
        self.p2Played = False  # check if player 2 made a move
        self.ready = False  # check if game is ready
        self.id = id  # ID for player
        self.moves = [None, None]  # first int is move for player 1, second int is move for player 2

    def getMove(self, player):  # gets the move for specified player
        return self.moves[player]

    def play(self, player, move):  # checks if player has made a move
        self.moves[player] = move  # sets the move of the player as the input
        if player == 0:  # checks if the player was player 1
            self.p1Played = True  # set that player 1 has made a move
        else:  # default to player 2 if not player 1
            self.p2Played = True  # set that player 2 has made a move

    def connected(self):  # checks if both players are connected
        return self.ready

    def bothPlayed(self):  # check if both players made a move
        return self.p1Played and self.p2Played  # return values for p1Played and p2Played

    def winner(self):  # checks for winner

        p1 = self.moves[0].upper()[0]  # grab move for player 1 and turn the move to uppercase
        p2 = self.moves[1].upper()[0]  # grab move for player 2 and turn the move to uppercase

        winner = -1  # default winner to -1 for tied
        # player 1 wins if winner = 0, player 2 wins if winner = 1
        if p1 == "R" and p2 == "S":  # p1 rock vs p2 scissor
            winner = 0  # player 1 wins
        elif p1 == "S" and p2 == "R":  # p1 scissor vs p2 rock
            winner = 1  # player 2 wins
        elif p1 == "P" and p2 == "R":  # p1 paper vs p2 rock
            winner = 0  # player 1 wins
        elif p1 == "R" and p2 == "P":  # p1 rock vs p2 paper
            winner = 1  # player 2 wins
        elif p1 == "S" and p2 == "P":  # p1 scissor vs p2 paper
            winner = 0  # player 1 wins
        elif p1 == "P" and p2 == "S":  # p1 paper vs p2 scissor
            winner = 1  # player 2 wins
        return winner

    def resetWent(self):  # resets Went for both players for next game
        self.p1Played = False
        self.p2Played = False
