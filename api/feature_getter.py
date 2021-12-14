import numpy as np
import chess.pgn

piece_type_offset = dict()
piece_type_offset[1] = 0
piece_type_offset[2] = 64
piece_type_offset[3] = 128
piece_type_offset[4] = 192
piece_type_offset[5] = 256
piece_type_offset[6] = 320

def file_to_arrays(winfilename, lossfilename, totalgames):
    features_set = np.array([0] * 775)
    winfile = open(winfilename)
    winlines = winfile.readlines()
    lossfile = open(lossfilename)
    losslines = lossfile.readlines()
    results = []
    gamecount = 0

    for row in range(len(winlines) + len(losslines)):
        if row % 2 == 0:
            line = winlines[int(row/2)]
        else:
            line = losslines[int(row/2)]
        tokens = line.split(":")
        if "Game" in tokens[0]:
            if gamecount == totalgames + 1:
                break
            gamecount = gamecount + 1
            print("games read: " + str(gamecount))
        elif "1-0" == tokens[0]:
            results.append(1)
            values = tokens[2]
            values = values.replace("[", "")
            values = values.replace("]\n", "")
            values = values.split(", ")
            for i in range(len(values)):
                values[i] = int(values[i])
            features_set = np.vstack([features_set, values])
        elif "0-1" == tokens[0]:
            results.append(0)
            values = tokens[2]
            values = values.replace("[", "")
            values = values.replace("]\n", "")
            values = values.split(", ")
            for i in range(len(values)):
                values[i] = int(values[i])
            features_set = np.vstack([features_set, values])
        if row % 1000 == 0:
            print("now loaded " + str(row) + " positions" + str())
    features_set = np.delete(features_set, 0, 0)
    print("got " + str(gamecount) + " games. " + str(len(results)) + " positions loeaded")
    return (results, features_set)


# get the first 10k games of the desired result and the features of all moves- write them to the given filename
def get_first_10k_result(desired_result, filename):
    pgn = open("./lichess_games_11_2021.pgn")
    # commenting this out so the file doesn't get rewritten
    # file = open(filename, "w")
    count = 0
    current_game = chess.pgn.read_game(pgn)
    while current_game is not None:
        current_game = chess.pgn.read_game(pgn)
        result = current_game.headers["Result"]
        # if given result found then assess game
        if result == desired_result and current_game.headers["Termination"] != "Abandoned":
            count += 1
            print("\nGame:", count)
            # file.write("\nGame " + str(count) + "\n")
            board = current_game.board()
            moves = current_game.mainline_moves()
            move_num = 0
            for move in moves:
                board.push(move)
                move_num += 1
                print(result + ":" + str(move_num) + ":" + str(get_features(board)))
                # file.write(result + ":" + str(move_num) + ":" + str(get_features(board)) + "\n")
        if count == 10000:
            break
    # file.close()


def count_pgn():
    pgn = open("./lichess_games_11_2021.pgn")
    data = dict()
    data["white"] = 0
    data["black"] = 0
    data["draw"] = 0

    file = open("count_november_games.txt", "w")

    current_game = chess.pgn.read_game(pgn)
    count = 0
    # while current_game is not None:
    for iteration in range(5500):
        count += 1
        current_game = chess.pgn.read_game(pgn)
        result = current_game.headers["Result"]
        if result == "1-0":
            data["white"] += 1
        elif result == "0-1":
            data["black"] += 1
        elif result == "1/2-1/2":
            data["draw"] += 1

        if count % 1000 == 0:
            countstr = "count: " + str(count) + "\n"
            whitestr = "white wins:" + str(data["white"]) + "\n"
            blackstr = "black wins:" + str(data["black"]) + "\n"
            drawstr = "draws:" + str(data["draw"]) + "\n\n"
            file.write(countstr)
            file.write(whitestr)
            file.write(blackstr)
            file.write(drawstr)

    countstr = "loop over. " + str(count) + " iterations\n"
    whitestr = "white wins:" + str(data["white"]) + "\n"
    blackstr = "black wins:" + str(data["black"]) + "\n"
    drawstr = "draws:" + str(data["draw"]) + "\n\n"
    file.write(countstr)
    file.write(whitestr)
    file.write(blackstr)
    file.write(drawstr)
    file.close()


def get_features(board):
    # white pawn 0-63, white knight, bishop, rook, queen, king, then black pawn, first is 384
    # + 4 is castling rights + 1 is white turn/black turn + 2 is white checkmate / black checkmate
    features = [0] * (768 + 4 + 1 + 2)
    for square in range(64):
        index = 0
        current = board.piece_at(square)
        if current is not None:
            # if the piece is black
            if not current.color:
                index += 384
            # offset by the piece type * 64
            index += piece_type_offset[current.piece_type]
            # add the corresponding square to the index
            index += square
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
            elif not outcome.winner:
                features[774] = 1

    return features

# file_to_arrays("first10kwhitewins.txt", "first10kblackwins.txt", 100)
# get_first_10k_result("1-0", "first10kwhitewins.txt")
# get_first_10k_result("0-1", "first10kblackwins.txt")
# get_first_10k_result("1/2-1/2", "first10kdraws.txt")

# count_pgn()