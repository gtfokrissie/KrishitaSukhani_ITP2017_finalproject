import pygame
from pygame.locals import *
import sys
from  pygame.sprite import *
from pygame import *
pygame.init()

crash_sound = pygame.mixer.Sound("break.WAV")
class textrect(Sprite):
    def __init__(self, fontstyle , text , fontsize , xpos , ypos ,R, G , B ):
        Sprite.__init__(self)
        self.font= pygame.font.SysFont(fontstyle,fontsize)
        self.image= self.font.render(text, False,(R,G,B))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos



def winner():
    Congratulations = textrect("Arial ","Congratulations! You have won the game!",36,50,300,255,0,0)
    screen = pygame.display.set_mode((600, 600))
    pygame.mouse.set_visible(True)

    while True :
        screen.fill((0,0,0))
        display.update()
        congrats = Group(Congratulations)
        congrats.draw(screen)
        c = event.wait()
        if Congratulations.rect.collidepoint(mouse.get_pos()):
             Congratulations = textrect("Arial ","Congratulations! You have won the game!",36,50,300,0,255,0)
             if c.type == MOUSEBUTTONDOWN:
                 pygame.quit()
        else:
            Congratulations = textrect("Arial ","Congratulations! You have won the game!",36,50,300,255,0,0)
        pygame.display.update()


def end():
    go = textrect("Arial ","Game Over",50,200,300,0,255,0)
    restart = textrect("Arial","Restart",50,200,200,0,0,255)
    screen = pygame.display.set_mode((600, 600))
    pygame.mouse.set_visible(True)

    while True :
        screen.fill((0,0,0))
        options = Group(go,restart)
        options.draw(screen)
        display.update()
        b = event.wait()
        if restart.rect.collidepoint(mouse.get_pos()):
            restart = textrect("Arial","Restart",50,200,200,0,0,255)
            if b.type == MOUSEBUTTONDOWN:
                level1().main()
        else:
            restart = textrect("Arial","Restart",50,200,200,255,0,0)

        if go.rect.collidepoint(mouse.get_pos()):
            go = textrect("Arial","GameOver",50,200,300,255,0,255)
            if b.type == MOUSEBUTTONDOWN:
                pygame.quit()
        else:
            go = textrect("Arial","GameOver",50,200,300,0,255,0)

            pygame.display.update()

