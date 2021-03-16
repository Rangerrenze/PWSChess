import numpy as np
from copy import deepcopy
import ChessEngine
import ChessMain
import ChessMinimax
import random

# import Algorithm




class MoveGeneration():
    def __init__(self):
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
        self.gameOver = False
        self.WhitetoMove = True
        self.WhiteKingLocation = (7,4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.whiteWin = False
        self.blackWin = False
        self.Minimax = True
        self.minimax = False
        self.forcedCaptures = []
        self.whiteCaptures = []
        self.blackcaptures = []
        # self.castleRights = None
        self.Minimax = False
        self.finalMoves = []
        self.ChessMainCastle = ()
        self.MinimaxCastle = ()

    def getMoves(self, board, WhitetoMove, minimaxMove, castles):
        self.miniMax = minimaxMove
        if self.miniMax:
            self.ChessMainCastle = castles
        else:
            self.ChessMainCastle = castles

        self.board = np.copy(board)
        self.whiteAI = ChessMain.whiteAIrule
        self.blackAI = ChessMain.blackAIrule
        moves = self.getValidMoves(WhitetoMove)
        self.finalMoves = moves
        if ChessMain.antiChess:
            whitePieces = []
            blackPieces = []
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    piece = self.board[r][c]
                    if piece[0] == 'w':
                        whitePieces.append((piece, (r, c)))
                    elif piece[0] == 'b':
                        blackPieces.append((piece, (r, c)))
            if len(moves) == 0 or len(whitePieces) == 1 or len(blackPieces) == 1:
                if len(whitePieces) < len(blackPieces) and self.inCheck:
                    self.gameOver = True
                    self.whiteWin = True
                elif len(blackPieces) < len(whitePieces) and self.inCheck:
                    self.gameOver = True
                    self.blackWin = True
                elif len(whitePieces) < len(blackPieces) and not self.inCheck:
                    self.gameOver = True
                    self.whiteWin = True
                elif len(blackPieces) < len(whitePieces) and not self.inCheck:
                    self.gameOver = True
                    self.blackWin = True
                elif len(blackPieces) == 1:
                    self.gameOver = True
                    self.blackWin = True
                elif len(whitePieces) == 1:
                    self.gameOver = True
                    self.whiteWin = True
                else:
                    self.gameOver = True

                if moves == None:
                    moves = "None Moves"
                return self.finalMoves, self.gameOver, self.whiteWin, self.blackWin
            else:
                return self.finalMoves, self.gameOver, self.whiteWin, self.blackWin
        else:
            WhiteWinMoves = self.getValidMoves(True)
            if len(WhiteWinMoves) < 1:
                if self.inCheck:
                    self.blackWin = True
                    self.whiteWin = False
                    self.gameOver = True
                    return self.finalMoves, self.gameOver, self.whiteWin, self.blackWin
                else:
                    self.blackWin = False
                    self.whiteWin = False
                    self.gameOver = True
                    return self.finalMoves, self.gameOver, self.whiteWin, self.blackWin
            BlackWinMoves = self.getValidMoves(False)
            if len(BlackWinMoves) < 1:
                if self.inCheck:
                    self.blackWin = False
                    self.whiteWin = True
                    self.gameOver = True
                    return self.finalMoves, self.gameOver, self.whiteWin, self.blackWin

            self.blackWin = False
            self.whiteWin = False
            self.gameOver = False
            return  self.finalMoves, self.gameOver, self.whiteWin, self.blackWin



    def getValidMoves(self, WhitetoMove):
        self.WhitetoMove = WhitetoMove
        moves, whiteForcedCaptures, blackForcedCaptures = self.getAllMoves()
        if not self.gameOver:
            self.ForcedCaptureRule = ChessMain.antiChess
            self.forcedCaptures = []
            self.whiteCaptures = []
            self.blackcaptures = []
            if self.ForcedCaptureRule:
                self.whiteCaptures = whiteForcedCaptures
                self.blackcaptures = blackForcedCaptures
                self.forcedCaptures.append(whiteForcedCaptures)
                self.forcedCaptures.append(blackForcedCaptures)
            # print("Captures", forcedCaptures)

            self.inCheck, self.pins, self.checks = self.CheckforPinsandChecks()
            if self.WhitetoMove:
                kingRow = self.WhiteKingLocation[0]
                kingCol = self.WhiteKingLocation[1]
            else:
                kingRow = self.blackKingLocation[0]
                kingCol = self.blackKingLocation[1]
            if self.inCheck:
                print("Checks: ", self.checks)
                if len(self.checks) == 1:
                    check = self.checks[0]
                    checkRow = check[0]
                    checkCol = check[1]
                    pieceChecking = self.board[checkRow][checkCol]
                    validSquares = []
                    if pieceChecking[1] == "N":
                        validSquares.append((checkRow, checkCol))
                    else:
                        for i in range(1, 8):
                            validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                            validSquares.append(validSquare)
                            if validSquare[0] == checkRow and validSquare[1] == checkCol:
                                break
                    for i in range(len(moves) - 1, -1, -1):
                        if moves[i].pieceMoved[1] != "K":
                            if not (moves[i].endRow, moves[i].endCol) in validSquares:
                                moves.remove(moves[i])
                                self.Checkmoves = moves
                else:
                    whiteForcedCaptures = []
                    blackForcedCaptures = []
                    self.getKingMoves(kingRow, kingCol, moves, blackForcedCaptures, whiteForcedCaptures)


            elif len(self.whiteCaptures) > 0 and self.WhitetoMove:
                print("White move and possible capture")
                whiteValidSquares = []
                if self.inCheck:
                    moves = self.Checkmoves
                else:
                    moves = self.getAllMoves()[0]
                for x in range(len(self.whiteCaptures)):
                    whiteValidSquares.append(self.whiteCaptures[x])
                print("White validsquares", whiteValidSquares)
                for i in range(len(moves)-1, -1, -1):
                    if not (moves[i].endRow, moves[i].endCol) in whiteValidSquares:
                        moves.remove(moves[i])
            elif len(self.blackcaptures) > 0 and not self.WhitetoMove:
                blackValidSquares = []
                print("Black move and possible capture")
                if self.inCheck:
                    moves = self.Checkmoves
                else:
                    moves = self.getAllMoves()[0]

                for x in range(len(self.blackcaptures)):
                    blackValidSquares.append(self.blackcaptures[x])
                print("Black validsquares", blackValidSquares)
                for i in range(len(moves)-1, -1, -1):
                    if not (moves[i].endRow, moves[i].endCol) in blackValidSquares:
                        moves.remove(moves[i])
                        # Capturemoves = []
                        #     Capturemoves.append(moves[i])
                        # moves = Capturemoves
            else:
                moves = self.getAllMoves()[0]

            return moves



    def getAllMoves(self):
        moves = []
        whiteForcedCapture = []
        blackForcedCapture = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == "wK":
                    self.WhiteKingLocation = (r, c)
                elif self.board[r][c] == "bK":
                    self.blackKingLocation = (r, c)
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhitetoMove) or (turn == 'b' and not self.WhitetoMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves, whiteForcedCapture, blackForcedCapture)
        return moves, whiteForcedCapture, blackForcedCapture

    def getPawnMoves(self, r, c, moves, whiteForcedCapture, blackForcedCapture):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])

        if self.WhitetoMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r,c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >=0:
                if not piecePinned or pinDirection == (-1, -1):
                    if self.board[r-1][c-1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c-1), self.board))
                        whiteForcedCapture.append((r-1, c-1))

            if c+1 < len(self.board[r]):
                if not piecePinned or pinDirection == (-1, 1):
                    if self.board[r-1][c+1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c+1), self.board))
                        whiteForcedCapture.append((r-1, c+1))

        elif not self.WhitetoMove:
            if not self.WhitetoMove:
                if self.board[r + 1][c] == "--":
                    if not piecePinned or pinDirection == (1, 0):
                        moves.append(Move((r, c), (r + 1, c), self.board))
                        if r == 1 and self.board[r + 2][c] == "--":
                            moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:
                    if self.board[r + 1][c - 1][0] == 'w':
                        if not piecePinned or pinDirection == (1, -1):
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                            blackForcedCapture.append((r+1, c-1))
                if c + 1 < len(self.board[r]):
                    if self.board[r + 1][c + 1][0] == 'w':
                        if not piecePinned or pinDirection == (1, 1):
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))
                            blackForcedCapture.append((r+1, c+1))
    def getRookMoves(self, r, c, moves, whiteForcedCaptures, blackForcedCaptures):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.WhitetoMove else "w"
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol <8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":
                            moves.append(Move((r, c), (endrow, endcol), self.board))
                        elif endpiece[0] == enemyColor:
                            moves.append(Move((r, c), (endrow, endcol), self.board))
                            if self.WhitetoMove:
                                whiteForcedCaptures.append((endrow, endcol))
                            elif not self.WhitetoMove:
                                blackForcedCaptures.append((endrow, endcol))
                            break
                        else:
                            break
                    else:
                        break

    def getBishopMoves(self, r, c, moves, whiteForcedCaptures, blackForcedCaptures):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.WhitetoMove else "w"
        enemyColor = "b" if self.WhitetoMove else "w"
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":
                            moves.append(Move((r, c), (endrow, endcol), self.board))
                        elif endpiece[0] == enemyColor:
                            moves.append(Move((r, c), (endrow, endcol), self.board))
                            if self.WhitetoMove:
                                whiteForcedCaptures.append((endrow, endcol))
                            elif not self.WhitetoMove:
                                blackForcedCaptures.append((endrow, endcol))
                            break
                        else:
                            # friendly piece
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves, whiteForcedCaptures, blackForcedCaptures):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        allyColor = "w" if self.WhitetoMove else "b"
        enemyColor = "b" if self.WhitetoMove else "w"
        for m in knightMoves:
            endrow = r + m[0]
            endcol = c + m[1]
            if 0 <= endrow < 8 and 0 <= endcol <8:
                if not piecePinned:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] != allyColor:
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        if endpiece[0] == enemyColor:
                            if self.WhitetoMove:
                                whiteForcedCaptures.append((endrow, endcol))
                            elif not self.WhitetoMove:
                                blackForcedCaptures.append((endrow, endcol))

    def getKingMoves(self, r, c, moves, whiteForcedCaptures, blackForcedCaptures):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.WhitetoMove else "b"
        enemyColor = "b" if self.WhitetoMove else "w"
        for i in range(8):
            endrow = r + rowMoves[i]
            endcol = c + colMoves[i]
            if 0 <= endrow < 8 and 0 <= endcol <8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allyColor:
                    if allyColor == 'w':
                        self.WhiteKingLocation = (endrow, endcol)
                    else:
                        self.blackKingLocation = (endrow, endcol)
                    inCheck, pins, checks, = self.CheckforPinsandChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        if endpiece[0] == enemyColor:
                            if self.WhitetoMove:
                                whiteForcedCaptures.append((endrow, endcol))
                            elif not self.WhitetoMove:
                                blackForcedCaptures.append((endrow, endcol))
                    if allyColor == 'w':
                        self.WhiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        if ChessMain.castleRule:
            self.getCastleMoves(r, c, moves)

    def squareUnderAttack(self, r, c):
        enemyColor = "b" if self.WhitetoMove else "w"
        possiblePin = ()
        attacks = []
        startRow = r
        startCol = c
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != enemyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or  (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == "K"):
                            if possiblePin == ():
                                attacks.append("possible attack")
                                break
                            else:
                                break
                        else:
                            break

                else:
                    break
        if len(attacks) != 0:
            return True
        else:
            return False



    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        print("MoveGenCastle = ", self.ChessMainCastle)
        if (self.WhitetoMove and self.ChessMainCastle[0]) or (not self.WhitetoMove and self.ChessMainCastle[2]):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.WhitetoMove and self.ChessMainCastle[1]) or (not self.WhitetoMove and self.ChessMainCastle[3]):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if not c >= 6:
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                    moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if not c < 3:
            if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
                if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                    moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

    def getQueenMoves(self, r, c, moves, whiteForcedCaptures, blackForcedCaptures):
        self.getRookMoves(r, c, moves, whiteForcedCaptures, blackForcedCaptures)
        self.getBishopMoves(r, c, moves, whiteForcedCaptures, blackForcedCaptures)


    def CheckforPinsandChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.WhitetoMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.WhiteKingLocation[0]
            startCol = self.WhiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or
                                                             (enemyColor == 'b' and 4 <= j <= 5))) or (type == 'Q') or (
                                i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

class Move():
    rankstoRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2,"7": 1, "8": 0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h":7}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, startsq, endsq, board, isEnpessantMove=False, isCastleMove=False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        self.isEnpassantMove = isEnpessantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + +self.endCol
        if self.isCastleMove:
            print("Move object: isCastleMove")

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessnotation(self):
        return self.getrankfile(self.startRow, self.startCol) + self.getrankfile(self.endRow, self.endCol)
        #Add advanced "true" chess notation

    def getrankfile(self, r, c):
        return self.colstoFiles[c] + self.rowstoRanks[r]
