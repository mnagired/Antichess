'''
The Piece class stores the attributes of each chess piece which is stored on a
subsequent location on the board.

The various subclasses are more specific pieces (ex. Pawn and Knight) with their
pictures as the only overriden attribute in their respective __init__ functions.
'''

from tkinter import *
from PIL import Image, ImageTk


class Piece(object):
    def __init__(self, location, size, board, color, value=0, picName=''):
        self.location = location
        (self.x, self.y) = location
        self.size, self.picName = size, picName
        self.board = board
        self.color = color
        self.canCapture = False
        self.singleCapture = False
        self.value = value

    def draw(self, canvas):
        x = self.location[1] * self.size + self.size * 0.5
        y = self.location[0] * self.size + self.size * 0.5
        # image.open idea taken from https://pythonbasics.org/tkinter-image/
        canvas.create_image(
            x, y, image=ImageTk.PhotoImage(Image.open(self.picName)))

    def __eq__(self, other):
        if isinstance(other, Piece):
            if self.location == other.location:
                return True
        return False

    # incorporated and adjusted idea for moves from https://github.com/saavedra29/chess_tk
    def moves(self, location, isPerpendicular, isDiagonal, distance, isPawn, isKnight):
        self.canCapture = False
        moves = []
        captures = []

        # all possible directions for moves for all pieces except knights and pawns
        perpendicular = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diagonal = ((-1, -1), (-1, 1), (1, -1), (1, 1))

        start = self.location
        if isPerpendicular and isDiagonal:
            dirs = perpendicular + diagonal
        elif isDiagonal:
            dirs = diagonal
        elif isPerpendicular:
            dirs = perpendicular

        if isKnight:
            return self.knightMoves(self.location, moves, captures)
        elif isPawn:
            return self.pawnMoves(self.location, moves, captures)
        else:
            for x, y in dirs:
                # check max distance a piece can move (ex. max Queen move distance = 8)
                for move in range(1, distance + 1):
                    if self.color == 'black':
                        # black moves in opposite direction of white so subtract
                        result = (start[0] - move * x, start[1] - move * y)
                        resultx, resulty = start[0] - \
                            move * x, start[1] - move * y
                    else:  # white turn
                        result = (start[0] + move * x, start[1] + move * y)
                        resultx, resulty = start[0] + \
                            move * x, start[1] + move * y
                    if self.inBounds(resultx, resulty):
                        if self.board[resultx][resulty] is None:
                            # moving to an empty location
                            moves.append(result)
                        # there is a capture
                        elif isinstance(self.board[resultx][resulty], Piece):
                            # can't capture your own pieces
                            if self.board[resultx][resulty].color != self.color:
                                # don't want to capture a piece behind another piece
                                if(not self.singleCapture):
                                    self.singleCapture = True
                                    self.canCapture = True
                                    captures.append(result)
                            else:
                                break
                self.singleCapture = False
        # there is at least 1 capture, so captures is/are the only move(s)
        if len(captures) != 0:
            return captures
        else:
            # no captures
            return moves

    def knightMoves(self, start, moves, captures):
        # 8 possible moves for knight
        knightDirs = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1))
        # same logic as for other pieces
        for x, y in knightDirs:
            if (self.color == 'black'):
                result = (start[0] - x, start[1] - y)
                resultx, resulty = start[0] - x, start[1] - y
            else:
                result = (start[0] + x, start[1] + y)
                resultx, resulty = start[0] + x, start[1] + y
            if self.inBounds(resultx, resulty):
                if self.board[resultx][resulty] is None:
                    moves.append(result)
                if isinstance(self.board[resultx][resulty], Piece):
                    if self.board[resultx][resulty].color != self.color:
                        self.canCapture = True
                        captures.append(result)
                    else:
                        break
        if len(captures) != 0:
            return captures
        else:
            return moves

    def pawnMoves(self, start, moves, captures):
        if self.color == 'white':
            pawnCaptures = ((-1, -1), (-1, 1))
        else:
            # x coordinate is reverse of for white pawn captures
            pawnCaptures = ((1, -1), (1, 1))
        # if pawn hasn't moved yet, so it can also move two cells up first
        if self.location[0] == 6 and self.color == 'white':
            pawnDirs = ((-1, 0), (-2, 0))
        # pawn has moved, so it can only move one up
        elif self.color == 'white':
            pawnDirs = ((-1, 0),)
        # if pawn hasn't moved yet, so it can also move two cells up first
        elif self.location[0] == 1 and self.color == 'black':
            pawnDirs = ((1, 0), (2, 0))
        # pawn has moved, so it can only move one up
        else:
            pawnDirs = ((1, 0),)

        for x, y in pawnDirs:
            result = (start[0] + x, start[1] + y)
            resultx, resulty = start[0] + x, start[1] + y
            if self.inBounds(resultx, resulty):
                if self.board[resultx][resulty] is None:
                    moves.append(result)
                else:
                    break
        for x, y in pawnCaptures:
            result = (start[0] + x, start[1] + y)
            resultx, resulty = start[0] + x, start[1] + y
            if self.inBounds(resultx, resulty):
                if isinstance(self.board[resultx][resulty], Piece):
                    if self.board[resultx][resulty].color != self.color:
                        self.canCapture = True
                        captures.append(result)
                    else:
                        break
        if len(captures) != 0:
            return captures
        else:
            return moves

    def inBounds(self, x, y):
        return (0 <= x < len(self.board) and
                0 <= y < len(self.board[0]))

    def __repr__(self):
        return f'{self.color} {type(self)} at location {self.location}'


class Pawn(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/araXKrt
            self.picName = 'pieces_image/pwhite.png'
        else:  # color == 'black'
            # image from https://imgur.com/8FAMtmp
            self.picName = 'pieces_image/pblack.png'

    def moves(self):
        return super().moves(self.location, False, False, 1, True, False)


class Knight(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/PwRbQGU
            self.picName = 'pieces_image/nwhite.png'
        else:
            # image from https://imgur.com/hy6QTNL
            self.picName = 'pieces_image/nblack.png'

    def moves(self):
        return super().moves(self.location, False, False, 0, False, True)


class Rook(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/FzNUKtn
            self.picName = 'pieces_image/rwhite.png'
        else:
            # image from https://imgur.com/tCAb1Sc
            self.picName = 'pieces_image/rblack.png'

    def moves(self):
        return super().moves(self.location, True, False, 8, False, False)


class Bishop(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/lF7DrTd
            self.picName = 'pieces_image/bwhite.png'
        else:
            # image from https://imgur.com/WMiZew1
            self.picName = 'pieces_image/bblack.png'

    def moves(self):
        return super().moves(self.location, False, True, 8, False, False)


class Queen(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/KCll87Z
            self.picName = 'pieces_image/qwhite.png'
        else:
            # image from https://imgur.com/tdCVVQ0
            self.picName = 'pieces_image/qblack.png'

    def moves(self):
        return super().moves(self.location, True, True, 8, False, False)


class King(Piece):
    def __init__(self, location, size, board, color, value):
        super().__init__(location, size, board, color, value)
        if color == 'white':
            # image from https://imgur.com/2TqVFyz
            self.picName = 'pieces_image/kwhite.png'
        else:
            # image from https://imgur.com/n6c8p65
            self.picName = 'pieces_image/kblack.png'

    def moves(self):
        return super().moves(self.location, True, True, 1, False, False)
