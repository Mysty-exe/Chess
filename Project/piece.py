import pygame
from Project.helpers import getName, getLocation

class Piece:
    def __init__(self, name, location, colour):
        self.name = getName(name)
        self.location = location
        self.colour = colour
        self.size = 52
        self.selected = False
        self.promotion = False
        
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
    def checkValidLocation(location, pieces):
        if location[0] in range(1, 9) and location[1] in range(1, 9):
            if location not in [getLocation(piece.location) for piece in pieces]:
                return True
        return False

    @staticmethod
    def diagonalMovement(loc, moves, pieces):
        for n in range(1, 9):
            move = [loc[0] - n, loc[1] - n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break
                
        for n in range(1, 9):
            move = [loc[0] + n, loc[1] + n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break

        for n in range(1, 9):
            move = [loc[0] - n, loc[1] + n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break

        for n in range(1, 9):
            move = [loc[0] + n, loc[1] - n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break
        
        return moves

    @staticmethod
    def regularMovement(loc, moves, pieces):
        for n in range(1, 9):
            move = [loc[0] - n, loc[1]]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break
                
        for n in range(1, 9):
            move = [loc[0] + n, loc[1]]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break

        for n in range(1, 9):
            move = [loc[0], loc[1] + n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break

        for n in range(1, 9):
            move = [loc[0], loc[1] - n]
            if move not in [getLocation(piece.location) for piece in pieces]:
                moves.append(move)
            else:
                break
        
        return moves

    def draw(self, display, position):
        self.piece_rect.x, self.piece_rect.y = position
        display.blit(self.piece, self.piece_rect)

    def promote(self, newPiece):
        self.name = newPiece
        self.piece = pygame.image.load(f"Assets\\Pieces\\{self.colour}\\{self.name}.png").convert_alpha()
        self.piece = pygame.transform.scale(self.piece, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.piece)

    def getPossibleMoves(self, pieces):
        loc = getLocation(self.location)
        moves = []
        if self.name == "pawn":
            moves.append([loc[0], loc[1] - 1])
            if self.moves == 0:
                moves.append([loc[0], loc[1] - 2])

        if self.name == "rook":
            moves = self.regularMovement(loc, moves, pieces)

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
            moves = self.diagonalMovement(loc, moves, pieces)

        if self.name == "queen":
            moves = self.regularMovement(loc, moves, pieces)
            moves = self.diagonalMovement(loc, moves, pieces)

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

        for piece in pieces:
            if piece.name == "rook":
                if piece.moves == 0 and self.moves == 0 :
                    if self.checkLeftCastleLocations(pieces):
                        moves.append([1, 8])
                    if self.checkRightCastleLocations(pieces):
                        moves.append([8, 8])

        return moves

    def checkLeftCastleLocations(self, pieces):
        if self.checkValidLocation([2, 8], pieces) and self.checkValidLocation([2, 8], pieces) and self.checkValidLocation([2, 8], pieces):
            return True
        return False

    def checkRightCastleLocations(self, pieces):
        if self.checkValidLocation([6, 8], pieces) and self.checkValidLocation([7, 8], pieces):
            return True
        return False
