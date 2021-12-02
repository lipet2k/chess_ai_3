import math
import chess
import random


class Agent:
    def __init__(self, board):
        self.board = board

    def getValue(self, outcome):
        if outcome is None:
            return (self.getValueColor(chess.WHITE) - self.getValueColor(chess.BLACK)) * self.getColor()
        else:
            winner = outcome.winner
            if winner is None:
                return 0
            colorIsNotWinner = winner ^ self.board.turn
            return (1 - colorIsNotWinner) * 999 + colorIsNotWinner * -999

    def getValueColor(self, color):
        return len(self.board.pieces(1, color)) + (
                    len(self.board.pieces(2, color)) + len(self.board.pieces(3, color))) * 3 + len(
            self.board.pieces(4, color)) * 5 + len(self.board.pieces(5, color)) * 9

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


class GeneralizedFeatures(Agent):
    def __init__(self, board):
        super().__init__(board)
        self.color = self.board.turn
        # if > 26 pieces its early game
        self.early_cutoff = 26
        # if > 10 pieces its midgame
        self.mid_cutoff = 10

        self.center = [10, 11, 12, 13, 18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37]
        self.b_Left = [0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27]
        self.b_Right = [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31]
        self.t_Left = [32, 33, 34, 35, 40, 41, 42, 43, 48, 49, 50, 51, 56, 57, 58, 59]
        self.t_Right = [36, 37, 38, 39, 44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63]

    def bestAction(self, depth, alpha, beta):
        return None

    # 0 = center        = [10,11,12,13, 18,19,20,21,    26,27,28,29,    34,35,36,37]
    # 1 is bottom left  = [0,1,2,3,     8,9,10,11,      16,17,18,19,    24,25,26,27]
    # 2 is bottom right = [4,5,6,7,     12,13,14,15,    20,21,22,23,    28,29,30,31]
    # 3 is top left     = [32,33,34,35, 40,41,42,43,    48,49,50,51,    56,57,58,59]
    # 4 is top right    = [36,37,38,39, 44,45,46,47,    52,53,54,55,    60,61,62,63]

    def piecesInAreas(self, color):

        gamestate = None
        num_pieces = len(self.board.pieces)

        if num_pieces > self.early_cutoff:
            gamestate = 0
        elif num_pieces > self.mid_cutoff:
            gamestate = 1
        else:
            gamestate = 2

        #               knights                 bishops rooks queen king
        #     /     /       |      \    \
        # center, bleft, bright, tleft, tright
        #   / | \
        # early  middle, endgame  ...
        # 0-2 early middle end knights in center, 3-5 early middle end knights in bleft, etc

        # index conversion:
        # ((piece type - 2) * 15) + (quadrant index * 3) + gamestate

        output = [0] * 75
        for i in range(64):
            # get the current piece
            current = self.board.piece_at(i)
            # if it is a piece and it is the right color
            if current is not None and current.color == color and current.piece_type in range(2,7):
                pieceindex = current.piece_type - 2

                if i in self.center:
                    feature_index = (pieceindex * 15) + 0 + gamestate
                    output[feature_index] = output[feature_index] + 1

                if i in self.b_Left:
                    quadrant_index = 1
                elif i in self.b_Right:
                    quadrant_index = 2
                elif i in self.t_Left:
                    quadrant_index = 3
                elif i in self.t_Right:
                    quadrant_index = 4

                # quadrant index should always be initialized as long as those 4 lists were made properly
                feature_index = (pieceindex * 15) + (quadrant_index * 3) + gamestate
                output[feature_index] = output[feature_index] + 1

        return tuple(output)

    def printAreas(self, tuple):

        gamestate = None
        num_pieces = len(self.board.pieces)

        if num_pieces > self.early_cutoff:
            gamestate = 0
        elif num_pieces > self.mid_cutoff:
            gamestate = 1
        else:
            gamestate = 2

        for i in range(75):
            if i % 3 == gamestate:
                if i < 15:
                    print("knights in")

                elif i < 30:
                    print("bishops in")
                elif i < 45:
                    print("rooks in")
                elif i < 60:
                    print("queens in")
                elif i < 75:
                    print("kings in")

                if i % 5 == 0:
                    print("center is", tuple[i])
                if i % 5 == 1:
                    print("bottom left is", tuple[i])
                if i % 5 == 2:
                    print("bottom right is", tuple[i])
                if i % 5 == 3:
                    print("top left is", tuple[i])
                if i % 5 == 4:
                    print("top right is", tuple[i])

    def number_of_attacking_squares(self, color):

        # knight, bishop, rook, queen
        # decided to count two pieces attacking one square as 1
        attacksets = [set()] * 4
        output = [] * 4
        modifier = len(self.board.pieces) / 32.00

        for i in range(64):
            # get the current piece
            current = self.board.piece_at(i)

            # if it is a piece and it is the right color
            if current is not None and current.color == color and current.piece_type in range(2,7):
                pieceindex = current.piece_type - 2

                for square in self.board.attacks():
                    attacksets[pieceindex].add(square)

        output[pieceindex] = len(attacksets[pieceindex]) * modifier

        return tuple(output)

    def pawn_chains_count(self, color):

        num_chains = 0
        connected_pawns = 0

        # TODO
