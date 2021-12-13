from flask import Flask, render_template, url_for, request, redirect, Markup
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields

import chess
import chess.svg
import math
from program import MiniMaxAgent, MiniMaxAlphaBetaAgent

app = Flask(__name__)
api = Api(app)

board = chess.Board()
agent = MiniMaxAlphaBetaAgent(board)

def renderBoard():
    return chess.svg.board(board, size=500)

board_fields = {
    'board': fields.String,
    'value': fields.Integer
}

class Board(object):
    def __init__(self, board, value):
        self.board = board
        self.value = value

def play(depth):
    best_action = agent.bestAction(depth, -math.inf, math.inf)
    best_value = best_action[0]
    best_move = best_action[1]
    if best_move is None:
        if agent.board.turn == False:
            return "White wins!"
        else:
            return "Black wins!"
    else:
        board.push(best_move)
        return Board(board.fen(), best_value)

class Initialize(Resource):
    @marshal_with(board_fields)
    def get(self):
        try:
            # thisIs = type(Board(Markup(renderBoard()), 0))
            return Board(board.fen(), 0)
        except:
            abort(404, message="Fail to initialize.")

class Reset(Resource):
    @marshal_with(board_fields)
    def get(self):
        try:
            board.reset()
            return Board(board.fen(), 0)
        except:
            abort(404, message="Fail to reset.")

class Next(Resource):
    @marshal_with(board_fields)
    def get(self):
        try:
            return play(2)
        except:
            abort(404, message="Fail to get next move.")

class Previous(Resource):
    @marshal_with(board_fields)
    def get(self):
        try:
            board.pop()
            return Board(board.fen(), 0)
        except:
            abort(404, message="Fail to undo move.")            

api.add_resource(Next, '/next')
api.add_resource(Reset, '/reset')
api.add_resource(Initialize, '/')
api.add_resource(Previous, '/previous')

if __name__ == "__main__":
    app.run(debug=True)
