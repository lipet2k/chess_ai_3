import math
import chess
import random

class Agent:
    def __init__(self, board):
        self.board = board
        self.color = chess.WHITE
    
    def getValue(self, outcome):

        if outcome is None:
            player_1 = self.getColor(chess.WHITE)
            player_2 = self.getColor(chess.BLACK)
            return player_1 - player_2
        else:
            winner = outcome.winner
            if winner is None:
                return 0
            num = self.color
            if num is -1:
                num = 0
            colorIsNotWinner = winner^num
            return (1 - colorIsNotWinner)*999 + colorIsNotWinner*-999
            

    def getColor(self, color):
        return len(self.board.pieces(1, color)) + (len(self.board.pieces(2, color))+len(self.board.pieces(3, color)))*3 + len(self.board.pieces(4, color))*5 + len(self.board.pieces(5, color))*9
    
    def swap(self):
        self.color = -self.color

    def setColor(self, color):
        self.color = color

class MiniMaxAgent(Agent):
    def __init__(self, board):
        super().__init__(board)

    def bestAction(self, depth):
        outcome = self.board.outcome()
        if depth == 0 or outcome != None:
            return (self.getValue(outcome) * self.color, None)
        max = -math.inf
        best_moves = []
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.bestAction(depth - 1)[0]
            self.board.pop()
            if (score > max):
                best_moves = [move]
                max = score
            elif score == max:
                best_moves.append(move)
        return max, random.choice(best_moves)






