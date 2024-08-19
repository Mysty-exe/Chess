import pygame
from Project.helpers import getName, getLocation

class Piece:
    def __init__(self, name, location, colour):
        self.name = getName(name)
        self.location = location
        self.colour = colour
        self.size = 52
        self.selected = False
        
        if name != "None":
            self.piece = pygame.image.load(f"Assets\\Pieces\\{self.colour}\\{self.name}.png").convert_alpha()
            self.piece = pygame.transform.scale(self.piece, (self.size, self.size))
            self.piece_rect = self.piece.get_rect()
            self.mask = pygame.mask.from_surface(self.piece)

        self.moves = 0

    @classmethod
    def getPiece(cls, pieces, location):
        for piece in pieces:
            if getLocation(piece.location) == location:
                return piece
        return -1

    def draw(self, display, position):
        self.piece_rect.x, self.piece_rect.y = position
        display.blit(self.piece, self.piece_rect)

    def getPossibleMoves(self):
        loc = getLocation(self.location)
        moves = []
        if self.name == "pawn":
            if loc[1] > 1:
                moves.append([loc[0], loc[1] - 1])
                if self.moves == 0:
                    moves.append([loc[0], loc[1] - 2])

        return moves

