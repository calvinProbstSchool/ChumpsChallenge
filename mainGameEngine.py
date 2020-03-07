# Chump's Challenge
# By Calvin Probst calvin.probst@gmail.com
# https://github.com/calvinProbstSchool/chumpschallenge

import pygame
import sys
from pygame.sprite import *
from pygame.locals import *


BLANKSURF = pygame.Surface((80, 80))
BLANKSURF.set_alpha(0)

class ChumpPlayer(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.image = pygame.image.load(
            "DKDonkeyKongHesTheLeaderOfTheBunchYouKnowHimWellHesFinallyBackToKickSomeTailHisCoconutGunCanFireInSpurtsIfHeShootsYaItsGonnaHurtHesBiggerFasterAndStrongerTooHesTheFirstMemberOfTheDKCrewHuh.png")
        self.rect = self.image.get_rect()

        self.bX = -1
        self.bY = -1


class BasicTile(Sprite):
    def __init__(self, boardX, boardY, imageFilename, tType):
        Sprite.__init__(self)

        self.image = pygame.image.load(imageFilename)
        self.rect = self.image.get_rect()

        self.bX = boardX
        self.bY = boardY

        self.tileType = tType
        self.itemType = None


    def __str__(self):
        return ("A " + self.tileType + " at " + str(self.bX) + ", " + str(self.bY) + ".")


class BasicItem(BasicTile):
    def __init__(self, boardX, boardY, imageFilename, itemType):
        BasicTile.__init__(self, boardX, boardY, imageFilename, "_")

        self.itemType = itemType


    def __str__(self):
        return ("A " + self.itemType + " at " + str(self.bX) + ", " + str(self.bY) + ".")


class WallTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "shesABrickHouse.png", "W")


class IceTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "iceIceBaby.png", "I")


class WaterTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "vvaves(Kanye).png", "w")


class DoorTile(BasicTile):
    def __init__(self, boardX, boardY, keyNumber):
        BasicTile.__init__(self, boardX, boardY, "jimMorrison.png", "D")

        self.keyNum = int(keyNumber)


class EmptyTile(Sprite):
    def __init__(self, boardX, boardY):
        Sprite.__init__(self)

        self.image = BLANKSURF
        self.rect = pygame.Rect(0, 0, 80, 80)

        self.bX = boardX
        self.bY = boardY

        self.tileType = "_"
        self.itemType = None


    def __str__(self):
        return ("A " + self.tileType + " at " + str(self.bX) + ", " + str(self.bY) + ".")


class HintTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "hintsAreForRealChumps.png", "H")


class CrateTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "heartShapedBox.png", "B")


class DarkTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "areYouAfraidOfTheDark.png", "d")


class FireTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "burningFireOnTheDancefloor.png", "F")

#It takes 24:36 to reach the bottom give or take a bit with 4.2k tiles
#
#

class BoxTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "heartShapedBox.png", "B")


class GoalTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "2021ForJamesonJKLmao.png", "G")

class MonsterTile(BasicTile):
    def __init__(self, boardX, boardY):
        BasicTile.__init__(self, boardX, boardY, "theOneThingWorseThanAChild.png", "K")


class FireShoesItem(BasicItem):
    def __init__(self, boardX, boardY):
        BasicItem.__init__(self, boardX, boardY, "pumpedUpKicks.png", "K")


class KeyItem(BasicItem):
    def __init__(self, boardX, boardY, keyN):
        BasicItem.__init__(self, boardX, boardY, "key1.png", "k")
        self.keyNum = keyN


WINDOWSIZEX = 1980
WINDOWSIZEY = 1080
BOARDSIZE = 720
MARGINSIZE = 100
TILESIZE = 80
FONTSIZE = 60
FPS = 20


PLAYER = "+"
GOAL = "G"
WALL = "W"
WATER = "w"
ICE = "I"
DOOR = "D"
DARK = "d"
EMPTY = "_"
HINT = "H"
BOX = "B"
FIRE = "F"
SHOES = "K"
KEY = "k"
KEY1 = "!"
KEY2 = "@"
KEY3 = "#"
MONSTER = "M"


DIRUP = 0.5
DIRRIGHT = 1
DIRDOWN = -0.5
DIRLEFT = -1

playerX = -1
playerY = -1

