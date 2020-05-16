'''
This is the main file that does both the alogrithms and displays the game.
It utilizes a modal app structure in order to effectively have an object-oriented design.
'''

# from Week9: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
import random
import copy
from cmu_112_graphics import *
from tkinter import *
from PIL import Image, ImageTk


# Modal App Structure Taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class ChessGame(ModalApp):
    def appStarted(app):
        app.startMenu = StartMenu()
        app.helpMenu = HelpMenu()
        app.gameMode = GameMode()
        app.setActiveMode(app.startMenu)

    def runChessGame(app):
        ChessGame()

#all image loading syntax taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#loadImageUsingUrl

class StartMenu(Mode):
    # methods taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def appStarted(mode):
        #image from https://picon.ngfiles.com/686000/flash_686219_largest_crop.png?f1482400573
        mode.imgFile = 'images/title.png'
        mode.img = mode.scaleImage(mode.loadImage(mode.imgFile), 1.5)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.helpMenu)

    def mousePressed(mode, event):
        mode.app.setActiveMode(mode.app.helpMenu)

    #image loading taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#imageMethods
    def redrawAll(mode, canvas):
        text = '''
        Welcome to Antichess!
        Click or press any key to get started!
        Once in the game mode, press h to go to the help screen!
        '''
        canvas.create_rectangle(0, 0, mode.app.width,
                                mode.app.height, fill='teal')
        canvas.create_image(mode.app.width/2, mode.app.height*2/5,
                            image=ImageTk.PhotoImage(mode.img))
        #font idea from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html#sizingText
        canvas.create_text(mode.app.width/2, mode.app.height *
                           8.5/10, text=text, font="Helvetica 26 bold")

class HelpMenu(Mode):
    def appStarted(mode):
        #image from http://www.astro-baby.com/astrobaby/wp-content/uploads/2017/10/header_help.jpg
        mode.imgFile = 'images/helpScreen.jpg'
        mode.img = mode.scaleImage(mode.loadImage(mode.imgFile), 0.5)

        #image from https://community.cmu.edu/servlet/servlet.FileDownload?file=00P2S000017yveKUAQ
        mode.kosbieFile = 'images/kosbie.png'
        mode.kosbie = mode.scaleImage(mode.loadImage(mode.kosbieFile), 0.2)
        #idea for image.size from https://tinyurl.com/rolo7tz
        mode.kosbieWidth, mode.kosbieHeight = mode.kosbie.size

    def mousePressed(mode, event):
        if ((mode.app.width*1/2-mode.kosbieWidth/2 <= event.x <= (mode.app.width*1/2 + mode.kosbieWidth/2)) and
            (mode.app.height*4/5-mode.kosbieHeight/2 <= event.y <= (mode.app.height*4/5 + mode.kosbieHeight/2))):
            mode.app.setActiveMode(mode.app.gameMode)

    #from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html
    def rgbString(mode, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def redrawAll(mode, canvas):
        color = mode.rgbString(252,152,3)
        text = '''
        Rules: Same as regular chess EXCEPT...
        if there is a capture available, the ONLY move is to capture
        first one to lose all pieces wins!
        \n
        Touch Prof. Kosbie for good luck (or if you wanna play this game)
        '''
        canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill = color)

        #font idea from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html#sizingText
        canvas.create_text(mode.app.width/2, mode.app.height*4/9,
                           text=text, font="Helvetica 20 ")
        canvas.create_text(mode.app.width/2, mode.app.height*1/6,
                           text='Help Menu', font="Helvetica 60 bold")

        #each of the four help images
        canvas.create_image(mode.app.width*1/6, mode.app.height*1/6,
                            image=ImageTk.PhotoImage(mode.img))
        canvas.create_image(mode.app.width*5/6, mode.app.height*1/6,
                            image=ImageTk.PhotoImage(mode.img))
        canvas.create_image(mode.app.width*1/6, mode.app.height*5/6,
                            image=ImageTk.PhotoImage(mode.img))
        canvas.create_image(mode.app.width*5/6, mode.app.height*5/6,
                            image=ImageTk.PhotoImage(mode.img))

        canvas.create_image(mode.app.width*1/2, mode.app.height*4/5,
                            image=ImageTk.PhotoImage(mode.kosbie))

