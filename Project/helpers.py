def getName(name):
        if name == "king":
            return "king"
        elif name[0] == "p":
            return "pawn"
        elif name[0] == "r":
            return "rook"
        elif name[0] == "k":
            return "knight"
        elif name[0] == "b":
            return "bishop"
        elif name[0] == "q":
            return "queen"
        else:
            return name

def getLocation(loc):
    column = 0
    row = 0
    column = 1 if loc[0] == "a" else column
    column = 2 if loc[0] == "b" else column
    column = 3 if loc[0] == "c" else column
    column = 4 if loc[0] == "d" else column
    column = 5 if loc[0] == "e" else column
    column = 6 if loc[0] == "f" else column
    column = 7 if loc[0] == "g" else column
    column = 8 if loc[0] == "h" else column

    row = 1 if loc[1] == "8" else row
    row = 2 if loc[1] == "7" else row
    row = 3 if loc[1] == "6" else row
    row = 4 if loc[1] == "5" else row
    row = 5 if loc[1] == "4" else row
    row = 6 if loc[1] == "3" else row
    row = 7 if loc[1] == "2" else row
    row = 8 if loc[1] == "1" else row

    return [column, row]