monsterX = -1
monsterY = -1
MonsterHere = False

WATERSINKS = []

GREEN = (0, 0, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main(level=1):
    global FPSCLOCK, DISPLAYSURF, CHUMPFONT, SHOWNBOARD, CHUMP, SHOWNBOARDTOPLAYER, INVENTORY, SCORE, DODEATH, PRINTEDTIMEDIFF, WATERSINKS, playerX, playerY, monsterX, monsterY, MonsterHere
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
    pygame.display.set_caption("Chump's Challenge")
    FPSCLOCK = pygame.time.Clock()
    CHUMPFONT = pygame.font.Font("./Jumpman.ttf", FONTSIZE)
    SHOWNBOARD = Group()
    SHOWNBOARDTOPLAYER = Group()
    CHUMP = ChumpPlayer()

    tileBoard = getBoard(level)
    INVENTORY = []
    for i in range(0, 3):
        row = []
        for j in range(0, 3):
            row.append(None)
        INVENTORY.append(row)

    PRINTEDTIMEDIFF = int(pygame.time.get_ticks() / 1000)

    scoreStart = 0
    if level == 1:
        scoreStart = 40000
    elif level == 2:
        scoreStart = 540 + 1537 - PRINTEDTIMEDIFF
    elif level == 3:
        scoreStart = 600 + 540 + 1537 - PRINTEDTIMEDIFF
    SCORE = scoreStart
    DODEATH = False

    while True:
        if DODEATH:
            gameEnd(level)
        DISPLAYSURF.fill(BLACK)
        drawBoard(tileBoard)
        pygame.display.update()
        FPSCLOCK.tick()
        keyPress = False
        keyDir = 0

        SCORE = scoreStart - int(pygame.time.get_ticks() / 1000)

        if int(pygame.time.get_ticks() / 1000) > 10000000:
            gameTimeOut()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    keyPress = True
                    keyDir = DIRLEFT
                elif event.key == K_RIGHT:
                    keyPress = True
                    keyDir = DIRRIGHT
                elif event.key == K_UP:
                    keyPress = True
                    keyDir = DIRUP
                elif event.key == K_DOWN:
                    keyPress = True
                    keyDir = DIRDOWN

        if keyPress:
            movePlayer(tileBoard, keyDir, level)
            if level == 1:
                if abs(playerY - monsterY) > abs(playerX - monsterX):
                    if playerY > monsterY:
                        dirMons = DIRDOWN
                    else:
                        dirMons = DIRUP
                else:
                    if playerX > monsterX:
                        dirMons = DIRRIGHT
                    else:
                        dirMons = DIRLEFT

                monsMovePos = tileInDir(monsterX, monsterY, dirMons)
                phold = tileBoard[monsterY][monsterX]
                tileBoard[monsterY][monsterX] = EmptyTile(monsterX, monsterY)
                tileBoard[monsMovePos[1]][monsMovePos[0]] = phold
                monsterX = monsMovePos[0]
                monsterY = monsMovePos[1]


            if (playerY == monsterY and playerX == monsterX):
                drawBoard(tileBoard)
                pygame.display.update()
                DODEATH = True

        if gameWin(tileBoard):
            gameNext(level)

def gameEnd(levelNum):
    endGameLine1 = CHUMPFONT.render("You are mad because you are bad.", True, GREEN, WHITE)
    endGameLine2 = CHUMPFONT.render("Press any key to just give up and start over,", True, GREEN, WHITE)
    endGameLine3 = CHUMPFONT.render("like the chump you aspire to be",
                                    True, GREEN, WHITE)
    DISPLAYSURF.blit(endGameLine1, (100, 100))
    DISPLAYSURF.blit(endGameLine2, (100, 160))
    pygame.display.update()
    bpress = False
    while not bpress:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                main(levelNum)

def gameHint(board, hintText):
    drawBoard(board)
    pygame.display.update()
    FPSCLOCK.tick()
    endGameLine1 = CHUMPFONT.render(hintText, True, GREEN, WHITE)
    DISPLAYSURF.blit(endGameLine1, (100, 100))
    pygame.display.update()
    bpress = False
    while not bpress:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                bpress = True

def gameNext(levelNum):
    global PRINTEDTIMEDIFF
    endGameLine1 = CHUMPFONT.render("You beat it, hopefully with dignity intact.", True, GREEN, WHITE)
    endGameLine2 = CHUMPFONT.render("if this is the last level cognarts you beat it", True, GREEN, WHITE)
    DISPLAYSURF.blit(endGameLine1, (100, 100))
    DISPLAYSURF.blit(endGameLine2, (100, 160))
    pygame.display.update()
    bpress = False
    while not bpress:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and levelNum < 3:
                PRINTEDTIMEDIFF = PRINTEDTIMEDIFF + int(pygame.time.get_ticks() / 1000)
                main(levelNum + 1)


def gameTimeOut():
    endGameLine1 = CHUMPFONT.render("oops the hidden timer cap caught you better luck next time", True, GREEN, WHITE)
    endGameLine2 = CHUMPFONT.render("bottom text", True, GREEN, WHITE)
    DISPLAYSURF.blit(endGameLine1, (100, 100))
    DISPLAYSURF.blit(endGameLine2, (100, 800))
    pygame.display.update()
    bpress = False
    pygame.time.wait(1000)
    while not bpress:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                exit()


def getBoard(levelNum):
    f = open(("level" + str(levelNum) + ".txt"), "r")
    rows = f.readlines()
    board = []
    for row in rows:
        TileRow = []
        for x in row.split(","):
            if not x== "\n":
                TileRow.append(x)
        board.append(TileRow)
    for y in range(len(board)):
        for x in range(len(board[y])):
            board[y][x] = getTextToTile(board[y][x], x, y)
    return board


def getEmptyInventorySpace():
    global INVENTORY
    for y in range(0, 3):
        for x in range(0, 3):
            if INVENTORY[y][x] is None:
                return x, y

    INVENTORY[0][0] = None
    for y in range(0, 3):
        for x in range(0, 3):
            if x == 2 and not y == 2:
                INVENTORY[y][x] = INVENTORY[y + 1][0]
            elif not (x == 2 and y == 2):
                INVENTORY[y][x] = INVENTORY[y][x + 1]
    INVENTORY[2][2] = None
    return (2, 2)



def getTextToTile(tileStr, x, y):
    global playerX, playerY, monsterX, monsterY, MonsterHere
    if tileStr == WALL:
        return WallTile(x, y)
    elif tileStr == WATER:
        return WaterTile(x, y)
    elif tileStr == ICE:
        return IceTile(x, y)
    elif tileStr == "1" or tileStr == "2" or tileStr == "3":
        return DoorTile(x, y, tileStr)
    elif tileStr == EMPTY:
        return EmptyTile(x, y)
    elif tileStr == DARK:
        return DarkTile(x, y)
    elif tileStr == HINT:
        return HintTile(x, y)
    elif tileStr == FIRE:
        return FireTile(x, y)
    elif tileStr == BOX:
        return BoxTile(x, y)
    elif tileStr == GOAL:
        return GoalTile(x, y)
    elif tileStr == SHOES:
        return FireShoesItem(x, y)
    elif tileStr == KEY1:
        return KeyItem(x, y, 1)
    elif tileStr == KEY2:
        return KeyItem(x, y, 2)
    elif tileStr == KEY3:
        return KeyItem(x, y, 3)
    elif tileStr == PLAYER:
        playerX = x
        playerY = y
        return EmptyTile(x, y)
    elif tileStr == MONSTER:
        monsterX = x
        monsterY = y
        MonsterHere = True
        return MonsterTile(x, y)


def gameWin(board):
    return board[playerY][playerX].tileType == GOAL


def tileInDir(x, y, dir):
    if dir == DIRDOWN:
        return (x, y + 1)
    elif dir == DIRUP:
        return (x, y - 1)
    elif dir == DIRLEFT:
        return (x - 1, y)
    elif dir == DIRRIGHT:
        return (x + 1, y)


def kicksInInv():
    for y in range(0, 3):
        for x in range(0, 3):
            itemTile = INVENTORY[y][x]
            if not itemTile is None:
                if itemTile.itemType == SHOES:
                    return True
    return False


def movePlayer(board, dir, levelNum):
    global playerX, playerY, INVENTORY, DODEATH, WATERSINKS, monsterY, monsterX, MonsterHere
    movePos = tileInDir(playerX, playerY, dir)
    moveTile = board[movePos[1]][movePos[0]]
    moveType = moveTile.tileType
    for sitch in WATERSINKS:
        sitch[2] = sitch[2] - 1
        if sitch[2] < 1:
            board[sitch[1]][sitch[0]] = sitch[3]
            WATERSINKS.remove(sitch)

    if (moveType == FIRE and not kicksInInv()) or moveType == WATER:
        playerX = movePos[0]
        playerY = movePos[1]
        DODEATH = True
    elif moveType == EMPTY or moveType == GOAL or (moveType == FIRE and kicksInInv()):
        playerX = movePos[0]
        playerY = movePos[1]
        if not moveTile.itemType is None:
            invX, invY = getEmptyInventorySpace()
            INVENTORY[invY][invX] = moveTile
            board[movePos[1]][movePos[0]] = EmptyTile(movePos[0], movePos[1])
    elif moveType == BOX:
        boxMovePos = tileInDir(movePos[0], movePos[1], dir)
        boxMoveTile = board[boxMovePos[1]][boxMovePos[0]]
        boxMoveType = boxMoveTile.tileType
        if boxMoveType == EMPTY:
            playerX = movePos[0]
            playerY = movePos[1]
            board[movePos[1]][movePos[0]].bX, board[movePos[1]][movePos[0]].bY = boxMovePos
            board[boxMovePos[1]][boxMovePos[0]].bX, board[boxMovePos[1]][boxMovePos[0]].bY = movePos
            placeholderTile = board[movePos[1]][movePos[0]]
            board[movePos[1]][movePos[0]] = board[boxMovePos[1]][boxMovePos[0]]
            board[boxMovePos[1]][boxMovePos[0]] = placeholderTile
        elif boxMoveType == FIRE:
            playerX = movePos[0]
            playerY = movePos[1]
            board[movePos[1]][movePos[0]] = EmptyTile(movePos[0], movePos[1])
            board[boxMovePos[1]][boxMovePos[0]] = EmptyTile(boxMovePos[0], boxMovePos[1])
        elif boxMoveType == WATER:
            playerX = movePos[0]
            playerY = movePos[1]
            WATERSINKS.append([boxMovePos[0], boxMovePos[1], 24, board[boxMovePos[1]][boxMovePos[0]]])
            board[movePos[1]][movePos[0]] = EmptyTile(movePos[0], movePos[1])
            board[boxMovePos[1]][boxMovePos[0]] = EmptyTile(boxMovePos[0], boxMovePos[1])
    elif moveType == ICE:
        playerX = movePos[0]
        playerY = movePos[1]
        drawBoard(board)
        pygame.display.update()
        FPSCLOCK.tick()
        movePlayer(board, dir, levelNum)
    elif moveType == DOOR and not board[playerY][playerX].tileType == ICE:
        openNum = moveTile.keyNum
        for y in range(0, 3):
            for x in range(0, 3):
                itemTile = INVENTORY[y][x]
                if not itemTile is None:
                    if itemTile.itemType == KEY:
                        if itemTile.keyNum == openNum:
                            board[movePos[1]][movePos[0]] = EmptyTile(movePos[0], movePos[1])
                            INVENTORY[y][x] = None
                            for x1 in range(x, 3):
                                if x1 == 2 and not y == 2:
                                    INVENTORY[y][x1] = INVENTORY[y + 1][0]
                                elif not (x1 == 2 and y == 2):
                                    INVENTORY[y][x1] = INVENTORY[y][x1 + 1]
                            for y1 in range(y + 1, 3):
                                for x1 in range(0, 3):
                                    if x1 == 2 and not y1 == 2:
                                        INVENTORY[y1][x1] = INVENTORY[y1 + 1][0]
                                    elif not (x1 == 2 and y1 == 2):
                                        INVENTORY[y1][x1] = INVENTORY[y1][x1 + 1]
                            return
    elif moveType == DOOR and board[playerY][playerX].tileType == ICE:
        openNum = moveTile.keyNum
        for y in range(0, 3):
            for x in range(0, 3):
                itemTile = INVENTORY[y][x]
                if not itemTile is None:
                    if itemTile.itemType == KEY:
                        if itemTile.keyNum == openNum:
                            board[movePos[1]][movePos[0]] = EmptyTile(movePos[0], movePos[1])
                            INVENTORY[y][x] = None
                            for x1 in range(x, 3):
                                if x1 == 2 and not y == 2:
                                    INVENTORY[y][x1] = INVENTORY[y + 1][0]
                                elif not (x1 == 2 and y == 2):
                                    INVENTORY[y][x1] = INVENTORY[y][x1 + 1]
                            for y1 in range(y + 1, 3):
                                for x1 in range(0, 3):
                                    if x1 == 2 and not y1 == 2:
                                        INVENTORY[y1][x1] = INVENTORY[y1 + 1][0]
                                    elif not (x1 == 2 and y1 == 2):
                                        INVENTORY[y1][x1] = INVENTORY[y1][x1 + 1]
                            playerY = movePos[1]
                            playerX = movePos[0]
                            return
        movePlayer(board, dir * -1, levelNum)
    elif moveType == WALL and board[playerY][playerX].tileType == ICE:
        movePlayer(board, dir * -1, levelNum)
    elif moveType == HINT:
        playerX = movePos[0]
        playerY = movePos[1]
        if levelNum == 1:
            gameHint(board, "just go down, $crublord")
        elif levelNum == 2:
            gameHint(board, "oops I lost my keys - you, 2019")
        elif levelNum == 3:
            gameHint(board, "you shouldn't need a hint if you beat the other levels")




def drawBoard(board):
    global playerX, playerY, INVENTORY
    lEdge = 0
    rEdge = len(board[0])
    tEdge = 0
    bEdge = len(board)

    if playerX > 3:
        lEdge = playerX - 4

    if playerX < len(board[0]) - 4:
        rEdge = playerX + 5

    if playerY > 3:
        tEdge = playerY - 4

    if playerY < len(board) - 4:
        bEdge = playerY + 5

    SHOWNBOARD.empty()
    SHOWNBOARDTOPLAYER.empty()

    for y in range(tEdge, bEdge):
        for x in range(lEdge, rEdge):
            print(str(x) + ' , ' + str(y))
            board[y][x].rect.x = boardToCoord(x - lEdge)
            board[y][x].rect.y = boardToCoord(y - tEdge)
            SHOWNBOARD.add(board[y][x])
    for y in range(0, 3):
        for x in range(0, 3):
            if not INVENTORY[y][x] is None:
                INVENTORY[y][x].rect.x, INVENTORY[y][x].rect.y = invToCoord(x, y)
                SHOWNBOARD.add(INVENTORY[y][x])
    drawClock()
    CHUMP.rect.x = boardToCoord(playerX - lEdge)
    CHUMP.rect.y = boardToCoord(playerY - tEdge)
    SHOWNBOARDTOPLAYER.add(CHUMP)
    pygame.draw.rect(DISPLAYSURF, (0, 100, 40), (MARGINSIZE, MARGINSIZE, BOARDSIZE, BOARDSIZE))
    SHOWNBOARD.draw(DISPLAYSURF)
    SHOWNBOARDTOPLAYER.draw(DISPLAYSURF)


def boardToCoord(n):
    return MARGINSIZE + (n * TILESIZE)


def invToCoord(x, y):
    return ((MARGINSIZE * 2) + BOARDSIZE + (x * TILESIZE + 20)), (MARGINSIZE + (y * TILESIZE + 20))


def drawClock(new=False):
    FPSCLOCK.tick(FPS)
    timeNum = int(pygame.time.get_ticks() / 1000) - PRINTEDTIMEDIFF
    timeStr = str(int(timeNum % 60))
    timeNum = timeNum - (timeNum % 60)
    minnum = 0
    while timeNum >= 60:
        minnum += 1
        timeNum -= 60
    if len(timeStr) == 1:
        timeStr = "0" + timeStr
    timeStr = str(minnum) + ":" + timeStr
    if new:
        timeStr = "0:00"
    timer = CHUMPFONT.render(timeStr, True, GREEN, BLACK)
    scoreText = CHUMPFONT.render(str(SCORE), True, GREEN, BLACK)
    DISPLAYSURF.blit(scoreText, ((2 * MARGINSIZE) + BOARDSIZE + 100, 10))
    DISPLAYSURF.blit(timer, ((2 * MARGINSIZE) + BOARDSIZE, 10))


main()