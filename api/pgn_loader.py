import chess.pgn

pgn = open("../lichess_games_11_2021.pgn")

first_game = chess.pgn.read_game(pgn)
board = first_game.board()
moves = first_game.mainline_moves()

print(first_game.mainline_moves())

for move in first_game.mainline_moves():
    board.push(move)
    print(move)