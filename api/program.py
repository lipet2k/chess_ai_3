import math
import chess
import random
import pandas as pd
import numpy as np


class EvaluationFunctions:
    def __init__(self, board):
        self.board = board

    # returns classic- number of pieces * their point value {1,3,5,9}
    def pieceValues(self, color):
        return len(self.board.pieces(1, color)) + (
                len(self.board.pieces(2, color)) + len(self.board.pieces(3, color))) * 3 + len(
            self.board.pieces(4, color)) * 5 + len(self.board.pieces(5, color)) * 9

    # returns sum of (piece value * #(ranks away from their side))
    def pushValuablePeices(self, color):
        knights = self.board.pieces(chess.KNIGHT, color)
        bishops = self.board.pieces(chess.BISHOP, color)
        rooks = self.board.pieces(chess.ROOK, color)
        queens = self.board.pieces(chess.QUEEN, color)
        pawns = self.board.pieces(chess.PAWN, color)

        value = self.pushPiecesHelper(color, knights, bishops, rooks, queens, pawns)

        return value

    # return the number of total attacks made by this color
    def numAttacks(self, color):
        knights = self.board.pieces(chess.KNIGHT, color)
        bishops = self.board.pieces(chess.BISHOP, color)
        rooks = self.board.pieces(chess.ROOK, color)
        queens = self.board.pieces(chess.QUEEN, color)
        pawns = self.board.pieces(chess.PAWN, color)

        numAttacks = self.numAttacksHelper(knights, bishops, rooks, queens, pawns, 1, 1, 1, 1, 1)
        return numAttacks

    def pieceValuesAndMakeAttacks(self, color):
        return self.numAttacks(color) * 0.2 + self.pieceValues(color)

    # return the push pieces evaluation function times some modifier plus the num attacks evaluation function
    def pushValuablePeicesAndMakeAttacks(self, color):
        knights = self.board.pieces(chess.KNIGHT, color)
        bishops = self.board.pieces(chess.BISHOP, color)
        rooks = self.board.pieces(chess.ROOK, color)
        queens = self.board.pieces(chess.QUEEN, color)
        pawns = self.board.pieces(chess.PAWN, color)

        pushPiecesValue = self.pushPiecesHelper(color, knights, bishops, rooks, queens, pawns)
        numAttacks = self.numAttacksHelper(knights, bishops, rooks, queens, pawns, 1, 1, 1, 1, 1)

        value = (pushPiecesValue * .2) + (numAttacks)
        return value

    # given the lists of pieces, for each piece add its value times its current rank to the score
    def pushPiecesHelper(self, color, knights, bishops, rooks, queens, pawns):
        value = 0
        multiplier = 1
        rankdiff = 7

        if color == chess.WHITE:
            multiplier = 1
            rankdiff = 1
        elif color == chess.BLACK:
            multiplier = -1
            rankdiff = 8

        for square in knights:
            value += ((multiplier * chess.square_rank(square)) + rankdiff) * 3
        for square in bishops:
            value += ((multiplier * chess.square_rank(square)) + rankdiff) * 3
        for square in rooks:
            value += ((multiplier * chess.square_rank(square)) + rankdiff) * 5
        for square in queens:
            value += ((multiplier * chess.square_rank(square)) + rankdiff) * 9
        for square in pawns:
            value += ((multiplier * chess.square_rank(square)) + rankdiff) * 1

        return value

    # for each list of pieces, add the number of squares being attacked by those pieces times the modifier to the score
    # allows it to value pawn attacks greater than queen for example
    def numAttacksHelper(self, knights, bishops, rooks, queens, pawns, knightMod, bishMod, rookMod, queenMod, pawnMod):
        numAttacks = 0

        # for each piece of type x, return the number of squares they are attacking mult by the corresponding mod
        for square in knights:
            numAttacks += len(self.board.attacks(square)) * knightMod
        for square in bishops:
            numAttacks += len(self.board.attacks(square)) * bishMod
        for square in rooks:
            numAttacks += len(self.board.attacks(square)) * rookMod
        for square in queens:
            numAttacks += len(self.board.attacks(square)) * queenMod
        for square in pawns:
            numAttacks += len(self.board.attacks(square)) * pawnMod

        return numAttacks



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

        evalfunc = EvaluationFunctions(self.board)
        return evalfunc.pieceValuesAndMakeAttacks(color)

        # return len(self.board.pieces(1, color)) + (
        #             len(self.board.pieces(2, color)) + len(self.board.pieces(3, color))) * 3 + len(
        #     self.board.pieces(4, color)) * 5 + len(self.board.pieces(5, color)) * 9

    def getColor(self):
        if self.board.turn:
            return 1
        else:
            return -1

class LogisticRegression(Agent):
    def __init__(self, board):
        super().__init__(board)
        weights = pd.read_excel("final_weights_10_games_10_batch.xlsx", "Sheet1")
        self.weights = weights[815]

        bias = 0.605043
        self.bias_weight = bias
    def bestAction(self):
        outcome = self.board.outcome()
        if outcome != None:
            return (self.getValue(outcome), None)
        
        if self.board.turn:
            best_action = []
            base = -math.inf
            for move in self.board.legal_moves:
                self.board.push(move)
                features = self.get_features(self.board)
                self.board.pop()
                total_sum = self.total_sum(features)
                if total_sum > base:
                    base = total_sum
                    best_action = [move]
                elif total_sum == base:
                    best_action.append(move)

        else:
            best_action = []
            base = math.inf
            for move in self.board.legal_moves:
                self.board.push(move)
                features = self.get_features(self.board)
                self.board.pop()
                total_sum = self.total_sum(features)
                if total_sum < base:
                    base = total_sum
                    best_action = [move]
                elif total_sum == base:
                    best_action.append(move)
        return base, random.choice(best_action)
                

    def total_sum(self, features):
        return self.sigmoid(self.bias_weight + np.dot(features, self.weights))

    def sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-z))
    
    def get_features(self, board):

        piece_type_offset = dict()
        piece_type_offset[1] = 0
        piece_type_offset[2] = 64
        piece_type_offset[3] = 128
        piece_type_offset[4] = 192
        piece_type_offset[5] = 256
        piece_type_offset[6] = 320
        # white pawn 0-63, white knight, bishop, rook, queen, king, then black pawn, first is 384
        # + 4 is castling rights + 1 is white turn/black turn + 2 is white checkmate / black checkmate
        features = np.array([0] * (768 + 4 + 1 + 2))
        mapping = board.piece_map()
        for square, piece in mapping.items():
            index = 0
            if not piece.color:
                index += 384
            # offset by the piece type * 64
            # add the corresponding square to the index
            index += piece_type_offset[piece.piece_type] + square

            features[index] = 1

        # assign castling rights features
        castling_rights = board.castling_rights
        features[768] = castling_rights >> 0 & 1
        features[769] = castling_rights >> 7 & 1
        features[770] = castling_rights >> 56 & 1
        features[771] = castling_rights >> 63 & 1

        # if it is whites turn
        if board.turn:
            features[772] = 1

        outcome = board.outcome()
        if outcome is not None:
            if outcome.winner is not None:
                if outcome.winner:
                    features[773] = 1
                else:
                    features[774] = 1

        return features





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


class QLearningAgent(Agent):
    def __init__(self, board):
        # if pieces > 26, early game
        super().__init__(board)
        EARLY = 26
        # if 26 > pieces > 10, midgame
        MID = 10

        CENTER = [18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]
        BOT_LEFT = [0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 25, 25]

class GeneralizedFeatures(Agent):
    def __init__(self, board):
        super().__init__(board)
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

    def piece_pins(self, color):
        pass
