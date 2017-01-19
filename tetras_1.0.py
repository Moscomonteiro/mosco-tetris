import pygame
from random import randrange
import gc


# Define some colors as global constants
BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)
GREEN = (0  , 255, 0  )
RED   = (255, 0  , 0  )
BLUE  = (0  , 0  , 255)
GREY  = (150, 150, 150)
ORANG = (255, 165, 0  )
MAGEN = (180,   0, 180)
CYAN  = (0  , 255, 255)
LIME  = (140, 255, 63 )
OLIVE = (0  , 150, 0  )
BASE  = (51 , 51 , 51 )

#Other global variables
SIDE = 20

# Defining game classes

class Text():
    '''This is the class for text variables''' 
    def __init__(self, integer):
        text = str(integer)
        text2 = ''
        for i in range(6 - len(text)):
            text2 += '0'
        text2 += text
        self.text = text2

    def setText(self, text):
        self.text = str(text)
        
    def getText(self):
        return self.text

    def increasePoints(self, x):
        text2 = str(int(self.text) + int(x))
        self.text = ''
        for i in range(6 - len(text2)):
            self.text += '0'
        self.text += text2

    def printText(self, pos_x, pos_y, screen):
        font = pygame.font.Font(None, 36)
        text = font.render( self.text, True, BLACK)
        screen.blit(text, [pos_x * SIDE, pos_y * SIDE])

#============
class Block():
    '''this class creates a block that will compose the system'''
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def moveDown(self):
        self.y += 1
    def moveUp(self):
        self.y -= 1
    def moveLeft(self):
        self.x -= 1
    def moveRight(self):
        self.x += 1

    def drawBlock(self, screen):
        pygame.draw.rect(screen, self.color,
                         [self.x * SIDE,
                          self.y * SIDE,
                          SIDE, SIDE])

    def isTouching(self, block):
        if (self.x == block.x and self.y == block.y):
            return True
        else:
            return False

#============
class Board():
    '''This class creates a board for the game'''
    def __init__(self, blockList):
        self.walls = blockList
        self.groundBlocks = []
        self.checker = Block(2, 20, RED)

    def drawBoard(self, screen):
        '''This method draws the board'''
        for b in self.walls:
            b.drawBlock(screen)

    def drawGround(self, screen, flashList = []):
        '''this method draws the ground blocks'''
        for block in self.groundBlocks:
            if (flashList.count(block.y) == 0):
                block.drawBlock(screen)

    def newGround(self, blockList):
        '''This method grabs the blocks that fell to the ground
        and makes them ground blocks.'''
        for block in blockList:
            self.groundBlocks.append(block)

    def lineNumber(self, y):
        '''this method returns the number of blocks in a given
        line'''
        counter = 0
        for block in self.groundBlocks:
            if (block.y == y):
                counter += 1
        return counter
        
    def deleteLine(self, deleteList):
        '''this method delete blocks from flaged lines. The ones 
        in deleteList won't be drawn'''
        deleteBlocks = []
        for block in self.groundBlocks:
            if deleteList.count(block.y):
                deleteBlocks.append(block)

        for block in deleteBlocks:
            self.groundBlocks.remove(block)

        deleteBlocks = []

    def moveGround(self, deleted):
        '''this method moves the ground blocks'''
        while(len(deleted) > 0):
            x = min(deleted)
            for block in self.groundBlocks:
                if block.y < x:
                    block.moveDown()
            deleted.remove(x)

    def deleteGround(self):
        '''deletes Ground'''
        self.groundBlocks = []
        

