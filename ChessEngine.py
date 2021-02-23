import ChessMain
import ChessMoveGen
import ChessMinimax
import pygame as p
import numpy as np
import math

class GameState ():
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
        self.WhiteToMove = True
        self.turn = 1
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0, 4)
        self.gameOver = False
        self.whiteWin = False
        self.blackWin = False
        self.currentCastlingRights = castleRights(True, True, True, True)
        self.castlingCopy = (True, True, True, True)
        self.castleRightLog = [castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                            self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]
        self.castleRule = ChessMain.castleRule
        self.empassentPossible = False

    def getBoard(self):
        return self.board

    def aiMove(self):
        if not self.WhiteToMove:
            move = ChessMinimax.AI().minimax(self.board, 5, 5, True, self.WhiteToMove, math.inf, -math.inf)[0]
            if move == "None moves" or move == None:
                print("None moves error")
                return None
            else:
                return move
        if self.WhiteToMove:
            move = ChessMinimax.AI().minimax(self.board, 5, 5, True, self.WhiteToMove, math.inf, -math.inf)[0]
            if move == "None moves" or move == None:
                print("None moves error")
                return None
            else:
                return move

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'


        print("Castletest 2131313", move.isCastleMove)
        if move.isCastleMove:
            print("MakeMove Castletest")
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow, move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow, move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        self.updateCastlingRights(move)
        self.castleRightLog.append(
            castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs))
        print("Castlerights: ", self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        self.castlingCopy = (self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        print("Castletest 100", self.castlingCopy)
        movegen = ChessMoveGen.MoveGeneration().getMoves(self.board, self.WhiteToMove, False, self.castlingCopy)
        self.gameOver = movegen[1]
        self.whiteWin = movegen[2]
        self.blackWin = movegen[3]
        if self.whiteWin:
            print("GameOver, White Win")
        elif self.blackWin:
            print("GameOver, Black Win")
        elif self.gameOver:
            print("GameOver, Draw")


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpessantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpessantPossible = ()
            self.castleRightLog.pop()
            newRights = self.castleRightLog[-1]
            self.currentCastlingRights = castleRights(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

    def getValidMoves(self):
        if not self.gameOver:
            movegen = ChessMoveGen.MoveGeneration().getMoves(self.board, self.WhiteToMove, False, self.castlingCopy)
            moves = movegen[0]
            return moves


    def updateCastlingRights(self, move):
        print("Castlingtest 4")
        move = move
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
            print("Catlingtest WK")
        if move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
            print("Catlingtest BK")
        if move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.wks = False
                print("Catlingtest WR")
        if move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.bks = False
                print("Catlingtest BR")





class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

