#-------------------------------------------------------------------------------
# Name:        Iagno.py
# Purpose:
#
# Author:      Ganesh Zilpe
#
# Created:     11/06/2015
# Copyright:   (c) Ganesh Zilpe 2015
# Licence:     Freely Available
#-------------------------------------------------------------------------------
import random, pygame, sys, Buttons
from pygame.locals import *

WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 8 # number of columns of icons
BOARDHEIGHT = 8 # number of rows of icons

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
BLACK    = (  0, 0, 0)
RED     =  (128,0,0)

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

CIRCLE = 'circle'


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == CIRCLE:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half)



def drawBoard(board):
      # This function prints out the board that it was passed. Returns None.
      for boxx in range(BOARDWIDTH):
          #print "boxx: ",boxx
          for boxy in range(BOARDHEIGHT):
              left, top = leftTopCoordsOfBox(boxx, boxy)
              if board[boxx][boxy] == ' ':
                  # draw background tile
                  pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))
              elif board[boxx][boxy] == 'X': #for user
                  # draw user circular tile on the square background tile
                  pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))
                  drawIcon(CIRCLE, BLACK, boxx, boxy)
              else:
                  # draw computer circular tile on the square background tile
                  pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))
                  drawIcon(CIRCLE, WHITE, boxx, boxy)



def resetBoard(board):
      # Reset the setting of the board
      for x in range(8):
          for y in range(8):
              board[x][y] = ' '
      # Starting pieces:
      board[3][3] = 'X'
      board[3][4] = 'O'
      board[4][3] = 'O'
      board[4][4] = 'X'


def getNewBoard():
      # Creates a brand new, blank board data structure.
      board = []
      for i in range(8):
          board.append([' '] * 8)
      return board


def isValidMove(board, tile, xstart, ystart):
      # Returns False if the player's move on space xstart, ystart is invalid.
      # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
      if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
          return False

      board[xstart][ystart] = tile # temporarily set the tile on the board.

      if tile == 'X':
         otherTile = 'O'
      else:
          otherTile = 'X'

      tilesToFlip = []
      for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
          x, y = xstart, ystart
          x += xdirection # first step in the direction
          y += ydirection # first step in the direction
          if isOnBoard(x, y) and board[x][y] == otherTile:
              # There is a piece belonging to the other player next to our piece.
              x += xdirection
              y += ydirection
              if not isOnBoard(x, y):
                  continue
              while board[x][y] == otherTile:
                  x += xdirection
                  y += ydirection
                  if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                      break
              if not isOnBoard(x, y):
                  continue
              if board[x][y] == tile:
                  # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                  while True:
                      x -= xdirection
                      y -= ydirection
                      if x == xstart and y == ystart:
                          break
                      tilesToFlip.append([x, y])

      board[xstart][ystart] = ' ' # restore the empty space
      if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
          return False
      return tilesToFlip


def isOnBoard(x, y):
      # Returns True if the coordinates are located on the board.
      return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
      # Returns a new board with . marking the valid moves the given player can make.
      dupeBoard = getBoardCopy(board)

      for x, y in getValidMoves(dupeBoard, tile):
         dupeBoard[x][y] = '.'
      return dupeBoard


def getValidMoves(board, tile):
     # Returns a list of [x,y] lists of valid moves for the given player on the given board.
     validMoves = []

     for x in range(8):
         for y in range(8):
             if isValidMove(board, tile, x, y) != False:
                 validMoves.append([x, y])
     return validMoves


def getScoreOfBoard(board):
     # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
     xscore = 0
     oscore = 0
     for x in range(8):
         for y in range(8):
             if board[x][y] == 'X':
                 xscore += 1
             if board[x][y] == 'O':
                 oscore += 1
     return {'X':xscore, 'O':oscore}


def enterPlayerTile():
     # Lets the player type which tile they want to be.
     # Returns a list with the player's tile as the first item, and the computer's tile as the second.
     tile = ''
     while not (tile == 'X' or tile == 'O'):
         print('Do you want to be X or O?')
         tile = input().upper()

     # the first element in the list is the player's tile, the second is the computer's tile.
     if tile == 'X':
         return ['X', 'O']
     else:
         return ['O', 'X']


def whoGoesFirst():
     # Randomly choose the player who goes first.
     if random.randint(0, 1) == 0:
         return 'computer'
     else:
         return 'player'


