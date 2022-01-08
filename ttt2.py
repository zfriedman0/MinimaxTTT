#Board design adapted from https://github.com/kying18/tic-tac-toe/blob/master/game.py
#Minimax adapted from https://athena.ecs.csus.edu/~gordonvs/Beijing/Minimax.pdf
#Pruning adapted from https://www.cs.swarthmore.edu/~meeden/cs63/f05/minimax.html

import math
import random
 
MAX = 'X'
MIN = 'O'
EMPTY = ' '

class Board():
    def __init__(self):
        self.board = self.MakeBoard() #a board state, initialized empty
        self.winner = None #game winner, neither MAX nor MIN at game start

    def MakeBoard(self): #returns a set of nine space chars, zero-indexed
        return [EMPTY for _ in range(9)]

    def PrintBoard(self): #pretty-prints the game state
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def CheckWinner(self):
        #check rows: top, middle, bottom
        #if all three squares match (and aren't empty) set winner to char at first checked element, return winner
        if(self.board[0] == self.board[1] and self.board[0] == self.board[2] and self.board[0] != EMPTY):
            self.winner = self.board[0]
            return self.winner
        elif(self.board[3] == self.board[4] and self.board[3] == self.board[5] and self.board[3] != EMPTY):
            self.winner = self.board[3]
            return self.winner
        elif(self.board[6] == self.board[7] and self.board[6] == self.board[8] and self.board[6] != EMPTY):
            self.winner = self.board[6]
            return self.winner

        #check columns: left, middle, right
        elif(self.board[0] == self.board[3] and self.board[0] == self.board[6] and self.board[0] != EMPTY):
            self.winner = self.board[0]
            return self.winner
        elif(self.board[1] == self.board[4] and self.board[1] == self.board[7] and self.board[1] != EMPTY):
            self.winner = self.board[1]
            return self.winner
        elif(self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != EMPTY):
            self.winner = self.board[2]
            return self.winner

        #check left-down diagonal
        elif(self.board[0] == self.board[4] and self.board[0] == self.board[8] and self.board[0] != EMPTY):
            self.winner = self.board[0]
            return self.winner
        #check left-up diagonal
        elif(self.board[2] == self.board[4] and self.board[2] == self.board[6] and self.board[2] != EMPTY):
            self.winner = self.board[2]
            return self.winner
        else:
            return False

    def CheckDraw(self): #a draw occurs if there are no more legal moves on the board
        if len(self.GetLegal()) == 0:
            return True
        return False

    def CheckLegal(self, move):
        move = int(move)
        if self.board[move] == EMPTY:
            return True
        else:
            return False

    def MakeMove(self, input, isMax): #check that a given input is legal, change board from EMPTY to MAX or MIN depending on isMax
        if self.CheckLegal(input) and isMax:
            self.board[input] = MAX
            print("\nMax made a move.")
            self.PrintBoard()
            if self.CheckWinner() == MAX:
                print("\nMAX wins!")
                self.PrintBoard()
                exit()
            elif self.CheckDraw():
                print("\nDraw!")
                self.PrintBoard()
                exit()
        elif self.CheckLegal(input) and not isMax:
            self.board[input] = MIN
            if self.CheckWinner() == MIN:
                print("\nMIN wins!")
                self.PrintBoard()
                exit()
            elif self.CheckDraw():
                print("\nDraw!")
                self.PrintBoard()
                exit()
        return self.board

    def GetLegal(self): #return a list of legal moves on the board
        return [i for i, j in enumerate(self.board) if j == EMPTY]

    def GetNumeric(self): #print the board with moves numbered
        numbered = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in numbered:
            print('| ' + ' | '.join(row) + ' |')

class Min():
    def __init__(self):
        pass
    
    def GetMove(self, game):
        valid = False

        while not valid:
            move = input("\nInput a move on the board (0-8): ")
            try:
                move = int(move)
                if move not in game.GetLegal():
                    raise ValueError   
                valid = True
            except ValueError:
                print("\nBad move. Try again...")
        return move

class AutoMin():
    def __init__(self):
        pass

    def GetMove(self, game):
        return random.choice(game.GetLegal())

class Max():
    def __init__(self):
        pass

    def GetMove(self, game):
        return self.Minimax(game)


    def Utility(self, game):
        if game.CheckWinner() == MAX:
            return 1
        elif game.CheckWinner() == MIN:
            return -1
        elif game.CheckDraw() == True:
            return 0

    def Maximizer(self, game, alpha, beta):
        if game.CheckWinner() != False:
            return self.Utility(game)
        else:
            bestScore = -9999
            bestMove = -1

            for move in game.GetLegal():
                game.board[move] = MAX
                score = self.Minimizer(game, alpha, beta)
                if score > bestScore:
                    bestMove = move
                    bestScore = score
                game.board[move] = EMPTY
                alpha = max(alpha, bestScore)

                if beta <= alpha: #if beta is less than alpha, 
                    return alpha

                #print("Max Move: ", move, "Alpha: ", alpha, "Beta: ", beta)
            return bestScore

    def Minimizer(self, game, alpha, beta):
        if game.CheckWinner() != False:
            return self.Utility(game)
        else:
            bestScore = 9999
            bestMove = -1

            for move in game.GetLegal():
                game.board[move] = MIN
                score = self.Maximizer(game, alpha, beta)
                if score < bestScore:
                    bestMove = move
                    bestScore = score
                game.board[move] = EMPTY
                beta = min(beta, bestScore)

                if beta <= alpha:
                    return beta

                #print("Min Move: ", move, "Alpha: ", alpha, "Beta: ", beta)
            return bestScore

    def Minimax(self, game):
        bestMove = -1
        bestScore = -9999

        for move in game.GetLegal():
            game.board[move] = MAX
            score = self.Minimizer(game, -math.inf, math.inf)
            if score > bestScore:
                bestMove = move
                bestScore = score
            game.board[move] = EMPTY
        return bestMove


newBoard = Board()
newMin = Min()
newAutoMin = AutoMin()
newMax = Max()

print("\nTo play, enter a number (0-8) to choose an open space when it's your turn.")
newBoard.GetNumeric()

while not newBoard.CheckWinner() or not newBoard.CheckDraw():
    newBoard.MakeMove(newMax.GetMove(newBoard), True)
    newBoard.MakeMove(newMin.GetMove(newBoard), False)
    newBoard.PrintBoard()