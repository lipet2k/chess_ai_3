import chess.pgn
import chess
import pandas as pd
import numpy as np


# get the first 10k games of the desired result and the features of all moves- write them to the given filename
def get_first_10_result():
    pgn = open("../lichess_games_11_2021.pgn")
    # commenting this out so the file doesn't get rewritten
    count = 0


    df_features = pd.DataFrame()
    df_winner = pd.DataFrame()
    df_game_num = pd.DataFrame()

    current_game = chess.pgn.read_game(pgn)

    total = 1
    winner_color = 1


    while current_game is not None:
        result = current_game.headers['Result']
        flag = -1
        if result == "1-0":
            flag = 1
        elif result == "0-1":
            flag = 0
        # if given result found then assess game
        #
        if flag == winner_color and current_game.headers["Termination"] != "Abandoned":

            winner_color = not winner_color
            count += 1
            board = current_game.board()
            moves = current_game.mainline_moves()
            move_num = 0
            for move in moves:
                move_num += 1
                board.push(move)
                df_features[total]= get_features(board)
                df_winner[total] = [flag]
                total += 1
        if count == 10:
            df_features.to_excel("values_features.xlsx", sheet_name="Sheet1")
            df_winner.to_excel("values_winner.xlsx", sheet_name="Sheet1")
            break
        current_game = chess.pgn.read_game(pgn)

def get_features(board):
    # white pawn 0-63, white knight, bishop, rook, queen, king, then black pawn, first is 384
    # + 4 is castling rights + 1 is white turn/black turn + 2 is white checkmate / black checkmate
    features = np.array([0] * 15)
    mapping = board.piece_map()
    for square, piece in mapping.items():
        index = 0
        if not piece.color:
            index += 6
        # offset by the piece type * 64
        # add the corresponding square to the index
        index += piece.piece_type - 1

        features[index] = features[index] + 1

    

    # if it is whites turn
    if board.turn:
        features[12] = 1

    outcome = board.outcome()
    if outcome is not None:
        if outcome.winner is not None:
            if outcome.winner:
                features[13] = 1
            else:
                features[14] = 1

    return features
get_first_10_result()