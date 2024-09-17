import pygame
import Project.constants as constants
from Project.helpers import getName, getLocation, getChessPos
import uuid

class Piece:
    def __init__(self, name, location, colour):
        self.id = uuid.uuid4()
        self.name = getName(name)
        self.location = location
        self.colour = colour
        self.size = 52
        self.selected = False
        self.promotion = False
        self.possibleMoves = []

        if name != "None":
            self.piece = pygame.image.load(f"Assets\\Pieces\\{self.colour}\\{self.name}.png").convert_alpha()
            self.piece = pygame.transform.scale(self.piece, (self.size, self.size))
            self.piece_rect = self.piece.get_rect()
            self.mask = pygame.mask.from_surface(self.piece)

        self.moves = 0

    @classmethod
    def getPiecesFromList(cls, colour, lst):
        newLst = []
        for piece in lst:
            p = cls(piece[0], piece[1], colour)
            p.id = uuid.UUID(piece[2])
            newLst.append(p)

        return newLst

    @classmethod
    def getListPieces(cls, pieces):
        result = []
        for piece in pieces:
            result.append([piece.name, piece.location, str(piece.id)])

        return result

    @classmethod
    def getPiece(cls, pieces, location):
        for piece in pieces:
            if getLocation(piece.location) == location:
                return piece
        return -1

    @classmethod
    def getNumberOfPieces(cls, piece, pieces):
        counter = 0
        for p in pieces:
            if p.name == piece:
                counter += 1

        return counter

    @classmethod
    def getPieceImage(cls, colour, piece, size):
        image = pygame.image.load(f"Assets\\Pieces\\{colour}\\{piece}.png").convert_alpha()
        return pygame.transform.scale(image, (size, size))

    @staticmethod
    def checkValidLocation(location, pieces, others=[]):
        if location[0] in range(1, 9) and location[1] in range(1, 9):
            if location not in [getLocation(piece.location) for piece in (pieces + others)]:
                return True
        return False

    @staticmethod
    def diagonalMovement(loc, moves, pieces, others=[]):
        for n in range(1, 9):
            move = [loc[0] - n, loc[1] - n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break
                
        for n in range(1, 9):
            move = [loc[0] + n, loc[1] + n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break

        for n in range(1, 9):
            move = [loc[0] - n, loc[1] + n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break

        for n in range(1, 9):
            move = [loc[0] + n, loc[1] - n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break
        
        return moves

    @staticmethod
    def regularMovement(loc, moves, pieces, others=[]):
        for n in range(1, 9):
            move = [loc[0] - n, loc[1]]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break
                
        for n in range(1, 9):
            move = [loc[0] + n, loc[1]]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break

        for n in range(1, 9):
            move = [loc[0], loc[1] + n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break

        for n in range(1, 9):
            move = [loc[0], loc[1] - n]
            if move not in [getLocation(piece.location) for piece in (pieces + others)]:
                moves.append(move)
            else:
                if Piece.checkValidLocation(move, pieces):
                    moves.append(move)
                break
        
        return moves

    @staticmethod
    def reflectLocation(loc):
        loc[1] = constants.REFLECTED[int(loc[1])]
        return loc

    def draw(self, display, position):
        self.piece_rect.x, self.piece_rect.y = position
        display.blit(self.piece, self.piece_rect)

    def reflect(self):
        self.location = getChessPos(self.reflectLocation(getLocation(self.location)))

    def promote(self, newPiece):
        self.name = newPiece
        self.piece = pygame.image.load(f"Assets\\Pieces\\{self.colour}\\{self.name}.png").convert_alpha()
        self.piece = pygame.transform.scale(self.piece, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.piece)

    def getPossibleMoves(self, pieces, others, check):
        loc = getLocation(self.location)
        moves = []
        verified = []
        if self.name == "pawn":
            if self.checkValidLocation([loc[0], loc[1] - 1], pieces, others=others):
                moves.append([loc[0], loc[1] - 1])
                if self.moves == 0 and self.checkValidLocation([loc[0], loc[1] - 2], pieces, others=others):
                    moves.append([loc[0], loc[1] - 2])

            if not self.checkValidLocation([loc[0] - 1, loc[1] - 1], others):
                moves.append([loc[0] - 1, loc[1] - 1])
            if not self.checkValidLocation([loc[0] + 1, loc[1] - 1], others):
                moves.append([loc[0] + 1, loc[1] - 1])

        if self.name == "rook":
            moves = self.regularMovement(loc, moves, pieces, others=others)

        if self.name == "king":
            moves.append([loc[0], loc[1] - 1])
            moves.append([loc[0] - 1, loc[1] - 1])
            moves.append([loc[0], loc[1] + 1])
            moves.append([loc[0] - 1, loc[1] + 1])
            moves.append([loc[0] - 1, loc[1]])
            moves.append([loc[0] + 1, loc[1] + 1])
            moves.append([loc[0] + 1, loc[1]])
            moves.append([loc[0] + 1, loc[1] - 1])

        if self.name == "bishop":
            moves = self.diagonalMovement(loc, moves, pieces, others=others)

        if self.name == "queen":
            moves = self.regularMovement(loc, moves, pieces, others=others)
            moves = self.diagonalMovement(loc, moves, pieces, others=others)

        if self.name == "knight":
            moves.append([loc[0] - 2, loc[1] - 1])
            moves.append([loc[0] - 1, loc[1] - 2])
            moves.append([loc[0] + 2, loc[1] + 1])
            moves.append([loc[0] + 1, loc[1] + 2])
            moves.append([loc[0] - 2, loc[1] + 1])
            moves.append([loc[0] + 2, loc[1] - 1])
            moves.append([loc[0] - 1, loc[1] + 2])
            moves.append([loc[0] + 1, loc[1] - 2])

        moves = [move for move in moves if self.checkValidLocation(move, pieces) and move != loc]
        if check:
            moves = [move for move in moves if not self.checkMoveChecked(move, pieces, others)]

        if self.name == "king":
            for piece in pieces:
                if piece.name == "rook":
                    if piece.moves == 0 and self.moves == 0 :
                        if self.checkLeftCastleLocations(pieces, others):
                            if not self.checkMoveChecked([3, 8], pieces, others) and not self.checkMoveChecked([4, 8], pieces, others):
                                moves.append([1, 8])
                        if self.checkRightCastleLocations(pieces, others):
                            if not self.checkMoveChecked([6, 8], pieces, others) and not self.checkMoveChecked([7, 8], pieces, others):
                                moves.append([8, 8])

        self.possibleMoves = moves
        return moves

    def checkMoveChecked(self, move, pieces, others):
        tempPieces1, tempPieces2 = [], []
        for piece in pieces:
            p = Piece(piece.name, piece.location, piece.colour)
            if str(self.id) == str(piece.id):
                p.location = getChessPos(move)
            p.reflect()
            tempPieces1.append(p)
        for piece in others:
            if getChessPos(move) != piece.location:
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
                    return True

        return False

    def checkLeftCastleLocations(self, pieces, others):
        if self.checkValidLocation([2, 8], pieces, others=others) and self.checkValidLocation([3, 8], pieces, others=others) and self.checkValidLocation([4, 8], pieces, others=others):
            return True
        return False

    def checkRightCastleLocations(self, pieces, others):
        if self.checkValidLocation([6, 8], pieces, others=others) and self.checkValidLocation([7, 8], pieces, others=others):
            return True
        return False