from tkinter import *
from PIL import Image, ImageTk
from pieces import *
from board import *

class GameMode(Mode):
    def appStarted(mode):
        mode.emptyBoard = [[None] * 8 for i in range(8)]  # initialize board
        mode.board = Board(600, mode.emptyBoard)
        mode.regularBoard()
        mode.pieceSelected = None
        mode.color = 'white'
        mode.totalPieces, mode.whitePieces, mode.blackPieces = 32, 16, 16
        mode.totalMoves = []
        mode.movesList = []
        mode.player = True
        mode.doubleAI = False
        mode.isRandoAI = False
        mode.isMinimaxAI = False
        mode.winColor = None
        mode.gameOver = False
        #is there a draw (tie)
        mode.draw = False
        mode.help = False
        mode.seeFinalBoard = False
        #user input idea from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#ioMethods
        mode.app.timerDelay = mode.getUserInput('Timer Delay: ')
        mode.imgFile = 'images/endgame.png'
        mode.img = mode.scaleImage(mode.loadImage(mode.imgFile), 0.5)

    def regularBoard(mode):
        #pawns
        for i in range(0, 8):
            mode.board.board[6][i] = Pawn(
                (6, i), mode.board.size, mode.board.board, 'white', 5)
            mode.board.board[1][i] = Pawn(
                (1, i), mode.board.size, mode.board.board, 'black', -5)

        # white pieces
        mode.board.board[7][0] = Rook(
            (7, 0), mode.board.size, mode.board.board, 'white', 50)
        mode.board.board[7][1] = Knight(
            (7, 1), mode.board.size, mode.board.board, 'white', 25)
        mode.board.board[7][2] = Bishop(
            (7, 2), mode.board.size, mode.board.board, 'white', 15)
        mode.board.board[7][3] = Queen(
            (7, 3), mode.board.size, mode.board.board, 'white', 100)
        mode.board.board[7][4] = King(
            (7, 4), mode.board.size, mode.board.board, 'white', 10)
        mode.board.board[7][5] = Bishop(
            (7, 5), mode.board.size, mode.board.board, 'white', 15)
        mode.board.board[7][6] = Knight(
            (7, 6), mode.board.size, mode.board.board, 'white', 25)
        mode.board.board[7][7] = Rook(
            (7, 7), mode.board.size, mode.board.board, 'white', 50)

        # black pieces
        mode.board.board[0][0] = Rook(
            (0, 0), mode.board.size, mode.board.board, 'black', -50)
        mode.board.board[0][1] = Knight(
            (0, 1), mode.board.size, mode.board.board, 'black', -25)
        mode.board.board[0][2] = Bishop(
            (0, 2), mode.board.size, mode.board.board, 'black', -15)
        mode.board.board[0][3] = Queen(
            (0, 3), mode.board.size, mode.board.board, 'black', -100)
        mode.board.board[0][5] = Bishop(
            (0, 5), mode.board.size, mode.board.board, 'black', -10)
        mode.board.board[0][6] = Knight(
            (0, 6), mode.board.size, mode.board.board, 'black', -15)
        mode.board.board[0][7] = Rook(
            (0, 7), mode.board.size, mode.board.board, 'black', -25)
        mode.board.board[0][4] = King(
            (0, 4), mode.board.size, mode.board.board, 'black', -50)

    def demoBoard(mode):
        #get rid of pawns
        for i in range(0, 8):
            mode.board.board[6][i] = None
            mode.board.board[1][i] = None

    def mousePressed(mode, event):
        if mode.randomButtonBounds(event.x, event.y):
            mode.isRandoAI = not mode.isRandoAI
        elif mode.minimaxButtonBounds(event.x, event.y):
            mode.isMinimaxAI = not mode.isMinimaxAI
        elif mode.doubleAIButtonBounds(event.x, event.y):
            mode.doubleAI = not mode.doubleAI
        elif mode.player:
            #get total moves
            mode.antichessTotalMoves()
            #make copies of the board and # of pieces to check at end of method
            prevBoard = copy.deepcopy(mode.board.board)
            totalPiecesCopy = mode.totalPieces
            #mouse click is in bounds of the board
            if(0 <= event.x < 600 and 0 <= event.y<600):
                mode.board.getCell(event.x, event.y)
            row, col = mode.board.selectedPosition[0], mode.board.selectedPosition[1]
            #no previous selection
            if mode.pieceSelected is None:
                mode.pieceSelected = mode.board.board[row][col]
            #a piece has been selected
            else:
                prevRow, prevCol = mode.pieceSelected.location
                #only move pieces of the color of the current turn
                if mode.board.board[prevRow][prevCol].color == mode.color:
                    if (row, col) not in mode.board.board[prevRow][prevCol].moves():
                        #not a legal move, so change nothing
                        mode.board.board[prevRow][prevCol] = mode.pieceSelected
                    else:
                        if mode.isThereACapture():
                            canCapturePieces = mode.whichPiecesCanCapture()
                            if mode.board.board[prevRow][prevCol] in canCapturePieces:
                                mode.totalPieces -= 1
                                #update the board with the capture
                                mode.board.board[row][col] = mode.pieceSelected
                                #make the previous location empty
                                mode.board.board[prevRow][prevCol] = None
                                #update the piece's location
                                mode.pieceSelected.location = (row, col)
                        #no captures available
                        else:
                            #selected space on board is empty
                            if mode.board.board[row][col] is None:
                                mode.board.board[row][col] = mode.pieceSelected
                                mode.board.board[prevRow][prevCol] = None
                                mode.pieceSelected.location = (row, col)
                #clear the selection and selected piece
                mode.board.selectedPosition = (-1, -1)
                mode.pieceSelected = None
            #change turn only if board has changed
            if mode.hasBoardChanged(prevBoard, mode.board.board, totalPiecesCopy, mode.totalPieces, mode.color):
                if mode.color == 'white':
                    mode.color = 'black'
                else:
                    mode.color = 'white'
        if mode.draw:
            mode.seeFinalBoard = True
        elif mode.gameOver:
            mode.seeFinalBoard = True

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMenu)
        elif event.key == 'a':
            mode.demoBoard()
        elif event.key == 's':
            mode.appStarted()
        else:
            #only display superhelp once
            if not mode.help:
                mode.superhelp()
            mode.help = True

    def superhelp(mode):
        superhelp = '''Rules: Same as regular chess EXCEPT...
        if there is a capture available, the ONLY move is to capture
        first one to lose all pieces wins!
        \n
        Touch Prof. Kosbie for good luck (or if you wanna play this game)
        '''
        print(superhelp)

    def checkDraw(mode):
        x = 1
        for row in range(len(mode.board.board)):
            for piece in mode.board.board[row]:
                if isinstance(piece, Piece) and piece.color == mode.color:
                    if piece.moves() != []:
                        x += 1
        #no possible moves for any of the pieces of the current turn's color
        if x==1:
            mode.draw = True
        else:
            mode.draw = False

    def timerFired(mode):
        if not mode.gameOver and not mode.draw:
            if mode.isRandoAI:
                mode.randoAI()
            elif mode.isMinimaxAI:
                mode.minimaxAI()
            elif mode.doubleAI:
                mode.doubleMinimaxAI()

    def randoAI(mode):
        #same logic as two player, but with a random piece and move
        mode.antichessTotalMoves()
        if mode.color == 'black':
            prevBoard = copy.deepcopy(mode.board.board)
            totalPiecesCopy = mode.totalPieces
            try:
                aiPiece, aiMove = mode.randomAIMove()
                if isinstance(aiPiece[1], list):
                    row, col = aiPiece[1][random.randint(
                        0, len(aiPiece[1]) - 1)]
                else:
                    row, col = aiPiece[1]
                prevRow, prevCol = aiPiece[0]
                prevPiece = mode.board.board[prevRow][prevCol]
                mode.prevPiece = prevPiece
                if mode.isThereACapture():
                    canCapturePieces = mode.whichPiecesCanCapture()
                    if prevPiece in canCapturePieces:
                        mode.totalPieces -= 1
                        if(row, col in prevPiece.moves()):
                            mode.board.board[row][col] = prevPiece
                            mode.prevPiece = prevPiece
                            mode.board.board[prevRow][prevCol] = None
                            mode.currPiece = prevPiece
                            prevPiece.location = (row, col)
                        else:
                            mode.board.board[prevRow][prevCol] = prevPiece
                            prevPiece.location = prevRow, prevCol
                else:
                    if mode.board.board[row][col] is None:
                        mode.board.board[row][col] = prevPiece
                        mode.board.board[prevRow][prevCol] = None
                        if prevPiece is not None:
                            prevPiece.location = (row, col)

                if mode.hasBoardChanged(prevBoard, mode.board.board, totalPiecesCopy, mode.totalPieces, mode.color):
                    mode.color = 'white'
            except:
                mode.draw = True

    def numPieces(mode):
        whitePieceCount = 0
        blackPieceCount = 0
        for row in range(len(mode.board.board)):
            for piece in mode.board.board[row]:
                if isinstance(piece, Piece):
                    if piece.color == 'white':
                        whitePieceCount += 1
                    else:
                        blackPieceCount += 1
        mode.whitePieces = whitePieceCount
        mode.blackPieces = blackPieceCount

    def hasBoardChanged(mode, prevBoard, currBoard, totalPiecesCopy, totalPieces, color):
        # a capture has happened
        if totalPiecesCopy != totalPieces:
            return True
        else:
            for r in range(len(currBoard)):
                for c in range(len(currBoard[0])):
                    if currBoard[r][c] is not None:
                        if currBoard[r][c].color == color:
                            if prevBoard[r][c] is None:
                                return True
            return False

    def isThereACapture(mode):
        for row in range(len(mode.board.board)):
            for piece in mode.board.board[row]:
                if isinstance(piece, Piece) and piece.color == mode.color:
                    if piece.canCapture:
                        return True
        return False

    def whichPiecesCanCapture(mode):
        pieces = []
        if mode.isThereACapture():
            for row in range(len(mode.board.board)):
                for piece in mode.board.board[row]:
                    if isinstance(piece, Piece) and piece.color == mode.color:
                        if piece.canCapture:
                            pieces.append(piece)
        return pieces

    def captures(mode):
        pieces = mode.whichPiecesCanCapture()
        movesList = []
        capturesList = []
        for piece in pieces:
            x,y = piece.location
            movesList.append((mode.board.board[x][y], piece.location,
                             piece.moves()))
            for move in piece.moves():
                x,y = move
                capturesList.append(mode.board.board[x][y])
        return movesList, capturesList

    def antichessTotalMoves(mode):
        mode.totalMoves = []
        for row in range(len(mode.board.board)):
            for piece in mode.board.board[row]:
                if isinstance(piece, Piece) and piece.color == mode.color:
                    if piece.moves() != []:
                        mode.totalMoves.append((piece.location, piece.moves()))
        if mode.totalMoves != []:
            return mode.totalMoves
        else:
            #no possible moves left
            mode.gameOver = True

    def randomMove(mode, movesList):
        if not mode.draw and not mode.gameOver:
            try:
                pieceIndex = random.randint(0, len(movesList) - 1)
                moveIndex = random.randint(0, len(movesList[pieceIndex]) - 1)
                return movesList[pieceIndex], movesList[pieceIndex][moveIndex]
            #means that there are no possible moves left because it is draw
            except:
                mode.gameOver = True
                mode.draw = True

    def randomAIMove(mode):
        if not mode.draw and not mode.gameOver:
            try:
                piece, move = mode.randomMove(mode.antichessTotalMoves())
                return piece, move
            except:
                #means that there are no possible moves left because it is draw
                mode.gameOver = True
                mode.draw = True

    #from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html
    def rgbString(mode, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def highlightingPieces(mode, canvas):
        goodGreen = mode.rgbString(113, 227, 104)
        for row in range(8):
            for col in range(8):
                (x0, y0, x1, y1) = mode.board.getCellBounds(row, col)
                if(mode.board.board[row][col] != None):
                    if mode.isThereACapture():
                        for piece in mode.whichPiecesCanCapture():
                            if piece == mode.pieceSelected:
                                #only highlight for pieces of the current turn's color
                                if mode.pieceSelected.color == mode.color:
                                    for move in piece.moves():
                                        (x,y) = move
                                        #only highlight for piece that is selected
                                        if (row, col) == mode.board.selectedPosition:
                                            x1, y1, x2, y2 = mode.board.getCellBounds(x, y)
                                            canvas.create_rectangle(x1, y1, x2, y2, fill=goodGreen)
                    else:
                        for move in mode.board.board[row][col].moves():
                            if mode.board.board[row][col].color == mode.color:
                                (x, y) = move
                                if (row, col) == mode.board.selectedPosition:
                                    x1, y1, x2, y2 = mode.board.getCellBounds(x, y)
                                    canvas.create_rectangle(
                                        x1, y1, x2, y2, fill=goodGreen)

    def minimaxAI(mode):
        mode.antichessTotalMoves()
        if mode.color == 'black':
            prevBoard = copy.deepcopy(mode.board.board)
            totalPiecesCopy = mode.totalPieces
            try:
                piece, move = mode.randomMove(mode.antichessTotalMoves())
            except:
                #mode.gameOver = True
                mode.draw = True
            if isinstance(piece[1], list):
                row, col = piece[1][random.randint(
                    0, len(piece[1]) - 1)]
            else:
                row, col = piece[1]
            prevRow, prevCol = piece[0]
            prevPiece = mode.board.board[prevRow][prevCol]
            if mode.isThereACapture():
                movesList, capturesList = mode.captures()
                mode.movesList = movesList
                #find optimal move with minimax algorithm
                row,col = mode.minimax(capturesList)
                for item in movesList:
                    if((row, col) in item[2]):
                        prevRow, prevCol = item[1]
                        prevPiece = item[0]
                if(row, col in prevPiece.moves()):
                    mode.totalPieces -= 1
                    mode.board.board[row][col] = prevPiece
                    mode.board.board[prevRow][prevCol] = None
                    prevPiece.location = (row, col)
                else:
                    mode.totalPieces -= 1
                    mode.board.board[prevRow][prevCol] = prevPiece
                    prevPiece.location = prevRow, prevCol
            else:
                if mode.board.board[row][col] is None:
                    mode.board.board[row][col] = prevPiece
                    mode.board.board[prevRow][prevCol] = None
                    if prevPiece is not None:
                        prevPiece.location = (row, col)

            if mode.hasBoardChanged(prevBoard, mode.board.board, totalPiecesCopy, mode.totalPieces, mode.color):
                mode.color = 'white'
    #finds piece with the smallest value that can be captured, given a list of possible pieces to capture
    def minimax(mode, piecesList):
        minValue = 200
        minPiece = None
        for piece in piecesList:
            if piece.value < minValue:
                minValue = piece.value
                minPiece = piece
        return minPiece.location

    def minimaxCaptures(mode, canvas):
        moveString = ''
        for move in mode.movesList:
            move0string = 'Piece: ' + str(move[0])
            move1string = 'Piece was located at: ' + str(move[1])
            move2string = 'Location of Captures: ' + str(move[2][0])
            moveString += move0string + '\n' + move1string + '\n' + move2string + '\n'
            moveString += '\n'
        canvas.create_text(mode.app.width*7/9,
                           mode.app.height*3/8, text=moveString)
        canvas.create_text(mode.app.width*7/9,
                           mode.app.height/8, text='Potential Capture(s)')

    def doubleMinimaxAI(mode):
        mode.antichessTotalMoves()
        prevBoard = copy.deepcopy(mode.board.board)
        totalPiecesCopy = mode.totalPieces
        #continue to go back and forth until either a draw or win
        try:
            piece, move = mode.randomMove(mode.antichessTotalMoves())
            if isinstance(piece[1], list):
                row, col = piece[1][random.randint(
                    0, len(piece[1]) - 1)]
            else:
                row, col = piece[1]
            prevRow, prevCol = piece[0]
            prevPiece = mode.board.board[prevRow][prevCol]
            if mode.isThereACapture():
                movesList, capturesList = mode.captures()
                mode.movesList = movesList
                row, col = mode.minimax(capturesList)
                for item in movesList:
                    if((row, col) in item[2]):
                        prevRow, prevCol = item[1]
                        prevPiece = item[0]
                if(row, col in prevPiece.moves()):
                    mode.totalPieces -= 1
                    mode.board.board[row][col] = prevPiece
                    mode.board.board[prevRow][prevCol] = None
                    prevPiece.location = (row, col)
                else:
                    mode.totalPieces -= 1
                    mode.board.board[prevRow][prevCol] = prevPiece
                    prevPiece.location = prevRow, prevCol
            else:
                if mode.board.board[row][col] is None:
                    mode.board.board[row][col] = prevPiece
                    mode.board.board[prevRow][prevCol] = None
                    if prevPiece is not None:
                        prevPiece.location = (row, col)

            if mode.hasBoardChanged(prevBoard, mode.board.board, totalPiecesCopy, mode.totalPieces, mode.color):
                if mode.color == 'white':
                    mode.color = 'black'
                else:
                    mode.color = 'white'
        except:
            mode.gameOver = True
            mode.draw = True

    def randomButtonBounds(mode, x, y):
        return ((mode.app.width*6/9 <= x <= mode.app.width*6/9 + 100) and
                (mode.app.height*3/5 <= y <= mode.app.height*3/5 + 30))

    def minimaxButtonBounds(mode, x, y):
        return ((mode.app.width*6/9 <= x <= mode.app.width*6/9 + 100) and
                (mode.app.height*3/5+40 <= y <= mode.app.height*3/5+70))

    def doubleAIButtonBounds(mode, x, y):
        return ((mode.app.width*6/9 <= x <= mode.app.width*6/9 + 100) and
                (mode.app.height*3/5+80<= y <= mode.app.height*3/5 + 110))

    def redrawAll(mode, canvas):
        mode.numPieces()
        #either white or black has won
        if mode.whitePieces == 0 or mode.blackPieces == 0:
            mode.gameOver = True
        if not mode.gameOver:
            mode.board.draw(canvas)
            mode.highlightingPieces(canvas)
            canvas.create_rectangle(600, 0, mode.app.width, mode.app.height, fill = 'sky blue')
            if mode.isMinimaxAI or mode.doubleAI:
                mode.minimaxCaptures(canvas)

            canvas.create_text(mode.app.width*7/9,
                               mode.app.height/20, text= f'Player Turn: {mode.color}',
                               font = 'Times 20')

            canvas.create_text(mode.app.width*7/9,
                               mode.app.height*15/16, text='Press s to reset!',
                               font = 'Times 26')
            canvas.create_text(mode.app.width*3/4,
                               mode.app.height*3/5-20, text= 'Toggle AI on/off',
                               font = 'Times 20')

            canvas.create_rectangle(mode.app.width*6/9,
                                    mode.app.height*3/5,
                                    mode.app.width*6/9 + 100,
                                    mode.app.height*3/5 + 30,
                                    fill = 'red')
            canvas.create_text(mode.app.width*6/9 + 50,
                               mode.app.height*3/5 + 15, text=f'Random AI',
                               font='Times 20')

            canvas.create_rectangle(mode.app.width*6/9,
                                    mode.app.height*3/5+40,
                                    mode.app.width*6/9 + 100,
                                    mode.app.height*3/5 + 70,
                                    fill='teal')
            canvas.create_text(mode.app.width*6/9 + 50,
                               mode.app.height*3/5 + 55, text=f'Minimax AI',
                               font='Times 20')

            canvas.create_rectangle(mode.app.width*6/9,
                                    mode.app.height*3/5+80,
                                    mode.app.width*6/9 + 100,
                                    mode.app.height*3/5 + 110,
                                    fill='green')
            canvas.create_text(mode.app.width*6/9 + 50,
                               mode.app.height*3/5 + 95, text=f'Double AI',
                               font='Times 20')
        elif mode.draw:
            if not mode.seeFinalBoard:
                canvas.create_rectangle(0,0,mode.app.width,mode.app.height,
                    fill = 'yellow')
                #font idea from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html#sizingText
                canvas.create_text(mode.app.width/2, mode.app.height*1/12,
                                text='It is a Draw!',
                                font="Times 30 bold",
                                fill = 'green')
                canvas.create_text(mode.app.width/2, mode.app.height*11/12,
                                   text='Click to see the final board state!',
                                   font="Times 30 bold",
                                   fill='green')
                #image from https://tinyurl.com/rsulvtg
                canvas.create_image(mode.app.width/2, mode.app.height/2,
                            image=ImageTk.PhotoImage(mode.img))
            else:
                #display final board state
                mode.board.draw(canvas)
                canvas.create_text(mode.app.width*7/9,
                                   mode.app.height/12, text='DRAW! \nPress s to restart!',
                                   font = 'Times 20 bold')
        else:
            if not mode.seeFinalBoard:
                if mode.whitePieces == 0:
                    canvas.create_rectangle(0,0,mode.app.width,mode.app.height,
                    fill = 'grey')
                    #font idea from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html#sizingText
                    canvas.create_text(mode.app.width/2, mode.app.height*1/12,
                                    text='White has won the game!',
                                    font="Helvetica 30 bold",
                                    fill = 'white')
                    canvas.create_text(mode.app.width/2, mode.app.height*11/12,
                                       text='Click to see the final board state!',
                                       font="Times 30 bold",
                                       fill='green')
                    #image from https://tinyurl.com/rsulvtg
                    canvas.create_image(mode.app.width/2, mode.app.height/2,
                                image=ImageTk.PhotoImage(mode.img))
                elif mode.blackPieces == 0:
                    #font idea from https://www.cs.cmu.edu/~112/notes/notes-graphics-part2.html#sizingText
                    canvas.create_text(mode.app.width/2, mode.app.height*1/12,
                                    text='Black has won the game!',
                                    font="Helvetica 30 bold")
                    canvas.create_text(mode.app.width/2, mode.app.height*11/12,
                                       text='Click to see the final board state!',
                                       font="Times 30 bold",
                                       fill='green')
                    #image from https://tinyurl.com/rsulvtg
                    canvas.create_image(mode.app.width/2, mode.app.height/2,
                                        image=ImageTk.PhotoImage(mode.img))
                else:
                    canvas.create_image(mode.app.width/2, mode.app.height/2,
                                        image=ImageTk.PhotoImage(mode.img))
                    canvas.create_text(mode.app.width*7/9,
                                       mode.app.height/4, text='Press s to restart!',
                                       font='Times 20 bold')
            else:
                #display final board state
                mode.board.draw(canvas)
                canvas.create_text(mode.app.width*4/5,
                                   mode.app.height*11/12, text='Press s to restart!',
                                   font = 'Times 20 bold')

ChessGame(width=1000, height=600)
