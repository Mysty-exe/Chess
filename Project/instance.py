import pygame
import Project.constants as constants
from Project.grid import Grid
from Project.player import Player
from Project.piece import Piece
from Project.helpers import getLocation
import random

class GameInstance():

    def __init__(self):
        self.width, self.height = constants.WIDTH, constants.HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.display = pygame.Surface((self.width, self.height))
        self.timer = 0
        self.mouse = pygame.mouse.get_pos()
        self.mouseIncrement = [0, 0]

        self.p1 = Player("Player 1", "White")
        self.p2 = Player("Player 2", "Black")
        self.grid = Grid(constants.WIDTH / 2 - 256, constants.HEIGHT / 2 - 256)
        self.selectedPiece = None
        self.possibleMoves = []

    def main_menu(self):
        pass

    def run(self, dt, state, events):
        self.mouseIncrement = [pygame.mouse.get_pos()[0] - self.mouse[0], pygame.mouse.get_pos()[1] - self.mouse[1]]
        self.mouse = pygame.mouse.get_pos()
        self.display.fill(constants.COLOURS["light grey"])

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selectedPiece = Piece("None", [0, 0], "None")

        self.grid.drawLayout(self.display, self.possibleMoves, self.selectedPiece, self.mouse)
        self.grid.drawPieces(self.display, self.p1.pieces, self.selectedPiece)
        self.grid.drawPieces(self.display, self.p2.pieces, self.selectedPiece)

        for piece in self.p1.pieces:
            if piece.piece_rect.collidepoint(self.mouse):
                mask_x = self.mouse[0] - piece.piece_rect.left
                mask_y = self.mouse[1] - piece.piece_rect.top
                if piece.mask.get_at((mask_x, mask_y)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if pygame.mouse.get_pressed()[0] and self.selectedPiece is None:
                        self.selectedPiece = piece
                    break
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not pygame.mouse.get_pressed()[0]:
            self.selectedPiece = None
        elif self.selectedPiece != None:
            self.selectedPiece.piece_rect.x += self.mouseIncrement[0]
            self.selectedPiece.piece_rect.y += self.mouseIncrement[1]

        if self.selectedPiece != None:
            self.possibleMoves = self.selectedPiece.getPossibleMoves()

        self.screen.blit(self.display, (0, 0))

        return state
