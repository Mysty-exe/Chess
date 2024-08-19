import pygame
import Project.constants as constants
from Project.helpers import getLocation
from Project.piece import Piece

class Grid:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.layout = pygame.Rect(self.x - 10, self.y - 10, 532, 532)

    def drawLayout(self, display, moves, selected, mouse):
        x, y = self.x, self.y

        pygame.draw.rect(display, constants.COLOURS["purple"], self.layout)
        for row in range(1, 9):
            for col in range(1, 9):
                rect = pygame.Rect(x, y, 64, 64)
                if row % 2 != 0:
                    if col % 2 != 0:
                        pygame.draw.rect(display, constants.COLOURS["white"], rect)
                    else:
                        pygame.draw.rect(display, constants.COLOURS["black"], rect)
                else:
                    if col % 2 != 0:
                        pygame.draw.rect(display, constants.COLOURS["black"], rect)
                    else:
                        pygame.draw.rect(display, constants.COLOURS["white"], rect)

                if selected != None:
                    if [col, row] in moves:
                        pygame.draw.circle(display, constants.COLOURS["purple"], (x + 32, y + 32), 8, 8)
                        if rect.collidepoint(mouse):
                            pygame.draw.rect(display, constants.COLOURS["purple"], rect)

                x += 64

            x = self.x
            y += 64

    def drawPieces(self, display, pieces, selected):
        for piece in pieces:
            if piece != selected:
                column, row = getLocation(piece.location)
                x = self.x + (64 * (column - 1)) + (32 - piece.size / 2)
                y = self.y + (64 * (row - 1)) + (32 - piece.size / 2)
                piece.draw(display, (x, y))
            else:
                display.blit(piece.piece, piece.piece_rect)

    def allowed(self, pieces, square):
        for piece in pieces:
            if getLocation(piece.location) == square:
                break
        else:
            return False
        return True
