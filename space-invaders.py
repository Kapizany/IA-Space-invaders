from pygame.locals import *
import random
import sys
import pygame
import time
import enum

class Constantes(enum.Enum):
    lifeSize = 35.0
    windowWidth = 800
    windowHeight = 600
    playerWidth = 20
    playerHeight = 30
    missileWidth = 10
    missileHeight = 20
    missilesVelocity = 8 #Missiles
    countEnemies = 5
    enemiesVelocity = 0.2
    enemiesWidth = 40
    enemiesHeight = 40
    playerVelocity = 2


class Life:
    x = 0 
    y = 0
    numberLife = 0

    def __init__(self,numberLife):
        self.numberLife = numberLife

    def drawLife(self,surface,image):
        for i in range(self.numberLife):
            surface.blit(image,(self.x,self.y + i*(Constantes.lifeSize.value + 5.0)))

    def updateLifeDown(self):
        self.numberLife -= 1

    def updateLifeUp(self):
        self.numberLife += 1

class Player:

    #Here, velocity is the same as 'step', or the numbers
    #of steps that the spaceshift make to walk.

    score = 0 
    velocity = int(Constantes.playerVelocity.value)
    direction = 0
    positionX = 350
    positionY = 520
    lenght = 5

    def __init__(self,length):
        self.lenght = self.lenght
        

    def draw(self,surface,image):
        'Using pygame blit, draw the surface of spaceship'
        surface.blit(image,(self.positionX,self.positionY))




class App:

    windowWidth = Constantes.windowWidth.value
    windowHeight = Constantes.windowHeight.value
    enemiesWidth = Constantes.enemiesWidth.value
    enemiesHeight = Constantes.enemiesHeight.value
    lifeSize = Constantes.lifeSize.value
    playerWidth = Constantes.playerWidth.value
    playerHeight = Constantes.playerHeight.value
    missileWidth = Constantes.missileWidth.value
    missileHeight = Constantes.missileHeight.value
    score = 0 
    player = 0
    invaders = 0 
    velocity = Constantes.missilesVelocity.value
    countEnemies = Constantes.countEnemies.value
    enemiesVelocity = Constantes.enemiesVelocity.value


    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._invader_surf = None
        self._missile_surf = None
        self.player = Player(5)
        self.triggerMissile = False
        self.missileX = None
        self.missileY = None
        self.enemies = []
        self.enemyX = None
        self.enemyY = None
        self.life = Life(3)


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE) 
        pygame.display.set_caption('IA_SpaceInvaders')
        self._running = True
        self._image_surf =  pygame.image.load('nave.png').convert()
        self._image_life = pygame.transform.scale (pygame.image.load('nave.png').convert(), (int(self.lifeSize),int(self.lifeSize)))
        self._invader_surf = pygame.transform.scale(pygame.image.load('enemy.png'), (int(self.enemiesWidth),int(self.enemiesHeight)))
        self._missile_surf = pygame.image.load('missile.png').convert()

    def on_event(self,event):
        if event.type == QUIT:
            self._running = False

    #Missile fire configuration
    def missileFire(self,x,y):
        'fire the missile'
        if not self.triggerMissile:
            self.triggerMissile = True
            self.missileX = x
            self.missileY = y

    def updateMissile(self):
        'update missile position'
        if self.triggerMissile:
            if self.missileY < -self._missile_surf.get_rect().size[1]:
                self.triggerMissile = False
            else:
                self.missileY -= self.velocity
    
    def missileDraw(self,surface,image):
        'Using pygame blit, draw the surface of spaceship'
        if self.triggerMissile:
            surface.blit(image,(self.missileX,self.missileY))
        
    #Enemies configuration 

    def enemyCoordinate(self):
        'restart initial position for enemies'
        self.enemyX = random.randint(10, int(self.windowWidth-(self.enemiesWidth )))
        self.enemyY = (-1)*random.randint(20,200)

    def enemiesSpawn(self):
        'The enemies will be saved on a list'
        for i in range(self.countEnemies):
            self.enemyCoordinate()
            self.enemies.append([self.enemyX,self.enemyY])
    
    def updateEnemies(self):
        if self.enemyX != None and self.enemyY != None:
            for i in range(self.countEnemies):
                self.enemies[i][1] += self.enemiesVelocity
                if self.enemies[i][1] > (self.windowHeight+10):
                    self.enemyCoordinate()
                    self.enemies[i][0], self.enemies[i][1] = self.enemyX, self.enemyY

    def enemiesDraw(self,surface,image):
        for i in range(self.countEnemies):
            surface.blit(image,(self.enemies[i][0],self.enemies[i][1]))

    #Collision mechanism

    def colisionCondition1(self):
        'breakingmyheeaart'
        'Verify colisions between enemies and shots in a loop'
        for i in range(self.countEnemies):
            if self.missileX != None and self.missileY != None:
                if self._display_surf.blit(self._missile_surf,(self.missileX,self.missileY)).collidepoint((self.enemies[i][0],self.enemies[i][1])):
                    self.enemyCoordinate()
                    self.enemies[i][0], self.enemies[i][1] = self.enemyX , self.enemyY
                    self.triggerMissile = False
                    self.player.score += 1

                    if self.player.score % 25 == 0 and self.player.score != 0:
                        self.enemiesVelocity += 0.1
                        self.player.velocity += 0.5
                        self.countEnemies += 1 

    def colisionCondition2(self):
        'Verify colisions between enemies and a spaceship'
        for i in range(self.countEnemies):
            if self.enemyX != None and self.enemyY != None:#Rect((left, top), (width, height)) -> Rect
                if pygame.Rect((self.player.positionX ,self.player.positionY),(int(Constantes.playerWidth.value),int(Constantes.playerHeight.value))).colliderect(pygame.Rect((self.enemies[i][0], self.enemies[i][1] ),(int(Constantes.enemiesWidth.value),int(Constantes.enemiesHeight.value)))):
                    self.enemyCoordinate()
                    self.enemies[i][0], self.enemies[i][1] = self.enemyX, self.enemyY
                    self.life.updateLifeDown()



    def on_loop(self):
        self.updateMissile()
        self.updateEnemies()
        self.colisionCondition1()
        self.colisionCondition2()

        if self.player.score % 100 == 0 and self.player.score != 0:
            self.player.score += 1
            self.life.updateLifeUp()
        
        if self.life.numberLife == 0:
            self._running = False



    def on_render(self):
        black = (0,0,0) #rgb
        white = (255,255,255)

        self._display_surf.fill(black)
        self.missileDraw(self._display_surf,self._missile_surf)
        self.player.draw(self._display_surf, self._image_surf)
        self.enemiesSpawn()
        self.enemiesDraw(self._display_surf,self._invader_surf)
        self.life.drawLife(self._display_surf,self._image_life)

        message = self.player.score
        font = pygame.font.Font(None, 40)
        text = font.render(str(message),1,white)
        self._display_surf.blit(text, (700,0))

        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.positionX += self.player.velocity

            elif (keys[K_LEFT]):
                self.player.positionX -= self.player.velocity

            if (keys[K_ESCAPE]):
                self._running = False
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.missileFire(self.player.positionX,self.player.positionY)
                    #self.missile.triggerMissile = False
                elif event.type == pygame.QUIT:
                        self._running = False
                    

            self.on_loop()
            self.on_render()
        self.on_cleanup()
        
    
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()