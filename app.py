from flask import Flask, render_template, url_for, request, redirect, Markup

import chess
import chess.svg
import time
from program import MiniMaxAgent
from enum import Enum

app = Flask(__name__)

board = chess.Board()
agent = MiniMaxAgent(board)

def renderBoard(value):
    new_image = chess.svg.board(board, size=500)
    return render_template("index.html", new_image = Markup(new_image), value=value)

def play(depth):
    best_action = agent.bestAction(depth)
    best_value = best_action[0]
    best_move = best_action[1]
    if best_move is None:
        return str(agent.color) + " wins!"
    else:
        board.push(best_move)
        agent.swap()
        return renderBoard(best_value)

@app.route('/')
def init():
    return renderBoard(0)

@app.route('/reset', methods=['GET'])
def reset():
    try: 
        board.reset()
        agent.setColor(chess.WHITE)
        return renderBoard(0)
    except:
        return "Error when resetting"

@app.route('/next', methods=['GET'])
def nextMove():
    # try:
        return play(2)
    # except:
    #     return "Error when processing the move"


if __name__ == "__main__":
    app.run(debug=True)
