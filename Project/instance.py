import pygame
import Project.constants as constants
from Project.grid import Grid
from Project.player import Player
from Project.piece import Piece
from Project.helpers import getLocation, getChessPos
import random

class GameInstance():

    def __init__(self):
        self.width, self.height = constants.WIDTH, constants.HEIGHT

        self.titleTxt = constants.biggerFont.render("Chess", True, constants.COLOURS['white'])

        self.playTxt = constants.bigFont.render("Play", True, constants.COLOURS["white"])
        self.playTxtHovering = constants.bigFont.render("Play", True, constants.COLOURS["purple"])
        self.playTxtRect = self.playTxt.get_rect()
        self.playTxtRect.x, self.playTxtRect.y = (90, 200)

        self.quitTxt = constants.bigFont.render("Quit", True, constants.COLOURS["white"])
        self.quitTxtHovering = constants.bigFont.render("Quit", True, constants.COLOURS["purple"])
        self.quitTxtRect = self.quitTxt.get_rect()
        self.quitTxtRect.x, self.quitTxtRect.y = (90, 340)

        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.display = pygame.Surface((self.width, self.height))
        self.background = pygame.image.load("Assets\\background.png").convert_alpha()

        self.piecesTakenSurf = pygame.Surface((300, 350))
        self.promotionSurf = pygame.Surface((200, 260))
        self.timer = 0
        self.mouse = pygame.mouse.get_pos()
        self.mouseIncrement = [0, 0]

        self.p1 = Player("Player 1", "White")
        self.p1Txt = constants.regFont.render("You", True, constants.COLOURS['white'])
        self.p2 = Player("Player 2", "Black")
        self.p2Txt = constants.regFont.render("Them", True, constants.COLOURS['white'])
    
        self.grid = Grid(100, constants.HEIGHT / 2 - 256)
        self.hoveringSquare = None
        self.selectedPiece = None
        self.possibleMoves = []
        self.promotion = False

    def main_menu(self, dt, state, events):
        click = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        self.display.fill(constants.COLOURS["black"])
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.titleTxt, (50, 40))

        if not self.playTxtRect.collidepoint(pygame.mouse.get_pos()):
            self.display.blit(self.playTxt, self.playTxtRect)
        else:
            self.display.blit(self.playTxtHovering, self.playTxtRect)
            if click:
                state = "Game"
        
        if not self.quitTxtRect.collidepoint(pygame.mouse.get_pos()):
            self.display.blit(self.quitTxt, self.quitTxtRect)
        else:
            self.display.blit(self.quitTxtHovering, self.quitTxtRect)
            if click:
                state = "Quit"

        self.screen.blit(self.display, (0, 0))

        return state

    def run(self, dt, state, events):
        click = False
        self.mouseIncrement = [pygame.mouse.get_pos()[0] - self.mouse[0], pygame.mouse.get_pos()[1] - self.mouse[1]]
        self.mouse = pygame.mouse.get_pos()

        if not self.promotion:
            self.display.fill(constants.COLOURS["black"])

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if not self.promotion:
            self.updateGrid()

        for piece in self.p1.pieces:
            if piece.piece_rect.collidepoint(self.mouse):
                mask_x = self.mouse[0] - piece.piece_rect.left
                mask_y = self.mouse[1] - piece.piece_rect.top
                if piece.mask.get_at((mask_x, mask_y)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if pygame.mouse.get_pressed()[0] and self.selectedPiece is None:
                        piece.selected = True
                        self.selectedPiece = piece
                    break
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not pygame.mouse.get_pressed()[0]:
            if self.hoveringSquare != None:
                for piece in self.p1.pieces:
                    if piece == self.selectedPiece:
                        piece.selected = False
                        piece.moves += 1
                        if not piece.checkValidLocation(self.hoveringSquare, self.p1.pieces):
                            if self.hoveringSquare == [1, 8]:
                                piece.location = getChessPos([3, 8])
                                for p in self.p1.pieces:
                                    if getLocation(p.location) == [1, 8]:
                                        p.location = getChessPos([4, 8])
                                        p.moves += 1
                                        break
                            elif self.hoveringSquare == [8, 8]:
                                piece.location = getChessPos([7, 8])
                                for p in self.p1.pieces:
                                    if getLocation(p.location) == [8, 8]:
                                        p.location = getChessPos([6, 8])
                                        p.moves += 1
                                        break
                        else:
                            piece.location = getChessPos(self.hoveringSquare)
                            if piece.name == "pawn" and getLocation(piece.location)[1] == 1:
                                self.selectedPiece = None
                                piece.promotion = True
                                self.promotion = True
                                self.updateGrid()

                self.hoveringSquare = None
            self.selectedPiece = None

        elif self.selectedPiece != None:
            self.selectedPiece.piece_rect.x += self.mouseIncrement[0]
            self.selectedPiece.piece_rect.y += self.mouseIncrement[1]
            self.possibleMoves = self.selectedPiece.getPossibleMoves(self.p1.pieces)

        self.showPiecesTaken()

        self.display.blit(self.piecesTakenSurf, (self.grid.x + self.grid.layout.width + 50, 140))
        if self.promotion:
            chosen = self.promotionOptions(click)
            self.display.blit(self.promotionSurf, (self.width / 2 - self.promotionSurf.get_width() / 2, self.height / 2 - self.promotionSurf.get_height() / 2))
            if chosen != None:
                self.promotion = False
                for piece in self.p1.pieces:
                    if piece.promotion:
                        piece.promote(chosen)

        self.screen.blit(self.display, (0, 0))

        return state

    def updateGrid(self):
        self.hoveringSquare = self.grid.drawLayout(self.display, self.possibleMoves, self.selectedPiece, self.hoveringSquare, self.mouse)
        self.grid.drawPieces(self.display, self.p1.pieces, self.selectedPiece)
        self.grid.drawPieces(self.display, self.p2.pieces, self.selectedPiece)

    def showPiecesTaken(self):
        self.piecesTakenSurf.fill(constants.COLOURS["black"])
        self.piecesTakenSurf.blit(self.p2Txt, (0, 0))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "pawn", 32), (0, 50))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('pawn', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 55))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "rook", 32), (100, 50))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('rook', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 55))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "knight", 32), (200, 50))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('knight', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (240, 55))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "bishop", 32), (0, 120))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('bishop', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 125))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "queen", 32), (100, 120))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('queen', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 125))

        self.piecesTakenSurf.blit(self.p1Txt, (0, 200))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "pawn", 32), (0, 250))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('pawn', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 255))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "rook", 32), (100, 250))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('rook', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 255))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "knight", 32), (200, 250))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('knight', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (240, 255))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "bishop", 32), (0, 320))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('bishop', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 325))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "queen", 32), (100, 320))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('quen', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 325))

    def promotionOptions(self, click):
        self.promotionSurf.fill(constants.COLOURS["white"])
        self.promotionTxt = constants.medfont.render("Promotion", True, constants.COLOURS['black'])
        self.promotionSurf.blit(self.promotionTxt, (100 - self.promotionTxt.get_width() / 2, 10))

        rect = pygame.Rect(0, 60, 100, 100)
        if pygame.Rect((self.width / 2 - self.promotionSurf.get_width() / 2) + rect.x, (self.height / 2 - self.promotionSurf.get_height() / 2) + rect.y, 100, 100).collidepoint(self.mouse):
            pygame.draw.rect(self.promotionSurf, constants.COLOURS["purple"], rect)
            if click:
                return "rook"
        self.promotionSurf.blit(Piece.getPieceImage(self.p1.side, "rook", 80), (10, 70))

        rect = pygame.Rect(100, 60, 100, 100)
        if pygame.Rect((self.width / 2 - self.promotionSurf.get_width() / 2) + rect.x, (self.height / 2 - self.promotionSurf.get_height() / 2) + rect.y, 100, 100).collidepoint(self.mouse):
            pygame.draw.rect(self.promotionSurf, constants.COLOURS["purple"], rect)
            if click:
                return "knight"
        self.promotionSurf.blit(Piece.getPieceImage(self.p1.side, "knight", 80), (110, 70))

        rect = pygame.Rect(0, 160, 100, 100)
        if pygame.Rect((self.width / 2 - self.promotionSurf.get_width() / 2) + rect.x, (self.height / 2 - self.promotionSurf.get_height() / 2) + rect.y, 100, 100).collidepoint(self.mouse):
            pygame.draw.rect(self.promotionSurf, constants.COLOURS["purple"], rect)
            if click:
                return "bishop"
        self.promotionSurf.blit(Piece.getPieceImage(self.p1.side, "bishop", 80), (10, 170))

        rect = pygame.Rect(100, 160, 100, 100)
        if pygame.Rect((self.width / 2 - self.promotionSurf.get_width() / 2) + rect.x, (self.height / 2 - self.promotionSurf.get_height() / 2) + rect.y, 100, 100).collidepoint(self.mouse):
            pygame.draw.rect(self.promotionSurf, constants.COLOURS["purple"], rect)
            if click:
                return "queen"
        self.promotionSurf.blit(Piece.getPieceImage(self.p1.side, "queen", 80), (110, 170))

        return None
