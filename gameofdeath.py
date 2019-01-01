# lest we forget...
#  sox -r 16000 -e unsigned -b 8 -c 2 test.raw test.wav

import random
import math

width = 32
height = 32

board = [0] * height
for i in range(height):
    board[i] = [0] * width

nextBoard = [0] * height
for i in range(height):
    nextBoard[i] = [0] * width


#board[4][4] = 1
#board[4][6] = 1
#board[5][4] = 1
#board[5][6] = 1
#board[6][4] = 1
#board[6][5] = 1
#board[6][6] = 1


fileName = "test.raw"

def printboard(fh):
   global board

   pos = 0
   for y in range(0,height):
      amp = (1.0 * sum(board[y]) / height)

      for x in range(0, width):
         carrier = (math.sin((pos/(1024.0/1)) * math.pi * 2.0))
         signal = (board[y][x] * 2.0) - 1.0

         fh.write(bytearray([ int( (((carrier * (signal)) + 1.0) / 2) * 255 ) ]))

         pos += 1


def countFriends(x, y):
   global board
   friends = 0
   
   for row in [y-1, y, y+1]:
      for col in [x-1, x, x+1]:
#         if row < 0 or row > height-1 or col < 0 or col > width-1:
#            continue
         if col == x and row == y:
            continue
         if row < 0:
            row = height - 1
         if row > height - 1:
            row = 0
         if col < 0:
            col = width - 1
         if col > width - 1:
            col = 0

         friends += board[row][col]

   return friends


#('x', 0, 'y', 3, 'friends', 4)
#('x', 1, 'y', 3, 'friends', 5)
#('x', 2, 'y', 3, 'friends', 4)
#('x', 3, 'y', 3, 'friends', 4)
#('x', 4, 'y', 3, 'friends', 4)
with open(fileName, 'wb+') as fh:

   pin = 100 #random.randint(16, 64)

   for i in range(0, 1000):
      printboard(fh)
      nextBoard = [0] * height
      for g in range(height):
          nextBoard[g] = [0] * width

      for y in range(0, width):
         for x in range(0, height):
            f = countFriends(x,y)
            if board[y][x] == 1:
               if f < 2 or f > 3:
                  nextBoard[y][x] = 0
               elif f == 2 or f == 3:
                  nextBoard[y][x] = 1
            elif board[y][x] == 0 and f == 3:
               nextBoard[y][x] = 1

            if i % pin == 0 and nextBoard[y][x] == 0:
               if random.randint(1,10) == 1:
                  nextBoard[y][x] = 1
      #if i % pin == 0:
         #pin = random.randint(16, 512)

      board = nextBoard
