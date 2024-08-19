import Project.constants as constants
from Project.piece import Piece

class Player:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.pieces = self.setup()
        self.takenPieces = []

    def setup(self):
        pieces = []
        for piece, location in constants.PIECES.items():
            if self.side == "White":
                pieces.append(Piece(piece, location[0], self.side))
            else:
                pieces.append(Piece(piece, location[1], self.side))

        return pieces

    def drawPieces(self, display):
        for piece in self.pieces:
            piece.draw()