class level1:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))

        # pygame.display.set_mode((width, height)) - This will launch a window of the desired size
        self.blocks = []
        self.paddle = [[pygame.Rect(320, 520, 60, 20), 120],# ( x ,y , width, height)
                [pygame.Rect(360, 520, 60, 20), 100],
                [pygame.Rect(400, 520, 60, 20), 80],
                [pygame.Rect(420, 520, 60, 20), 45], ]
        self.ball = pygame.Rect(300, 500 , 5, 5)
        self.direction = -2 # the more you increasse the direction the more difficult the game bcomes
        self.yDirection = -1
        self.angle = 80
        self.speeds = {
            120:(-10, -3),
            100:(-10, -8),
            80:(10, -8),
            45:(10, -3),
        }
        self.swap = { # what this does is that when the paddle catches the ball the ball will bounce to the wall and it will keep bouncing till it either reaches the top OR it breaks a brick
            120:45,
            45:120,
            100:80,
            80:100,}
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25,(400,300))
        self.score = 0

    def createBlocks(self):
        self.blocks = []
        y = 50 # y axis of the block in the game
        for brick in range(100 // 20):#positions the bricks properly throughout the x axis
            x = 210  # x axis of the blocks in the game
            for _ in range(300 // 25 - 5):  # the 400 inside d vracket explains how many blocks r there in this stage of the game
                block = pygame.Rect(x, y, 20, 10)# (basically shows x axis, y axis, the width of the bricks, the height of the bricks)
                self.blocks.append(block)
                x += 30
            y += 40

    def ballUpdate(self):# movements of the ball throughout the game

        for _ in range(2):
            speed = self.speeds[self.angle]
            xMovement = True #shows the action carried out when the ball moves
            if _:
                self.ball.x += speed[0] * self.direction
            else:
                self.ball.y += speed[1] * self.direction * self.yDirection
                xMovement = False
            if self.ball.x <= 0 or self.ball.x >= 600: # limits where the ball can go so it will not allow the ball to go outside of the screen
                self.angle = self.swap[self.angle]# while playing the ball is enabled to work properly
                if self.ball.x <= 0:
                    self.ball.x = 1# this is the minimal x axis the bll can go so that d ball does not go out of the frame
                else:
                    self.ball.x = 599 # this is the maximum x axis the ball can go
            if self.ball.y <= 0:
                self.ball.y = 1
                self.yDirection *= -1

            for paddle in self.paddle:
                if paddle[0].colliderect(self.ball):
                    self.angle = paddle[1]
                    self.direction = -1
                    self.yDirection = -1

            check = self.ball.collidelist(self.blocks)
            if check != -1:
                block = self.blocks.pop(check)
                pygame.mixer.Sound.play(crash_sound)
                if xMovement:
                    self.direction *= -1
                self.yDirection *= -1
                self.score += 1
                if self.score == 35:# 35 bcoz there are 30 bricks so once you break them all you move on to thext stage
                    level2().main()
            if self.ball.y > 600:#if the ball exceeds this limit of y axis meaning it has already fell n therefore d game shoulld end

                end()

    def paddleUpdate(self):
        pos = pygame.mouse.get_pos()#enables you to control the paddle with your mouse or your touchpad
        on = 0
        for p in self.paddle:
            p[0].x = pos[0] + 20 * on
            on += 1
    def main(self):
        pygame.mouse.set_visible(False)#does not show the mouse
        clock = pygame.time.Clock()# creates an object that helps track time
        self.createBlocks()
        background_image= pygame.image.load("level1.jpg").convert()

        while True:
          clock.tick(20)#as the level progresses the clock tick increases the fps
          for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
          self.screen.blit(background_image,[0,0])
          self.paddleUpdate()
          self.ballUpdate()

          for block in self.blocks:
                pygame.draw.rect(self.screen, (255,0,255), block)
          for paddle in self.paddle:
                pygame.draw.rect(self.screen, (255,255,255), paddle[0])
          pygame.draw.rect(self.screen, (255,255,255), self.ball)
          self.screen.blit(self.font.render(str(self.score), -1, (255,255,255)), (300, 537)) # draws the image onto the screen
          pygame.display.update()



class level2:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        #pygame.display.set_mode((width, height)) - This will launch a window of the desired size
        self.blocks = []
        self.paddle = [[pygame.Rect(300, 400, 30, 20), 140],# as the game levels up the speed becomes faster and the paddle goes higher as well as the angle
                [pygame.Rect(320, 400, 30, 20), 120],
                [pygame.Rect(340, 400, 30, 20), 100],
                [pygame.Rect(360, 400, 30, 20), 65],]
        self.ball = pygame.Rect(300, 500 , 5, 5)
        self.direction = -2
        self.yDirection = -1
        self.angle = 100
        self.speeds = {
            140:(-10, -3),
            120:(-10, -8),
            100:(10, -8),
            65:(10, -3),
        }
        self.swap = {
            140:65,
            65:140,
            120:100,
            100:120,
        }
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)
        self.score = 0

    def createBlocks(self):
        self.blocks = []
        y = 100#y axis of the block in the game
        for __ in range(200 // 20):
            x = 210  #x axis of the blocks in the game
            for _ in range(200 // 20 - 5):  #the 200 inside d bracket explains how many blocks r there in this stage of the game
                block = pygame.Rect(x, y, 25, 10)
                self.blocks.append(block)
                x += 27
            y += 14

    def ballUpdate(self):
        for _ in range(2):
            speed = self.speeds[self.angle]
            xMovement = True
            if _:
                self.ball.x += speed[0] * self.direction
            else:
                self.ball.y += speed[1] * self.direction * self.yDirection
                xMovement = False
            if self.ball.x <= 0 or self.ball.x >= 600:
                self.angle = self.swap[self.angle]
                if self.ball.x <= 0:
                    self.ball.x = 1
                else:
                    self.ball.x = 599
            if self.ball.y <= 0:
                self.ball.y = 1
                self.yDirection *= -1

            for paddle in self.paddle:
                if paddle[0].colliderect(self.ball):
                    self.angle = paddle[1]
                    self.direction = -1
                    self.yDirection = -1
                    break
            check = self.ball.collidelist(self.blocks)
            if check != -1:
                block = self.blocks.pop(check)
                pygame.mixer.Sound.play(crash_sound)
                if xMovement:
                    self.direction *= -1
                self.yDirection *= -1
                self.score += 1
            if self.score == 50:
                winner()
        if self.ball.y > 600:
             end()


    def paddleUpdate(self):

        pos = pygame.mouse.get_pos()
        on = 0
        for p in self.paddle:
            p[0].x = pos[0] + 20 * on
            on += 1
    def main(self):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        self.createBlocks()
        background_image= pygame.image.load("LEVEL2.jpg").convert()
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self.screen.blit(background_image,[0,0])
            self.paddleUpdate()
            self.ballUpdate()

            for block in self.blocks:
                pygame.draw.rect(self.screen, (255,0,255), block)
            for paddle in self.paddle:
                pygame.draw.rect(self.screen, (255,255,255), paddle[0])
            pygame.draw.rect(self.screen, (255,255,255), self.ball)
            self.screen.blit(self.font.render(str(self.score), -1, (255,255,255)), (400, 550))
            pygame.display.update()

def menu():
    pygame.init()
    screen= pygame.display.set_mode((320,480))
    pygame.display.set_caption('Brick Breaker')
    bg = pygame.image.load("1.JPG")
    start = textrect("Arial ","Start",30,100,130,255,255,255)
    quit = textrect("Arial","Quit",30,100,300,255,255,255)
    while True :
        screen.blit(bg,(0,0))
        text = Group(start,quit)
        text.draw(screen)
        a = event.wait()
        if start.rect.collidepoint(mouse.get_pos()):
            start = textrect("Arial","Start",30,100,130,0,0,255)
            if a.type == MOUSEBUTTONDOWN:
                level1().main()
                level2().main()

        else:
            start = textrect("Arial","Start",30,100,130,255,255,255)

        if quit.rect.collidepoint(mouse.get_pos()):
            quit = textrect("Arial","Quit",30,100,300,0,255,0)
            if a.type == MOUSEBUTTONDOWN:
               pygame.quit()
        else:
            quit = textrect("Arial","Quit",30,100,300,255,255,255)

            pygame.display.update()
menu()

def end():
    go = textrect("Arial ","Game Over",50,200,300,0,255,0)
    restart = textrect("Arial","Restart",50,200,200,0,0,255)
    screen = pygame.display.set_mode((600, 600))
    pygame.mouse.set_visible(True)

    while True :
        screen.fill((0,0,0))
        options = Group(go,restart)
        options.draw(screen)
        display.update()
        b = event.wait()
        if restart.rect.collidepoint(mouse.get_pos()):
            restart = textrect("Arial","Restart",50,200,200,0,0,255)
            if b.type == MOUSEBUTTONDOWN:
                level1().main()
        else:
            restart = textrect("Arial","Restart",50,200,200,255,0,0)

        if go.rect.collidepoint(mouse.get_pos()):
            go = textrect("Arial","GameOver",50,200,300,255,0,255)
            if b.type == MOUSEBUTTONDOWN:
                pygame.quit()
        else:
            go = textrect("Arial","GameOver",50,200,300,0,255,0)

            pygame.display.update()



if __name__ == "__main__":
    level1().main()

