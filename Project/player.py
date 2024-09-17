import Project.constants as constants
from Project.piece import Piece
from Project.helpers import getLocation, getChessPos
import uuid

class Player:
    def __init__(self):
        self.userId = uuid.uuid4()
        self.side = ""
        self.pieces = []
        self.takenPieces = []
        self.state = "Good"

    def setup(self):
        pieces = []
        for piece, location in constants.PIECES.items():
            pieces.append(Piece(piece, location[0], self.side))

        return pieces

    def drawPieces(self, display):
        for piece in self.pieces:
            piece.draw()

    def reflectLocations(self):
        for piece in self.pieces:
            piece = piece.reflect()
