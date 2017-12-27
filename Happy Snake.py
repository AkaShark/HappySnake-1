#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,random,time,pygame
from pygame.locals import *

FPS = 5 # 屏幕刷新率（在这里相当于贪吃蛇的速度）
WINDOWWIDTH = 640 # 屏幕宽度
WINDOWHEIGHT = 480 # 屏幕高度
CELLSIZE = 20 # 小方格的大小

# 断言，屏幕的宽和高必须能被方块大小整除
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

# 横向和纵向的方格数
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)


# 定义几个常用的颜色
# R G B
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK

# 定义贪吃蛇的动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 贪吃蛇的头（）
HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()# 获取pygame的时钟
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#设置屏幕的宽高
    BASICFONT = pygame.font.SysFont('PAPYRUS',20)#设置字体
    pygame.display.set_caption("Wormy") # 设置窗口的标题

    showStartScreen()# 显示开始的画面
    while True:
        runGame()# 运行游戏
        showGameOverScreen()# 显示游戏结束画面
        pass
def runGame():
    #  随机初始化设置一个点作为贪吃蛇的起点
    startX = random.randint(5, CELLWIDTH-6)
    startY = random.randint(5, CELLHEIGHT-6)

    # 以这个点为起点，建立一个长度为3格的贪吃蛇（数组）
    wormCoords = [{'x':startX,'y':startY},
                  {'x':startX-1,'y':startY},
                  {'x':startX-2,'y':startY}]
    direction = RIGHT #初始化一个运动的方向
    # 随机一个apple的位置
    apple = getRandomLocation()
    while True: #游戏主循环
        for event in pygame.event.get(): #事件的处理
            if event.type == QUIT: #退出事件
                terminate()
            elif event.type == KEYDOWN : #按键事件
                # 如果按下的是左键或者a键，且当今的方向不是向右，就改变方向。一次类推
                if(event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT :
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        #检查贪吃蛇是否撞到边界
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT :
            return  #GameOver
        # 检查贪吃蛇是否撞倒自己
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and  wormBody['y'] == wormCoords[HEAD]['y']:
                return #GameOver

                # 检查贪吃蛇是否吃到apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # 不移除蛇的最后一个尾巴格
            apple = getRandomLocation()  # 重新随机生成一个apple
        else:
            del wormCoords[-1]  # 移除蛇的最后一个尾巴格


        #根据方向，添加一个新的舌头，以这种方式来移动贪吃蛇
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}#点
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        #插入一个头在数组前面
        wormCoords.insert(0,newHead)

        #绘制背景
        DISPLAYSURF.fill(BGCOLOR)
        #绘制所有的方格
        drawGrid()

        #绘制贪吃蛇
        drawWorm(wormCoords)

        # 绘制apple
        drawApple(apple)

        # 绘制分数（分数为贪吃蛇数组当前的长度-3）
        drawScore(len(wormCoords) - 3)

        # 更新屏幕
        pygame.display.update()

        # 设置帧率
        FPSCLOCK.tick(FPS)

# 绘制提示消息
def drawPressKeyMSg():
    pressKeySuf = BASICFONT.render('Press a key to play',True,RED)
    pressKeyRect = pressKeySuf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySuf,pressKeyRect)

#检查是否有按键事件
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvent = pygame.event.get(KEYUP)
    if len(keyUpEvent) == 0:
        return None
    if keyUpEvent[0].key == K_ESCAPE:
        terminate()
    return keyUpEvent[0].key

#显示开始画面
def showStartScreen():
    DISPLAYSURF.fill(BGCOLOR)
    titleFont = pygame.font.Font('PAPYRUS.ttf', 100)
    titleSurf = titleFont.render('Wormy!', True, GREEN)
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)

    drawPressKeyMSg()
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

#退出
def terminate():
    pygame.quit()
    sys.exit()

#随机生成一个位置
def getRandomLocation():
    return {'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}

#绘制分数
def drawScore(score):
    scoreFont = pygame.font.Font('PAPYRUS.ttf', 20)
    scoreSurf = scoreFont.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect) #在屏幕显示 传入是字和位置
#根据数组绘制🐍
def drawWorm(wormCoords):
    for cood in wormCoords:
        x = cood['x'] * CELLSIZE
        y = cood['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,DARKGREEN,wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
#根据coord绘制apple
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF,RED,appleRect) #绘制 传入要绘制的视图 颜色 位置

#绘制所有的方格
def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE) :
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(x,0),(x,WINDOWHEIGHT))#pygame绘制线传入视图和颜色还有起始点和终止点
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(0,y),(WINDOWWIDTH,y))
#显示GG
def showGameOverScreen():
    gameOverFont = pygame.font.Font('PAPYRUS.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2-gameRect.height-10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMSg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

if __name__ == '__main__':
    main()
