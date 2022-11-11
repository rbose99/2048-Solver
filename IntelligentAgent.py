import math
import time
import random
from BaseAI import BaseAI
class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        self.time=time.time()
        best_move, _=self.maximize(grid, -9999999, 9999999,0)
        return best_move

    def maximize(self,grid, alpha, beta,d):
        moveset=grid.getAvailableMoves()
        maxMove=None
        maxUtility = -9999999
        if not moveset:
            return None, self.calcUtility(grid)
        for move in moveset:
            new_grid = move[1].clone()
            utility = self.minimize(new_grid, alpha, beta,d+1)
            if utility > maxUtility:
                maxMove = move
                maxUtility=utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return maxMove[0], maxUtility

    def minimize(self, grid, alpha, beta,d):
        if d>4 or time.time()-self.time>=0.15: 
            return self.calcUtility(grid)

        minUtility = 99999999
        for x,y in grid.getAvailableCells():
            gridCopy1=grid.clone()
            gridCopy1.insertTile((x,y),4)
            gridCopy2=grid.clone()
            gridCopy2.insertTile((x,y),2)
            _,utility1 = self.maximize(gridCopy1, alpha, beta,d+1)
            _,utility2 = self.maximize(gridCopy2, alpha, beta,d+1)
            utility = 0.1*utility1+0.9*utility2

            if utility < minUtility:
                minUtility=utility

            if minUtility <= alpha:
                break

            if minUtility < beta:
                beta = minUtility

        return minUtility

    #we increase weight of h1 as number of empty cells is very low when board is almost full and moves are crucial, easier to handle almost empty board
    def calcUtility(self,grid):
        h3_1,h3_2=self.h3(grid)
        return 2.5*self.h1(grid)+self.h2(grid)+h3_1+h3_2
    #number of empty cells
    def h1(self,grid):
        return len(grid.getAvailableCells())
    #max tile value
    def h2(self,grid):
        return math.log(grid.getMaxTile())
    #calculating number of possible merges and  monotonicity, gives a penalty if not monotone
    def h3(self, grid):
        dec=0
        inc=0
        num_merges_ud=0
        for i in range(grid.size):
          merge_idx=-1
          curr=0
          next=curr+1
          while next<grid.size:
            #want to find non zero block if possible
            while(next<grid.size-1 and grid.getCellValue((i,next))==0):
              next=next+1
            next_val=0
            if grid.getCellValue((i,next))!=0:
              next_val=math.log(grid.getCellValue((i,next)))
            curr_val=0
            if grid.getCellValue((i,curr))!=0:
              curr_val=math.log(grid.getCellValue((i,curr)))
            if merge_idx!=curr and curr_val!=0 and curr_val==next_val:
              merge_idx=curr
              num_merges_ud+=1
            if curr_val>next_val:
              dec+=next_val-curr_val
            else:
              inc+=curr_val-next_val
            curr=next
            next=next+1
        ud=max(dec,inc)
        dec=0
        inc=0
        num_merges_lr=0
        for i in range(grid.size):
          merge_idx=-1
          curr=0
          next=curr+1
          while next<grid.size:
            #want to find non zero block if possible
            while(next<grid.size-1 and grid.getCellValue((next,i))==0):
              next=next+1
            next_val=0
            if grid.getCellValue((next,i))!=0:
              next_val=math.log(grid.getCellValue((next,i)))
            curr_val=0
            if grid.getCellValue((curr,i))!=0:
              curr_val=math.log(grid.getCellValue((curr,i)))
            if merge_idx!=curr and curr_val!=0 and curr_val==next_val:
              merge_idx=curr
              num_merges_lr+=1
            if curr_val>next_val:
              dec+=next_val-curr_val
            else:
              inc+=curr_val-next_val
            curr=next
            next=next+1
        lr=max(dec,inc)
        return ud+lr,max(num_merges_ud,num_merges_lr)
              
  