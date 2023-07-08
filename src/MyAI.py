# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random      # Need this for the guessing tile logic

# Class meant to store all of the data related to the Minesweeper tiles
class tileUnit():
    def __init__(self, xVal, yVal, rowDimension, colDimension):
        self.x = xVal
        self.y = yVal
        self.value = -1 #If value = -1, then that indicates uncovered state, and if >= 0, then it has been uncovered
        self.isFlagged = False  

        
# Our AI class
class MyAI( AI ):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.__rowDimension = colDimension
        self.__colDimension = rowDimension
        self.__coveredTilesLeft = (rowDimension*colDimension) - 1
        self.__totalMines = totalMines
        self.__lastAction = Action(AI.Action.UNCOVER, startX, startY)
        
        # Section of data structures
        # BoardMap stores the tileUnit class objects for reference and information updating
        self.__boardMap = [[tileUnit(row, col, self.__rowDimension, self.__colDimension) for col in range(self.__colDimension)]for row in range(self.__rowDimension)]
        # Frontier stores the neighbors/tileUnits of tiles yet to be uncovered
        self.__frontier = []
        # NewMoves stores the potential moves we could return and act on
        self.__newMoves = []

        
    #This function will check all, possible, 8 neighboring tiles for a given tile and determine which of the n 
    #     and add them to the frontierQueue
    # At max this will see 8 neighbors
    # Remember, the grid is 1 -> rowDimension
    def checkNeighbors(self, x: int, y: int) -> list:
        neighborList = []
        if(x > 0):
            neighborList.append(self.__boardMap[x-1][y]) #left
        if(x < self.__rowDimension-1):
            neighborList.append(self.__boardMap[x+1][y]) #right
        if(y < self.__colDimension-1):
            neighborList.append(self.__boardMap[x][y+1]) #up
        if(y > 0):
            neighborList.append(self.__boardMap[x][y-1]) #down
            
        if(y < self.__colDimension-1 and x < self.__rowDimension-1):
            neighborList.append(self.__boardMap[x+1][y+1]) #NE
        if(y > 0 and x < self.__rowDimension-1):
            neighborList.append(self.__boardMap[x+1][y-1]) #SE
        if(y > 0 and x > 0):
            neighborList.append(self.__boardMap[x-1][y-1]) #SW
        if(y < self.__colDimension-1 and x > 0):
            neighborList.append(self.__boardMap[x-1][y+1]) #NW
        return neighborList  

    
    # Decides what a unitTile we should act on
    def getAction(self, number: int) -> "Action Object":
        xCoordinate = self.__lastAction.getX()
        yCoordinate = self.__lastAction.getY()
        
        # If the tile value less than 0, that means we flagged the tileUnit, so update its internal flag value
        if (number == -1):
                self.__boardMap[xCoordinate][yCoordinate].isFlagged = True
        else:
            # Otherwise, it's an uncovering command, and thus we prcoess it as such
            self.__coveredTilesLeft -= 1
            self.__boardMap[xCoordinate][yCoordinate].value = number
            if (not self.__boardMap[xCoordinate][yCoordinate] in self.__frontier):
                self.__frontier.append(self.__boardMap[xCoordinate][yCoordinate])

        for curTile in self.__frontier:
            if curTile.value >= 0 and not curTile.isFlagged:
                # check how many blocks around are solved or are mines.
                numLocallyMarkedNeighbors = 0
                localUncoveredTiles = []

                ################################ Rule of Thumb Logic Section ################################
                # Calculate the effective label value to determine our logic 
                # According to the lecture notes, it'll be best to isolate for just the local
                #    neighbor nodes of a single tileUnit
                for neighboringNode in self.checkNeighbors(curTile.x, curTile.y):
                    if (neighboringNode.isFlagged):
                        numLocallyMarkedNeighbors += 1
                    elif (neighboringNode.value == -1):
                        localUncoveredTiles.append(neighboringNode)
                effectiveLabelValue = curTile.value - numLocallyMarkedNeighbors

                # Scan through the newMoves array and only add moves not already inside the array
                # Uncover all tiles not yet flagged
                if (effectiveLabelValue == 0):
                    for neighboringNode in localUncoveredTiles:
                        for tempMove in self.__newMoves:
                            if (( (tempMove.getX()) == neighboringNode.x) and ( (tempMove.getY()) == neighboringNode.y)):
                                break
                        else:
                            self.__newMoves.append(Action(AI.Action.UNCOVER, neighboringNode.x, neighboringNode.y))

                # Flag All uncovered tiles
                if (len(localUncoveredTiles) == effectiveLabelValue):
                    for neighboringNode in localUncoveredTiles:
                        for tempMove in self.__newMoves:
                            if (( (tempMove.getX()) == neighboringNode.x) and ( (tempMove.getY()) == neighboringNode.y)):
                                break
                        else:
                            self.__newMoves.append(Action(AI.Action.FLAG, neighboringNode.x, neighboringNode.y))
                #############################################################################################
                
                
        ################################ Inference / Guessing Logic Section ################################
        ## If after the Rule of Thumb logics do not produce any new moves, this section activates
        
        ############# Random Guess Logic
        ## Only runs if Inference Logic couldn't produce any results
        if(len(self.__newMoves) == 0):
            xValue, yValue = random.choice([[x, y] for y in range(self.__colDimension) for x in range(self.__rowDimension)])
            self.__newMoves.append(Action(AI.Action.UNCOVER, xValue, yValue))
        
        #############################################################################################

        ## Return a move
        self.__lastAction = self.__newMoves.pop()
        return self.__lastAction
    