#============
class Tetramino():
    '''This class creates the tetraminos'''
    def __init__(self, x, y):
        '''tetramino constructor method'''
        self.kind = randrange(7)
        self.blockList = []

        if (self.kind == 0): #L tetramino
            self.blockList.append(Block(x,y+2,RED))
            self.blockList.append(Block(x,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
            self.blockList.append(Block(x+1,y+2,WHITE))
        elif (self.kind == 1): #J tetramino
            self.blockList.append(Block(x,y+2,RED))
            self.blockList.append(Block(x,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
            self.blockList.append(Block(x-1,y+2,WHITE))
        elif (self.kind == 2): #T tetramino
            self.blockList.append(Block(x,y,RED))
            self.blockList.append(Block(x-1,y,WHITE))
            self.blockList.append(Block(x+1,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
        elif (self.kind == 3): #I tetramino
            self.blockList.append(Block(x,y,RED))
            self.blockList.append(Block(x-1,y,WHITE))
            self.blockList.append(Block(x+1,y,WHITE))
            self.blockList.append(Block(x+2,y,WHITE))
        elif (self.kind == 4): #O tetramino
            self.blockList.append(Block(x,y,RED))
            self.blockList.append(Block(x+1,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
            self.blockList.append(Block(x+1,y+1,WHITE))
        elif (self.kind == 5): #S tetramino
            self.blockList.append(Block(x,y,RED))
            self.blockList.append(Block(x+1,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
            self.blockList.append(Block(x-1,y+1,WHITE))
        elif (self.kind == 6): #Z tetramino
            self.blockList.append(Block(x,y,RED))
            self.blockList.append(Block(x-1,y,WHITE))
            self.blockList.append(Block(x,y+1,WHITE))
            self.blockList.append(Block(x+1,y+1,WHITE))

    def drawTetramino(self, screen):
        '''tetramino drawing method'''
        for block in self.blockList:
            block.drawBlock(screen)

    def moveDown(self):
        '''tetramino method for falling down'''
        for block in self.blockList:
            block.moveDown()

    def moveUp(self):
        '''tetramino method for moving up'''
        for block in self.blockList:
            block.moveUp()

    def moveLeft(self):
        '''tetramino method to move left'''
        for block in self.blockList:
            block.moveLeft()

    def moveRight(self):
        '''tetramino method to move right'''
        for block in self.blockList:
            block.moveRight()

    def goTo(self, x, y):
        dx = x - self.blockList[0].x
        dy = y - self.blockList[0].y
        for block in self.blockList:
            block.x += dx
            block.y += dy

    def rotate(self):
        for block in self.blockList:
            dx = block.x - self.blockList[0].x
            dy = block.y - self.blockList[0].y

            block.x = self.blockList[0].x - dy
            block.y = self.blockList[0].y + dx

    def isTouching(self, blockList):
        '''method for seeing if the tetramino touched a blocklist'''
        for b_1 in self.blockList:
            for b_2 in blockList:
                if b_1.isTouching(b_2):
                    return True
        return False

    def whoTouched(self, blockList):
        '''this method returns the relative coordiante of the
        hit block in respect to the [0]th block'''
        for i in range(1,4):
            for b_2 in blockList:
                if self.blockList[i].isTouching(b_2):
                    return [b_2.x - self.blockList[0].x,
                            b_2.y - self.blockList[0].y]
        return [0,0]


#Defining the main gameloop ===============================
def main():
    """ Main function for the game. """
    pygame.init()
 
    size = [20*SIDE, 22*SIDE] #Array for the canvas size
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption("MOSCO'S TETRIS")
 
    
    done = False #Variable to end the gameloop

    wallBlocks = [] #list for the blocks forming the walls
    for i in range(22):
        wallBlocks.append(Block( 1, i, BLACK))
        wallBlocks.append(Block(12, i, BLACK))
    for i in range(10):
        #wallBlocks.append(Block( 2+i, 0, BLACK))
        wallBlocks.append(Block( 2+i,21, BLACK))

    board = Board(wallBlocks) #Board

    wallBlocks = []
    for i in range(7):
        wallBlocks.append(Block( 12+i, 5, BLACK))
        wallBlocks.append(Block( 12+i, 12, BLACK))
    for i in range(8):
        wallBlocks.append(Block( 19, 5+i, BLACK))

    box = Board(wallBlocks)

    tetra = Tetramino(6,0)
    sideTetra = Tetramino(15,8)
    
    frameRate = 30
    downPace = 30
    animationPace = downPace
    time = 0
    sidePace = int(downPace/2) + 1

    time2 = 0
    
    moveRight = False
    moveLeft = False
    moveNow = False
    animation = False
    touched = False
    rotate = False
    fallFaster = False

    flashList = []
    deleteList = []

    points = Text('0')
    

    #In this part, we initialize the local variables of the
    #main game loop.
    
    clock = pygame.time.Clock() #Variable for the screen update
 
    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN and not animation:
                if event.key == pygame.K_RIGHT:
                    moveRight = True
                    moveLeft = False
                    moveNow = True
                        
                if event.key == pygame.K_LEFT:
                    moveLeft = True
                    moveRight = False
                    moveNow = True

                if event.key == pygame.K_DOWN:
                    fallFaster = True #makes tetraminos fall quicker

                if event.key == pygame.K_UP:
                    rotate = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and not animation:
                    moveRight = False
                if event.key == pygame.K_LEFT and not animation:
                    moveLeft = False
                if event.key == pygame.K_DOWN:
                    fallFaster = False #resets downPace to normal
        
 
        # Game logic ======================================
        time += 1
        if fallFaster:
            downPace = 1
        else:
            downPace = 30 - int(int(points.text)/1000)
            animationPace = downPace
            sidePace = int(downPace/2) + 1

        if not animation:
            #move sideways logic ====
            if (time % sidePace == 0 or moveNow):
                if moveRight:
                    tetra.moveRight()
                    if (tetra.isTouching(board.walls) or
                        tetra.isTouching(board.groundBlocks)):
                        tetra.moveLeft()
                if moveLeft:
                    tetra.moveLeft()
                    if (tetra.isTouching(board.walls) or
                        tetra.isTouching(board.groundBlocks)):
                        tetra.moveRight()
                moveNow = False

            #rotation logic ====
            if rotate:
                if tetra.kind != 4:
                    tetra.rotate()
                rotate = False
                boardList = board.groundBlocks + board.walls

                #Now the code verifies if the tetramino has touched
                #the gorund of the walls
                backX = tetra.blockList[0].x
                backY = tetra.blockList[0].y
                counter = 0
                while(tetra.isTouching(boardList)):
                    counter +=1
                    if (tetra.whoTouched(boardList)[0] > 0):
                        tetra.moveLeft()
                        counter += 1
                    if (tetra.whoTouched(boardList)[0] < 0):
                        tetra.moveRight()
                        counter += 1
                    if (tetra.whoTouched(boardList)[1] != 0):
                        tetra.moveUp()
                        counter += 1

                    if(counter > 8):
                        for i in range(3):
                            tetra.rotate()
                        tetra.goTo(backX, backY)

                boardList = []
                        
                
                        
                

            #move down logic ==== 
            if time % downPace == 0:
                tetra.moveDown()
                points.increasePoints(1)
                
                #This part of the code verifies if the block hit something
                #under it. In case it does, the block becomes part of the
                #ground, and a new tetramino is created.
                if (tetra.isTouching(board.walls) or
                    tetra.isTouching(board.groundBlocks)):
                    tetra.moveUp()
                    board.newGround(tetra.blockList)

                    #Now, the code checks if any block of the new ground blocks
                    #is in the toppest level. If yes, it finishes the game
                    touched = False
                    for block in tetra.blockList:
                        if block.y <= 0:
                            touched = True

                    #creates a new tetramino for the side, and passes
                    #the sideTetra for the main tetra
                    if not touched:
                        tetra = sideTetra
                        sideTetra = Tetramino(15,8)

                        for block in tetra.blockList:
                            block.x -= 9
                            block.y -= 8

                    #after that, the code checks for complete lines, by look-
                    #ing at the return of the function board.lineNumber(line)
                    deleteList = [] #list of lines (int) to be deleted
                    for line in range(20, 0, -1):
                        if (board.lineNumber(line) >= 10):
                            deleteList.append(line)
                    if (len(deleteList) > 0):
                        animation = True
                        points.increasePoints(10*len(deleteList))
                    

                #the code finishes the game:
                if touched:
                    done = True

               
            

            
        else:
            time2 += 1
            if((time2 % (2*animationPace/3)) > (animationPace/3)):
                flashList = []
            else:
                flashList = deleteList
            if(time2 > 2*animationPace):
                board.deleteLine(deleteList)
                board.moveGround(deleteList)
                animation = False
                time2 = 0

            
 
        # Drawing codes ===================================
        screen.fill(BASE) # Drawing the screen

        board.drawBoard(screen)
        board.drawGround(screen,flashList)
        box.drawBoard(screen)
        tetra.drawTetramino(screen)
        sideTetra.drawTetramino(screen)
        points.printText(15, 2, screen)

        


        # flipping the page ===============================
        pygame.display.flip()


 
        # setting frame rate ==============================
        clock.tick(frameRate)
 
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
 
if __name__ == "__main__":
    main()
