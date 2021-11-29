import math
import chess
import random

class Agent:
    def __init__(self, board):
        self.board = board
    
    def getValue(self, outcome):
        if outcome is None:
            return (self.getValueColor(chess.WHITE) - self.getValueColor(chess.BLACK))*self.getColor()
        else:
            winner = outcome.winner
            if winner is None:
                return 0
            colorIsNotWinner = winner^self.board.turn
            return (1 - colorIsNotWinner)*999 + colorIsNotWinner*-999
            
    def getValueColor(self, color):
        return len(self.board.pieces(1, color)) + (len(self.board.pieces(2, color))+len(self.board.pieces(3, color)))*3 + len(self.board.pieces(4, color))*5 + len(self.board.pieces(5, color))*9

    def getColor(self):
        if self.board.turn:
            return 1
        else:
            return -1


class MiniMaxAgent(Agent):
    def __init__(self, board):
        super().__init__(board)
    
    def bestAction(self, depth):
        outcome = self.board.outcome()
        if depth == 0 or outcome != None:
            return (self.getValue(outcome), None)
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

class MiniMaxAlphaBetaAgent(Agent):
    def __init__(self, board):
        super().__init__(board)

    def bestAction(self, depth, alpha, beta):
        outcome = self.board.outcome()
        if depth == 0 or outcome != None:
            return (self.getValue(outcome), None)
        max = -math.inf
        best_moves = []
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.bestAction(depth - 1, -beta, -alpha)[0]
            self.board.pop()
            if (score > max):
                best_moves = [move]
                max = score
            elif score == max:
                best_moves.append(move)
            if alpha >= beta:
                break
        return max, random.choice(best_moves)