def playAgain():
     # This function returns True if the player wants to play again, otherwise it returns False.
     print('Do you want to play again? (yes or no)')
     return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
     # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
     # Returns False if this is an invalid move, True if it is valid.
     tilesToFlip = isValidMove(board, tile, xstart, ystart)

     if tilesToFlip == False:
         return False

     board[xstart][ystart] = tile
     for x, y in tilesToFlip:
         board[x][y] = tile
     return True


def getBoardCopy(board):
     # Make a duplicate of the board list and return the duplicate.
     dupeBoard = getNewBoard()

     for x in range(8):
         for y in range(8):
             dupeBoard[x][y] = board[x][y]

     return dupeBoard


def isOnCorner(x, y):
     # Returns True if the position is in one of the four corners.
     return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
     # Let the player type in their move.
     # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
     DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
     while True:
         print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
         move = input().lower()
         if move == 'quit':
             return 'quit'
         if move == 'hints':
             return 'hints'

         if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
             x = int(move[0]) - 1
             y = int(move[1]) - 1
             if isValidMove(board, playerTile, x, y) == False:
                 continue
             else:
                 break
         else:
             print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
             print('For example, 81 will be the top-right corner.')

     return [x, y]


def getComputerMove(board, computerTile):
     # Given a board and the computer's tile, determine where to
     # move and return that move as a [x, y] list.
     possibleMoves = getValidMoves(board, computerTile)

     # randomize the order of the possible moves
     random.shuffle(possibleMoves)

     # always go for a corner if available.
     for x, y in possibleMoves:
         if isOnCorner(x, y):
             return [x, y]

     # Go through all the possible moves and remember the best scoring move
     bestScore = -1
     for x, y in possibleMoves:
         dupeBoard = getBoardCopy(board)
         makeMove(dupeBoard, computerTile, x, y)
         score = getScoreOfBoard(dupeBoard)[computerTile]
         if score > bestScore:
             bestMove = [x, y]
             bestScore = score
     return bestMove

def showPoints(playerTile, computerTile):
     # Prints out the current score.
     scores = getScoreOfBoard(mainBoard)
     #print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))
     return (scores[playerTile], scores[computerTile])

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def displayWarning(visible):
    basicFont = pygame.font.SysFont(None, 20)
    # set up the text
    if visible == "TRUE":
        text = basicFont.render('Warning: Invalid move, Try again', True, WHITE, BLUE)
    else:
        text = basicFont.render('Warning: Invalid move, Try again', True, BGCOLOR, BGCOLOR)
    textRect = text.get_rect()
    textRect.centerx = DISPLAYSURF.get_rect().centerx
    textRect.centery = 10
    DISPLAYSURF.blit(text, textRect)

def displayScore(playerScore, computerScore):
    basicFont = pygame.font.SysFont(None, 25)
    basicFont1 = pygame.font.SysFont(None, 20)
    # set up the text
    score = basicFont.render('Result ', True, WHITE, BLUE)
    score1 = basicFont1.render('Player: '+str(playerScore), True, WHITE, BLUE)
    score2= basicFont1.render('Computer: '+str(computerScore), True, WHITE, BLUE)
    textRect = score.get_rect()
    textRect1 = score1.get_rect()
    textRect2 = score2.get_rect()
    textRect.centery = DISPLAYSURF.get_rect().centery - 30
    textRect.centerx = DISPLAYSURF.get_rect().centerx + (DISPLAYSURF.get_rect().centerx)/2 +(DISPLAYSURF.get_rect().centerx)/4
    textRect1.centery = DISPLAYSURF.get_rect().centery - 10
    textRect1.centerx = DISPLAYSURF.get_rect().centerx + (DISPLAYSURF.get_rect().centerx)/2 +(DISPLAYSURF.get_rect().centerx)/4
    textRect2.centery = DISPLAYSURF.get_rect().centery + 10
    textRect2.centerx = DISPLAYSURF.get_rect().centerx + (DISPLAYSURF.get_rect().centerx)/2 +(DISPLAYSURF.get_rect().centerx)/4
    DISPLAYSURF.blit(score, textRect)
    DISPLAYSURF.blit(score1, textRect1)
    DISPLAYSURF.blit(score2, textRect2)


