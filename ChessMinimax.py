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
        self.castleRule = ChessMain.castleRule
        self.castlingCopy = ()
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])

        self.whitePawnPositionValue = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
            [1.1, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 1.],
            [1.05, 1.05, 1.1, 1.25, 1.25, 1.1, 1.05, 1.05],
            [1, 1, 1, 1.5, 1.5, 1, 1, 1],
            [1.05, 0.95, 0.9, 1.05, 1.05, 0.9, 0.95, 1.05],
            [1.05, 1.1, 1.1, 0.8, 0.8, 1.1, 1.1, 1.05],
            [1, 1, 1, 1, 1, 1, 1, 1]]

        self.blackPawnPositionValue = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.05, 1.1, 1.1, 0.8, 0.8, 1.1, 1.1, 1.05],
            [1.05, 0.95, 0.9, 1.05, 1.05, 0.9, 0.95, 1.05],
            [1, 1, 1, 1.5, 1.5, 1, 1, 1],
            [1.05, 1.05, 1.1, 1.25, 1.25, 1.1, 1.05, 1.05],
            [1.1, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 1.],
            [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
            [1, 1, 1, 1, 1, 1, 1, 1]]

        self.KnightPositionValue = [
            [0.5, 0.6, 0.7, 0.7, 0.7, 0.7, 0.6, 0.50],
            [0.6, 0.8, 1, 1, 1, 1, 0.8, 0.6],
            [0.7, 1, 1.1, 1.15, 1.15, 1.1, 1, 0.7],
            [0.7, 1.05, 1.15, 1.2, 1.2, 1.15, 1.05, 0.7],
            [0.7, 1.05, 1.15, 1.2, 1.2, 1.15, 1.05, 0.7],
            [0.7, 1, 1.1, 1.15, 1.15, 1.1, 1, 0.7],
            [0.6, 0.8, 1, 1, 1, 1, 0.8, 0.6],
            [-50, -40, -30, -30, -30, -30, -40, -50]]

        self.BishopPositionValue = [
            [0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8],
            [0.9, 1, 1, 1, 1, 1, 1, 0.9],
            [0.9, 1, 1.05, 1.1, 1.1, 1.05, 1, 0.9],
            [0.9, 1.05, 1.05, 1.1, 1.1, 1.05, 1.05, 0.9],
            [0.9, 1.05, 1.05, 1.1, 1.1, 1.05, 1.05, 0.9],
            [0.9, 1, 1.05, 1.1, 1.1, 1.05, 1, 0.9],
            [0.9, 1, 1, 1, 1, 1, 1, 0.9],
            [0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8]]

        self.RookPositionValue = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.05, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.05],
            [0.95, 1, 1, 1, 1, 1, 1, 0.95],
            [0.95, 1, 1, 1, 1, 1, 1, 0.95],
            [0.95, 1, 1, 1, 1, 1, 1, 0.95],
            [0.95, 1, 1, 1, 1, 1, 1, 0.95],
            [1.05, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.05],
            [1, 1, 1, 5, 5, 1, 1, 1]]

        self.QueenPositionValue = [
            [0.8, 0.9, 0.9, 0.95, 0.95, 0.90, 0.9, 0.8],
            [0.9, 1, 1, 1, 1, 1, 1, 0.9],
            [0.9, 1, 1.5, 1.5, 1.5, 1.5, 1, 0.9],
            [0.95, 1, 1.5, 1.5, 1.5, 1.5, 1, 0.95],
            [0.95, 1, 1.5, 1.5, 1.5, 1.5, 1, 0.95],
            [0.9, 1, 1.5, 1.5, 1.5, 1.5, 1, 0.9],
            [0.9, 1, 1, 1, 1, 1, 1, 0.9],
            [0.8, 0.9, 0.9, 0.95, 0.95, 0.90, 0.9, 0.8]]

        self.KingPositionValue = [
            [1.2, 1.1, 1.1, 1.05, 1.05, 1.1, 1.2, 1.2],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.2, 1.1, 1.1, 1.05, 1.05, 1.1, 1.2, 1.2]]





    def evaluateBoard(self, board, whiteToTurnRight, castles):
        whiteToTurnRight = whiteToTurnRight
        self.castlingCopy = castles
        self.board = board
        boardvalue = 0
        tempboard = copy.deepcopy(self.board)
        moveGen = ChessMoveGen.MoveGeneration().getMoves(board, whiteToTurnRight, True, self.castlingCopy)
        EvaluateWhiteWin = moveGen[2]
        EvaluateBlackWin = moveGen[3]

        if ChessMain.antiChess:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    piece = tempboard[r][c]
                    if whiteToTurnRight:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue - 3
                            if piece[1] == "Q":
                                boardvalue = boardvalue - 3
                            if piece[1] == "R":
                                boardvalue = boardvalue - 3
                            if piece[1] == "N":
                                boardvalue = boardvalue - 5
                            if piece[1] == "B":
                                boardvalue = boardvalue - 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue - 1
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue + 3
                            if piece[1] == "Q":
                                boardvalue = boardvalue + 3
                            if piece[1] == "R":
                                boardvalue = boardvalue + 3
                            if piece[1] == "N":
                                boardvalue = boardvalue + 5
                            if piece[1] == "B":
                                boardvalue = boardvalue + 3
                            if piece[1] == 'p':
                                boardvalue = boardvalue + 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue + math.inf
                        if EvaluateBlackWin:
                            boardvalue = boardvalue - math.inf
                        else:
                            if piece[0] == "w":
                                if piece[1] == "K":
                                    boardvalue = boardvalue + 3
                                if piece[1] == "Q":
                                    boardvalue = boardvalue + 3
                                if piece[1] == "R":
                                    boardvalue = boardvalue + 3
                                if piece[1] == "N":
                                    boardvalue = boardvalue + 5
                                if piece[1] == "B":
                                    boardvalue = boardvalue + 3
                                if piece[1] == 'p':
                                    boardvalue = boardvalue + 1
                            if piece[0] == "b":
                                if piece[1] == "K":
                                    boardvalue = boardvalue - 3
                                if piece[1] == "Q":
                                    boardvalue = boardvalue - 3
                                if piece[1] == "R":
                                    boardvalue = boardvalue - 3
                                if piece[1] == "N":
                                    boardvalue = boardvalue - 5
                                if piece[1] == "B":
                                    boardvalue = boardvalue - 3
                                if piece[1] == 'p':
                                    boardvalue = boardvalue - 1
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue - math.inf
                        if EvaluateBlackWin:
                            boardvalue = boardvalue + math.inf
        elif not ChessMain.antiChess:
            print("Normal chess minimax working as intended")
            for r in range(len(board)):
                for c in range(len(board[r])):
                    piece = tempboard[r][c]
                    if whiteToTurnRight:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue + (10*self.KingPositionValue[r][c])
                            if piece[1] == "Q":
                                boardvalue = boardvalue + (9*self.QueenPositionValue[r][c])
                            if piece[1] == "R":
                                boardvalue = boardvalue + (5*self.RookPositionValue[r][c])
                            if piece[1] == "N":
                               boardvalue = boardvalue + (3*self.KnightPositionValue[r][c])
                            if piece[1] == "B":
                                boardvalue = boardvalue + (3*self.BishopPositionValue[r][c])
                            if piece[1] == 'p':
                                boardvalue = boardvalue + (1*self.whitePawnPositionValue[r][c])
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue - (2*self.KingPositionValue[r][c])
                            if piece[1] == "Q":
                                boardvalue = boardvalue - (180*self.QueenPositionValue[r][c])
                            if piece[1] == "R":
                                boardvalue = boardvalue - (10*self.RookPositionValue[r][c])
                            if piece[1] == "N":
                                boardvalue = boardvalue - (6 * self.KnightPositionValue[r][c])
                            if piece[1] == "B":
                                boardvalue = boardvalue - (6 * self.BishopPositionValue[r][c])
                            if piece[1] == 'p':
                                boardvalue = boardvalue - (2*self.whitePawnPositionValue[r][c])
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue + 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue - 100000000000
                    else:
                        if piece[0] == "w":
                            if piece[1] == "K":
                                boardvalue = boardvalue - (1*self.KingPositionValue[r][c])
                            if piece[1] == "Q":
                                boardvalue = boardvalue - (9*self.QueenPositionValue[r][c])
                            if piece[1] == "R":
                                boardvalue = boardvalue - (5*self.RookPositionValue[r][c])
                            if piece[1] == "N":
                                boardvalue = boardvalue - (3 * self.KnightPositionValue[r][c])
                            if piece[1] == "B":
                                boardvalue = boardvalue - (3 * self.BishopPositionValue[r][c])
                            if piece[1] == 'p':
                                boardvalue = boardvalue - (1*self.whitePawnPositionValue[r][c])
                        if piece[0] == "b":
                            if piece[1] == "K":
                                boardvalue = boardvalue + (2*self.KingPositionValue[r][c])
                            if piece[1] == "Q":
                                boardvalue = boardvalue + (180*self.QueenPositionValue[r][c])
                            if piece[1] == "R":
                                boardvalue = boardvalue + (10*self.RookPositionValue[r][c])
                            if piece[1] == "N":
                                boardvalue = boardvalue + (6 * self.KnightPositionValue[r][c])
                            if piece[1] == "B":
                                boardvalue = boardvalue + (6 * self.BishopPositionValue[r][c])
                            if piece[1] == 'p':
                                boardvalue = boardvalue + (2*self.whitePawnPositionValue[r][c])
                        if EvaluateWhiteWin:
                            boardvalue = boardvalue - 100000000000
                        if EvaluateBlackWin:
                            boardvalue = boardvalue + 100000000000
        return boardvalue






