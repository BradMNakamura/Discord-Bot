from scipy.signal import convolve2d
import numpy as np

COLUMN_COUNT = 7
ROW_COUNT = 6

counter = 0
EMPTY = 0
WINDOW_LENGTH = 4
horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

class Position():
    def __init__(self):
      self.playerVal = ":white_circle:"
    def print(self):
        return " [" + self.playerVal + "] "
    def setVal(self, val):
      self.playerVal = val

class ConnectFour:
  def __init__(self):
    self.board = []
    self.playerOneBoard = np.zeros((6,7)) #Needs to be all zeros
    self.playerTwoBoard = np.zeros((6,7)) #Needs to be all zeros
    self.defaultBoard = np.ones((6,7)) #Needs to be all ones to compare
    self.keepTrack = [5,5,5,5,5,5,5] #Keep track of the peices.
    for i in range(6):
      col = []
      for j in range(7):
        col.append(Position())
      self.board.append(col)

  def PrintBoard(self):
    boardString = ""
    for i in range(6):
      currLine = ""
      for j in range(7):
        currLine += self.board[i][j].print()
      boardString += "\n" + currLine
    return boardString
  
  def TakeTurn(self,currPlayer, playerNum, row, col):
    self.keepTrack[col] -= 1
    self.board[row][col].setVal(currPlayer)
    currPlayerBoard = None
    if(playerNum == 0):
      self.playerOneBoard[row][col] = 1
      currPlayerBoard = self.playerOneBoard
    else:
      self.playerTwoBoard[row][col] = 1
      currPlayerBoard = self.playerTwoBoard

    return self.winning_move(currPlayerBoard)

  def GetRow(self, row):
    return self.keepTrack[row]

  
  def winning_move(self, player):
    for kernel in detection_kernels:
        print(convolve2d(self.defaultBoard == player, kernel, mode="valid"))
        if (convolve2d(self.defaultBoard == player, kernel, mode="valid") == 4).any():
            return True
    return False
