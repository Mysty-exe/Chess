import pygame
import Project.constants as constants
from Project.client import Client
from Project.grid import Grid
from Project.player import Player
from Project.piece import Piece
from Project.helpers import getLocation, getChessPos
import random
import json

class GameInstance():

    def __init__(self):
        self.client = Client()
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

        self.checkmateScreen = pygame.Surface((self.width, self.height))
        self.checkmateScreen.set_alpha(128)
        self.checkmateScreen.fill((constants.COLOURS["green"]))

        self.checkmatedScreen = pygame.Surface((self.width, self.height))
        self.checkmatedScreen.set_alpha(128)
        self.checkmatedScreen.fill((constants.COLOURS["red2"]))

        self.stalemateScreen = pygame.Surface((self.width, self.height))
        self.stalemateScreen.set_alpha(128)
        self.stalemateScreen.fill((constants.COLOURS["white"]))

        self.forfeitScreen = pygame.Surface((self.width, self.height))
        self.forfeitScreen.set_alpha(128)
        self.forfeitScreen.fill((constants.COLOURS["white"]))

        self.piecesTakenSurf = pygame.Surface((300, 500))
        self.promotionSurf = pygame.Surface((200, 260))
        self.timer = 0
        self.mouse = pygame.mouse.get_pos()
        self.mouseIncrement = [0, 0]

        self.p1 = Player()
        self.p2 = None
        self.p1Txt = constants.regFont.render("You", True, constants.COLOURS['white'])
        self.p2Txt = constants.regFont.render("Them", True, constants.COLOURS['white'])
        self.turnTxt = constants.medfont.render("Your Turn", True, constants.COLOURS['light purple'])
        self.checkTxt = constants.medfont.render("You\'re in Check", True, constants.COLOURS['light red'])

        self.yesTxt = constants.font.render(f"Yes", True, constants.COLOURS['white'])
        self.yesTxtRect = self.yesTxt.get_rect()
        self.yesTxtRect.x, self.yesTxtRect.y = (325, 275)
        self.noTxt = constants.font.render(f"No", True, constants.COLOURS['white'])
        self.noTxtRect = self.noTxt.get_rect()
        self.noTxtRect.x, self.noTxtRect.y = (600, 275)
    
        self.grid = Grid(100, constants.HEIGHT / 2 - 256)
        self.hoveringSquare = None
        self.selectedPiece = None
        self.possibleMoves = []
        self.promotion = False
        self.updated = False
        self.moved = False
        self.ourTurn = False
        self.check = False
        self.stalemate = False
        self.checkmate = False
        self.forfeit = False

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
                state = "Lobby"
        
        if not self.quitTxtRect.collidepoint(pygame.mouse.get_pos()):
            self.display.blit(self.quitTxt, self.quitTxtRect)
        else:
            self.display.blit(self.quitTxtHovering, self.quitTxtRect)
            if click:
                state = "Quit"

        self.screen.blit(self.display, (0, 0))

        return state

    def lobby(self, dt, state, events):
        
        self.display.fill(constants.COLOURS["black"])

        try:
            self.client.connect(self.p1)
        except Exception:
            state = "Server Fail"
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.client.disconnect()
                    state = "Menu"
                elif event.key == pygame.K_RETURN:
                    self.client.ready = True

        data = ""
        if self.client.connected:
            data = self.client.receive()
            if data != "received":
                data = json.loads(data)

                if data["started"]:
                    for key, value in data["players"].items():
                        if key == str(self.p1.userId):
                            self.p1.side = value["colour"]
                            self.p1.pieces = self.p1.setup()
                        elif key != "turn":
                            self.p2 = Player()
                            self.p2.userId = key
                            self.p2.side = value["colour"]

                    self.ourTurn = True if data["turn"] == str(self.p1.userId) else False
                    for piece in self.p1.pieces:
                        piece.getPossibleMoves(self.p1.pieces, self.p2.pieces, False)
                    state = "Game"

            if self.client.ready:
                self.client.send(json.dumps({"disconnect": False, "ready": True}))
            else:
                self.client.send(json.dumps({"disconnect": False, "ready": False}))

        if state == "Lobby" and data != "received":
            waitingTxt = constants.medfont.render(f"Waiting for Players...", True, (255, 255, 255))
            playersTxt = constants.regFont.render(f'Players Ready: {data["connections"]}/{data["players"]}', True, (255, 255, 255))
            enterTxt = constants.regFont.render(f"Press Enter if You're Ready", True, (255, 255, 255))
            
            self.display.blit(waitingTxt, (500 - waitingTxt.get_width() / 2, 300 - waitingTxt.get_height() / 2))
            self.display.blit(playersTxt, (500 - playersTxt.get_width() / 2, (300 + waitingTxt.get_height() / 2) + 20))
            self.display.blit(enterTxt, (1000 - enterTxt.get_width() - 10, 600 - enterTxt.get_height() - 10))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Forfeit"

        try:
            self.client.send(json.dumps({"disconnect": False, "colour": self.p1.side, "pieces": Piece.getListPieces(self.p1.pieces), "taken": Piece.getListPieces(self.p1.takenPieces), "state": self.p1.state, "moved": self.moved}))
            data = self.client.receive()
            data = json.loads(data)
            if "disconnect" in list(data.keys()):
                if data["disconnect"] == True:
                    state = "Menu"
            else:
                for key, value in data["players"].items():
                    if key == str(self.p2.userId):
                        self.p2.pieces = Piece.getPiecesFromList(self.p2.side, value["pieces"])
                        self.p2.takenPieces = Piece.getPiecesFromList(self.p2.side, value["taken"])
                        self.p2.state = value["state"]
                        self.p2.reflectLocations()

                self.ourTurn = True if data["turn"] == str(self.p1.userId) else False
                if not self.ourTurn and self.updated:
                    self.updated = False
                if self.ourTurn and not self.updated:
                    for piece in self.p1.pieces:
                        piece.getPossibleMoves(self.p1.pieces, self.p2.pieces, True)
                    self.updated = True
                self.moved = False
                if self.stalemate or self.p2.state == "Stalemate":
                    state = "Stalemate"
                if self.checkmate:
                    state = "Checkmated"
                if self.p2.state == "Checkmate":
                    state = "Checkmate"
        except WindowsError as e:
            if self.forfeit:
                state = "Menu"
            else:
                state = "Forfeited"
        except Exception as e:
            pass

        takenPiecesIds = [str(piece.id) for piece in self.p2.takenPieces]
        self.p1.pieces = [piece for piece in self.p1.pieces if str(piece.id) not in takenPiecesIds]

        if not self.promotion:
            self.updateGrid()

        self.checkForCheck()

        if self.check:
            moves = []
            for piece in self.p1.pieces:
                if piece.possibleMoves:
                    moves.append(piece.possibleMoves)

            if not moves:
                self.p1.state = "Checkmate"
                self.checkmate = True
        else:
            moves = []
            for piece in self.p1.pieces:
                if piece.possibleMoves:
                    moves.append(piece.possibleMoves)

            if not moves:
                self.p1.state = "Checkmate"
                self.checkmate = True

        for piece in self.p1.pieces:
            if piece.piece_rect.collidepoint(self.mouse):
                mask_x = self.mouse[0] - piece.piece_rect.left
                mask_y = self.mouse[1] - piece.piece_rect.top
                if piece.mask.get_at((mask_x, mask_y)):
                    if self.ourTurn:
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
                                        self.moved = True
                                        break
                            elif self.hoveringSquare == [8, 8]:
                                piece.location = getChessPos([7, 8])
                                for p in self.p1.pieces:
                                    if getLocation(p.location) == [8, 8]:
                                        p.location = getChessPos([6, 8])
                                        p.moves += 1
                                        self.moved = True
                                        break
                                
                        else:
                            if not Piece.checkValidLocation(self.hoveringSquare, self.p2.pieces):
                                p = None
                                for p1 in self.p2.pieces:
                                    if getLocation(p1.location) == self.hoveringSquare:
                                        p = p1
                                        self.p1.takenPieces.append(p1)
                                if p in self.p2.pieces:
                                    self.p2.pieces.remove(p)

                            if piece.name == "pawn" and self.hoveringSquare[1] == 1:
                                self.selectedPiece = None
                                piece.promotion = True
                                self.promotion = True

                            piece.location = getChessPos(self.hoveringSquare)
                            self.updateGrid()
                            self.moved = True

                self.hoveringSquare = None
            self.selectedPiece = None

        elif self.selectedPiece != None and self.ourTurn:
            self.selectedPiece.piece_rect.x += self.mouseIncrement[0]
            self.selectedPiece.piece_rect.y += self.mouseIncrement[1]
            self.possibleMoves = self.selectedPiece.possibleMoves

        self.showPiecesTaken()

        self.display.blit(self.piecesTakenSurf, (self.grid.x + self.grid.layout.width + 50, 90))
        if self.promotion:
            chosen = self.promotionOptions(click)
            self.display.blit(self.promotionSurf, (self.width / 2 - self.promotionSurf.get_width() / 2, self.height / 2 - self.promotionSurf.get_height() / 2))
            if chosen != None:
                self.promotion = False
                for piece in self.p1.pieces:
                    if piece.promotion:
                        piece.promote(chosen)
                        self.moved = True

        self.screen.blit(self.display, (0, 0))

        return state, self.display.copy()

    def checkForCheck(self):
        tempPieces1, tempPieces2 = [], []
        for piece in self.p1.pieces:
            p = Piece(piece.name, piece.location, piece.colour)
            p.possibleMoves = piece.possibleMoves
            p.reflect()
            tempPieces1.append(p)
        for piece in self.p2.pieces:
            p = Piece(piece.name, piece.location, piece.colour)
            p.reflect()
            tempPieces2.append(p)
    
        allPossibleMoves = []
        for piece in tempPieces2:
            mves = piece.getPossibleMoves(tempPieces2, tempPieces1, False)
            for m in mves:
                allPossibleMoves.append(m)

        for piece in tempPieces1:
            if piece.name == "king":
                if getLocation(piece.location) in allPossibleMoves:
                    self.p1.state = "Check"
                    self.check = True
                    break
        else:
            self.p1.state = "Good"
            self.check = False

    def updateGrid(self):
        self.hoveringSquare = self.grid.drawLayout(self.display, self.possibleMoves, self.selectedPiece, self.hoveringSquare, self.mouse, self.ourTurn, self.check)
        self.grid.drawPieces(self.display, self.p2.pieces, self.selectedPiece)
        self.grid.drawPieces(self.display, self.p1.pieces, self.selectedPiece)

    def showPiecesTaken(self):
        self.piecesTakenSurf.fill(constants.COLOURS["black"])
        if self.ourTurn:
            if not self.check:
                self.piecesTakenSurf.blit(self.turnTxt, (150 - self.turnTxt.get_width() / 2, 0))
            else:
                self.piecesTakenSurf.blit(self.checkTxt, (150 - self.checkTxt.get_width() / 2, 0))

        self.piecesTakenSurf.blit(self.p2Txt, (0, 70))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "pawn", 32), (0, 120))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('pawn', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 125))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "rook", 32), (100, 120))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('rook', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 125))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "knight", 32), (200, 120))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('knight', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (240, 125))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "bishop", 32), (0, 190))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('bishop', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 195))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p1.side, "queen", 32), (100, 190))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('queen', self.p2.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 195))

        self.piecesTakenSurf.blit(self.p1Txt, (0, 270))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "pawn", 32), (0, 320))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('pawn', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 325))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "rook", 32), (100, 320))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('rook', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 325))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "knight", 32), (200, 320))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('knight', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (240, 325))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "bishop", 32), (0, 390))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('bishop', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (40, 395))

        self.piecesTakenSurf.blit(Piece.getPieceImage(self.p2.side, "queen", 32), (100, 390))
        self.pieceTxt = constants.regFont.render(f"x {Piece.getNumberOfPieces('queen', self.p1.takenPieces)}", True, constants.COLOURS['white'])
        self.piecesTakenSurf.blit(self.pieceTxt, (140, 395))

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

    def forfeitedEnd(self, dt, state, events, copy):

        self.display.blit(copy, (0, 0))
        self.display.blit(self.forfeitScreen, (0, 0))

        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        self.forfeitTxt = constants.bigFont.render(f"Forfeit?", True, constants.COLOURS['white'])
        self.display.blit(self.forfeitTxt, (self.width / 2 - self.forfeitTxt.get_width() / 2, 150))

        if self.yesTxtRect.collidepoint(pygame.mouse.get_pos()):
            yesTxt = constants.font.render(f"Yes", True, constants.COLOURS['purple'])
            self.display.blit(yesTxt, (325, 275))
            if click:
                self.client.disconnect()
                state = "Menu"
        else:
            yesTxt = constants.font.render(f"Yes", True, constants.COLOURS['white'])
            self.display.blit(yesTxt, (325, 275))

        if self.noTxtRect.collidepoint(pygame.mouse.get_pos()):
            noTxt = constants.font.render(f"No", True, constants.COLOURS['purple'])
            self.display.blit(noTxt, (600, 275))
            if click:
                state = "Game"
        else:
            noTxt = constants.font.render(f"No", True, constants.COLOURS['white'])
            self.display.blit(noTxt, (600, 275))

        self.screen.blit(self.display, (0, 0))

        return state

    def forfeitEnd(self, dt, state, events, copy):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Menu"
                    self.reset()

        self.display.blit(copy, (0, 0))
        self.display.blit(self.checkmateScreen, (0, 0))

        self.checkmateTxt = constants.bigFont.render(f"Forfeited", True, constants.COLOURS['white'])
        self.wonTxt = constants.font.render(f"Opponent Disconnect. You have Won!", True, constants.COLOURS['white'])
        self.returnTxt = constants.regFont.render(f"Press Escape to go to Main Menu", True, constants.COLOURS['white'])
        self.display.blit(self.checkmateTxt, (self.width / 2 - self.checkmateTxt.get_width() / 2, 150))
        self.display.blit(self.wonTxt, (self.width / 2 - self.wonTxt.get_width() / 2, 275))
        self.display.blit(self.returnTxt, (self.width / 2 - self.returnTxt.get_width() / 2, 340))

        self.screen.blit(self.display, (0, 0))

        return state

    def checkmateEnd(self, dt, state, events, copy):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Menu"
                    self.reset()

        self.display.blit(copy, (0, 0))
        self.display.blit(self.checkmateScreen, (0, 0))

        self.checkmateTxt = constants.bigFont.render(f"Checkmate", True, constants.COLOURS['white'])
        self.wonTxt = constants.font.render(f"You have Won!", True, constants.COLOURS['white'])
        self.returnTxt = constants.regFont.render(f"Press Escape to go to Main Menu", True, constants.COLOURS['white'])
        self.display.blit(self.checkmateTxt, (self.width / 2 - self.checkmateTxt.get_width() / 2, 150))
        self.display.blit(self.wonTxt, (self.width / 2 - self.wonTxt.get_width() / 2, 275))
        self.display.blit(self.returnTxt, (self.width / 2 - self.returnTxt.get_width() / 2, 340))

        self.screen.blit(self.display, (0, 0))

        return state

    def checkmatedEnd(self, dt, state, events, copy):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Menu"
                    self.reset()

        self.display.blit(copy, (0, 0))
        self.display.blit(self.checkmatedScreen, (0, 0))

        self.checkmateTxt = constants.bigFont.render(f"Checkmated", True, constants.COLOURS['white'])
        self.wonTxt = constants.font.render(f"You have Lost...", True, constants.COLOURS['white'])
        self.returnTxt = constants.regFont.render(f"Press Escape to go to Main Menu", True, constants.COLOURS['white'])
        self.display.blit(self.checkmateTxt, (self.width / 2 - self.checkmateTxt.get_width() / 2, 150))
        self.display.blit(self.wonTxt, (self.width / 2 - self.wonTxt.get_width() / 2, 275))
        self.display.blit(self.returnTxt, (self.width / 2 - self.returnTxt.get_width() / 2, 340))
        self.screen.blit(self.display, (0, 0))

        return state

    def stalemateEnd(self, dt, state, events, copy):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Menu"
                    self.reset()

        self.display.blit(copy, (0, 0))
        self.display.blit(self.stalemateEnd, (0, 0))

        self.checkmateTxt = constants.bigFont.render(f"Stalemate", True, constants.COLOURS['purple'])
        self.wonTxt = constants.font.render(f"You have Tied.", True, constants.COLOURS['light purple'])
        self.returnTxt = constants.regFont.render(f"Press Escape to go to Main Menu", True, constants.COLOURS['light purple'])
        self.display.blit(self.checkmateTxt, (self.width / 2 - self.checkmateTxt.get_width() / 2, 150))
        self.display.blit(self.wonTxt, (self.width / 2 - self.wonTxt.get_width() / 2, 275))
        self.display.blit(self.returnTxt, (self.width / 2 - self.returnTxt.get_width() / 2, 340))
        self.screen.blit(self.display, (0, 0))

        return state

    def serverFailed(self, dt, state, events):
        self.display.fill((0, 0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Menu"

        self.failedTxt = constants.bigFont.render(f"Server Failed", True, constants.COLOURS['white'])
        self.display.blit(self.failedTxt, (self.width / 2 - self.failedTxt.get_width() / 2, 150))
        self.returnTxt = constants.regFont.render(f"Press Escape to go to Main Menu", True, constants.COLOURS['white'])
        self.display.blit(self.returnTxt, (self.width / 2 - self.returnTxt.get_width() / 2, 275))

        self.screen.blit(self.display, (0, 0))

        return state

    def reset(self):
        self.client = Client()
        self.p1 = Player()
        self.p2 = None
        self.hoveringSquare = None
        self.selectedPiece = None
        self.possibleMoves = []
        self.promotion = False
        self.moved = False
        self.ourTurn = False
        self.check = False
        self.stalemate = False
        self.checkmate = False
        self.forfeit = False