def displayResult():
    p_score, c_score = showPoints(playerTile, computerTile)
    result = ''
    if p_score > c_score:
         result = 'You beat the computer by %s points! Congratulations!' % (p_score - c_score)
    elif p_score < c_score:
         result = 'You lost. The computer beat you by %s points.' % (c_score - p_score)
    else:
         result = 'The game was a tie!'
    basicFont = pygame.font.SysFont(None, 30)
    basicFont1 = pygame.font.SysFont(None, 20)
    # set up the text
    score = basicFont.render('Result ', True, WHITE, BGCOLOR)
    score1 = basicFont1.render(result, True, WHITE, BGCOLOR)
    score2= basicFont1.render('Do you want to play again', True, WHITE, BGCOLOR)
    textRect = score.get_rect()
    textRect1 = score1.get_rect()
    textRect2 = score2.get_rect()

    y_center = DISPLAYSURF.get_rect().centery
    textRect.centery = y_center - 50
    textRect.centerx = DISPLAYSURF.get_rect().centerx

    textRect1.centery = y_center - 20
    textRect1.centerx = DISPLAYSURF.get_rect().centerx

    textRect2.centery = y_center
    textRect2.centerx = DISPLAYSURF.get_rect().centerx

    DISPLAYSURF.blit(score, textRect)
    DISPLAYSURF.blit(score1, textRect1)
    DISPLAYSURF.blit(score2, textRect2)

    Button_yes = Buttons.Button()
    Button_no = Buttons.Button()
    #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
    Button_yes.create_button(DISPLAYSURF, (107,142,35), DISPLAYSURF.get_rect().centerx - 50, y_center +30, 40,    20,    0,        "Yes", (255,255,255))
    Button_no.create_button(DISPLAYSURF, (107,142,35), DISPLAYSURF.get_rect().centerx +10, y_center +30, 40,    20,    0,        "No", (255,255,255))

    while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if Button_yes.pressed(pygame.mouse.get_pos()):
                        return True
                    elif Button_no.pressed(pygame.mouse.get_pos()):
                        return False


print('Welcome to Iagno!')



#initialize the font
pygame.font.init()

playerTile = 'X'
computerTile = 'O'
pygame.display.set_caption('Iagno')
#while True:
     # Reset the board and game.
while True:
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    mainBoard = getNewBoard()
    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    resetBoard(mainBoard)
    p_score, c_score = showPoints(playerTile, computerTile)
    displayScore(p_score, c_score)
    drawBoard(mainBoard)
    pygame.display.update()



    showHints = False
    turn = whoGoesFirst()
    #mainBoard = getNewBoard()
    # drawBoard(mainBoard)
    #playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            mouseClicked = False
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                for event in pygame.event.get(): # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    #elif event.type == MOUSEMOTION:
                    #    mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouseClicked = True

                #drawBoard(mainBoard)
                #showPoints(playerTile, computerTile)
                #move = getPlayerMove(mainBoard, playerTile)
                #set the tile for the user move
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx != None and boxy != None:
                    if mouseClicked:
                        if isValidMove(mainBoard, playerTile, boxx, boxy) == False:
                            #print "Not Valid Move, Try Again"
                            displayWarning("TRUE")
                            print "something"
                            drawBoard(mainBoard)
                            pygame.display.update()
                            continue

                        makeMove(mainBoard, 'X', boxx, boxy)
                    else:
                        continue
                else:
                    continue
                p_score, c_score = showPoints(playerTile, computerTile)
                displayScore(p_score, c_score)
                displayWarning('')
                drawBoard(mainBoard)
                if getValidMoves(mainBoard, playerTile) == []:
                    pygame.display.update()
                    break
                else:
                    turn = 'computer'
        else:
            # Computer's turn.
            #drawBoard(mainBoard)
            #showPoints(playerTile, computerTile)
            #input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, 'O')
            makeMove(mainBoard, 'O', x, y)
            pygame.time.delay(1000)
            p_score, c_score = showPoints(playerTile, computerTile)
            displayScore(p_score, c_score)
            displayWarning('FALSE')
            drawBoard(mainBoard)
            if getValidMoves(mainBoard, playerTile) == []:
                pygame.display.update()
                break
            else:
                turn = 'player'
        pygame.display.update()




    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    displayResult();
    if displayResult():
        continue
    else:
        pygame.quit()
        sys.exit()


