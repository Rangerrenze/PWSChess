import pygame as p
import copy
import numpy as np
import ChessMain
import ChessEngine
import random
import ChessMoveGen
import copy as c
import math

class AI():
    def __init__(self):
        self.gs = ChessEngine.GameState()
        self.WhitetoMove = self.gs.WhiteToMove
        self.allMoves = self.gs.getValidMoves()
        self.gameOver = False
        self.whiteWin = False
        self.blackWIn = False
        self.previousCastleMove = False
        self.whiteToTurnRight = True
        self.currentCastlingRights = castleRights(True, True, True, True)
        self.castlingCopy = (True, True, True, True)
        self.castleRightLog = [castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                            self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]
        self.castleRule = ChessMain.castleRule
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])


    def minimax(self, board, depth, OGDepth, maxPlayer, WhitetoMove, alpha, beta):
        if depth == OGDepth:
            self.whiteToTurnRight = WhitetoMove
        board = np.copy(board)
        self.WhitetoMove = WhitetoMove
        if depth == 0 or self.gameOver:
            return None, self.evaluateBoard(board, self.whiteToTurnRight)
        moveGen = ChessMoveGen.MoveGeneration().getMoves(board, self.WhitetoMove, True, self.castlingCopy)
        moves = moveGen[0]
        if not len(moves) >= 1:
            return None, self.evaluateBoard(board, self.WhitetoMove)
        gameOver = moveGen[1]
        bestMove = random.choice(moves)
        if gameOver:
            self.gameOver = True
        if maxPlayer:
            maxEval = -math.inf
            for move in moves:
                if move == "None Moves" or move == None:
                    break
                board, previousboard = self.makeMove(move, board)
                currentEval = self.minimax(board, depth -1, OGDepth, False, self.WhitetoMove, alpha, beta)[1]
                self.WhitetoMove = not self.WhitetoMove
                if ChessMain.castleRule:
                    self.castleRightLog.pop()
                    newRights = self.castleRightLog[-1]
                    self.currentCastlingRights = castleRights(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)
                    if self.previousCastleMove:
                        if move.endCol - move.startCol == 2:
                            previousboard[move.endRow][move.endCol + 1] = previousboard[move.endRow][move.endCol - 1]
                            previousboard[move.endRow][move.endCol - 1] = "--"
                        else:
                            previousboard[move.endRow][move.endCol - 2] = previousboard[move.endRow][move.endCol + 1]
                            previousboard[move.endRow][move.endCol + 1] = "--"
                board = previousboard


                if currentEval > maxEval:
                    maxEval = currentEval
                    bestMove = move
                alpha = max(alpha, currentEval)
                if alpha <= beta:
                    break
            return bestMove, maxEval
        else:
            minEval = math.inf
            for move in moves:
                if move == "None Moves" or move == None:
                    break
                board, previousboard = self.makeMove(move, board)
                currentEval = self.minimax(board, depth -1, OGDepth, True, self.WhitetoMove, alpha, beta)[1]
                self.WhitetoMove = not self.WhitetoMove
                if ChessMain.castleRule:
                    self.castleRightLog.pop()
                    newRights = self.castleRightLog[-1]
                    self.currentCastlingRights = castleRights(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)
                    if self.previousCastleMove:
                        if move.endCol - move.startCol == 2:
                            previousboard[move.endRow][move.endCol + 1] = previousboard[move.endRow][move.endCol - 1]
                            previousboard[move.endRow][move.endCol - 1] = "--"
                        else:
                            previousboard[move.endRow][move.endCol - 2] = previousboard[move.endRow][move.endCol + 1]
                            previousboard[move.endRow][move.endCol + 1] = "--"
                board = previousboard
                if currentEval < minEval:
                    minEval = currentEval
                    bestMove = move
                beta = min(beta, currentEval)
                if beta <= alpha:
                    break
            return bestMove, minEval



    def makeMove(self, move, board):
        tempboard = board
        move = move
        startrow = move.startRow
        startcol = move.startCol
        endrow = move.endRow
        endcol = move.endCol
        previousboard = copy.deepcopy(tempboard)
        startpiece = tempboard[startrow][startcol]
        tempboard[startrow][startcol] = "--"
        if startpiece == "wp":
            if endrow == 0:
                tempboard[endrow][endcol] = "wQ"
        elif startpiece == "bp":
            if endrow == 7:
                tempboard[endrow][endcol] = "bQ"
        if ChessMain.castleRule:
            if startpiece == "wK":
                self.currentCastlingRights.wks = False
                self.currentCastlingRights.wqs = False
            elif startpiece == "bK":
                self.currentCastlingRights.bks = False
                self.currentCastlingRights.bqs = False
            elif startpiece == "wR":
                if startrow == 7:
                    if move.startCol == 0:
                        self.currentCastlingRights.wqs = False
                    elif move.startCol == 7:
                        self.currentCastlingRights.wks = False
            elif startpiece == "bR":
                if startrow == 0:
                    if startcol == 0:
                        self.currentCastlingRights.bqs = False
                    elif startcol == 7:
                        self.currentCastlingRights.bks = False
            self.castleRightLog.append([castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                                self.currentCastlingRights.bks, self.currentCastlingRights.bqs)])
        if move.isCastleMove:
            if endcol - startcol == 2:
                tempboard[endrow][endcol-1] = tempboard[move.endRow][move.endCol+1]
                tempboard[endrow][endcol+1] = "--"
            else:
                tempboard[endrow][endcol + 1] = tempboard[endrow][endcol -2]
                tempboard[endrow][endcol -2] = "--"
            self.previousCastleMove = True
        else:
            self.previousCastleMove = False



        self.WhitetoMove = not self.WhitetoMove
        self.castlingCopy = (self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        return tempboard, previousboard




    def evaluateBoard(self, board, whiteToTurnRight):
        whiteToTurnRight = whiteToTurnRight
        boardvalue = 0
        tempboard = copy.deepcopy(board)
        moveGen = ChessMoveGen.MoveGeneration().getMoves(board, whiteToTurnRight, True, self.castlingCopy)
        EvaluateWhiteWin = moveGen[2]
        EvaluateBlackWin = moveGen[3]

        if ChessMain.antiChess:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    piece = tempboard[r][c]
                    if self.whiteToTurnRight:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue - 3
                            if piece[1] == "N":
                                boardvalue = boardvalue - 5
                            if piece[1] == "R" or piece[1] == "B" or piece[1] == "Q":
                                boardvalue = boardvalue - 4
                            if piece[1] == 'p':
                                boardvalue = boardvalue - 1
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue + 3
                            if piece[1] == "N":
                                boardvalue = boardvalue + 5
                            if piece[1] == "R" or piece[1] == "B" or piece[1] == "Q":
                                boardvalue = boardvalue + 4
                            if piece[1] == 'p':
                                boardvalue = boardvalue + 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue + 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue - 100000000000
                    else:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue + 3
                            if piece[1] == "N":
                                boardvalue = boardvalue + 5
                            if piece[1] == "R" or piece[1] == "B" or piece[1] == "Q":
                                boardvalue = boardvalue + 4
                            if piece[1] == 'p':
                                boardvalue = boardvalue + 1
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue - 3
                            if piece[1] == "N":
                                boardvalue = boardvalue - 5
                            if piece[1] == "R" or piece[1] == "B" or piece[1] == "Q":
                                boardvalue = boardvalue - 4
                            if piece[1] == 'p':
                                boardvalue = boardvalue - 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue - 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue + 100000000000
        elif not ChessMain.antiChess:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    piece = tempboard[r][c]
                    if self.whiteToTurnRight:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue + 100
                            if piece[1] == "Q":
                                boardvalue = boardvalue + 9
                            if piece[1] == "R":
                                boardvalue = boardvalue + 5
                            if piece[1] == "N" or piece[1] == "B":
                                boardvalue = boardvalue + 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue + 1
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue - 100
                            if piece[1] == "Q":
                                boardvalue = boardvalue - 9
                            if piece[1] == "R":
                                boardvalue = boardvalue - 5
                            if piece[1] == "N" or piece[1] == "B":
                                boardvalue = boardvalue - 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue - 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue + 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue - 100000000000
                    else:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue - 100
                            if piece[1] == "Q":
                                boardvalue = boardvalue - 9
                            if piece[1] == "R":
                                boardvalue = boardvalue - 5
                            if piece[1] == "N" or piece[1] == "B":
                                boardvalue = boardvalue - 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue - 1
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue + 100
                            if piece[1] == "Q":
                                boardvalue = boardvalue + 9
                            if piece[1] == "R":
                                boardvalue = boardvalue + 5
                            if piece[1] == "N" or piece[1] == "B":
                                boardvalue = boardvalue + 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue + 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue - 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue + 100000000000




        return boardvalue

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


