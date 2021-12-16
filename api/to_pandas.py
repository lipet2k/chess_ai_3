import chess.pgn
import chess
import pandas as pd
import numpy as np

piece_type_offset = dict()
piece_type_offset[1] = 0
piece_type_offset[2] = 64
piece_type_offset[3] = 128
piece_type_offset[4] = 192
piece_type_offset[5] = 256
piece_type_offset[6] = 320

# get the first 10k games of the desired result and the features of all moves- write them to the given filename
def get_first_10_result():
    pgn = open("../lichess_games_11_2021.pgn")
    # commenting this out so the file doesn't get rewritten
    count = 0


    df_features = pd.DataFrame()
    df_winner = pd.DataFrame()
    df_game_num = pd.DataFrame()

    current_game = chess.pgn.read_game(pgn)

    total_odd = 1
    total_even = 2
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
            if flag:
                total = total_odd
            else:
                total = total_even

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
                total += 2

            if flag:
                total_odd = total
            else:
                total_even = total
        if count == 1000:
            if total_even > total_odd + 1:
                df_features = df_features.drop([x for x in range(total_odd+1, total_even) if x%2 == 0], axis=1)
                df_winner = df_winner.drop([x for x in range(total_odd+1, total_even) if x%2 == 0], axis=1)
            elif total_even < total_odd - 1:
                df_features = df_features.drop([x for x in range(total_even+1, total_odd) if x%2 == 1], axis=1)
                df_winner = df_winner.drop([x for x in range(total_even+1, total_odd) if x%2 == 1], axis=1)

            df_features.sort_index(axis=1, inplace=True)
            df_winner.sort_index(axis=1, inplace=True)
            df_features.to_excel("1000_games_features.xlsx", sheet_name="Sheet1")
            df_winner.to_excel("1000_games_winner.xlsx", sheet_name="Sheet1")
            break
        current_game = chess.pgn.read_game(pgn)

def get_features(board):
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
get_first_10_result()