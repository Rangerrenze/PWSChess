import pygame as p
import ChessMoveGen
import ChessEngine
import timeit

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

global blackAIrule, whiteAIrule, playerPlayingrule, castleRule, antiChess
blackAIrule = False
whiteAIrule = True
playerPlayingrule = True
castleRule = True
antiChess = True

def loadImages():
    pieces = {'wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Images/' + piece + '.png'), ((SQ_SIZE) ,(SQ_SIZE)))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    if ChessEngine.GameState().gameOver:
        gameOver = True

    while running:
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)

        p.display.flip()
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    if ChessEngine.GameState().gameOver:
                        gameOver = True
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessMoveGen.Move(playerClicks[0], playerClicks[1], gs.board)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(validMoves)
                                print(ChessMoveGen.Move.getChessnotation(move))
                                print("ChessMain castling test", ChessEngine.GameState().castlingCopy)
                                print("Speedtest start")
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                drawGameState(screen, gs, validMoves, sqSelected)
                                p.display.update()

                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if not gs.WhiteToMove and blackAIrule:
            if not gs.gameOver:
                AIMove = gs.aiMove()
                if AIMove == None:
                    print("None error")
                    gameOver = True
                    gs.gameOver = True
                else:
                    gs.makeMove(AIMove)
                    moveMade = True
                    animate = True
                    print(ChessMoveGen.Move.getChessnotation(AIMove))
                    print("Move: White")




        if gs.WhiteToMove and whiteAIrule:
            if not gs.gameOver:
                AIMove = gs.aiMove()
                if AIMove == None:
                    print("None error")
                    gameOver = True
                    gs.gameOver = True
                else:
                    gs.makeMove(AIMove)
                    moveMade = True
                    animate = True
                    print(ChessMoveGen.Move.getChessnotation(AIMove))
                    print("Move: Black")

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False



def highlightSquares(screen, gs, validMoves, sqSelected):
    if not gs.gameOver:
        if len(sqSelected) > 0:
            r, c = sqSelected
            if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color('yellow'))
                screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
                s.fill(p.Color("red"))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global Colors
    Colors = [p.Color("#ebc28e"), p.Color("#89420B")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            Color = Colors[((r+c)%2)]
            p.draw.rect(screen, Color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global Colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = Colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()




