'''
Pygame version 2.1.2
'''

import pygame
from random import random

##### Set up static variables #####
BG_COLOUR = (255, 255, 255)             # white colour value
TEXT_COLOUR = (0, 0, 0)                 # black colour value
SCREEN_WIDTH = 800                      # width of window 
SCREEN_HEIGHT = 600                     # height of window
FPS = 60                                # frames per second

CANNON_SPEED = 5                        # speed of cannon
BALLOON_SPEED = 2                       # speed of balloon
BULLET_SPEED = BALLOON_SPEED * 10       # speed of bullet

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, speed, imagePath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect(center = position)
        self.speed = speed

class Cannon(Sprite):
    def __init__(self):
        super().__init__((SCREEN_WIDTH * 4/5, SCREEN_HEIGHT / 2), CANNON_SPEED, 'assets/cannon.png')

    def moveUp(self):
        '''
        move cannon up
        '''
        if inFrame(self.rect.x, self.rect.top - self.speed):    # if cannon won't move out of frame
            self.rect.centery -= self.speed                     # move up

    def moveDown(self):
        '''
        move cannon down
        '''
        if inFrame(self.rect.x, self.rect.bottom + self.speed): # if cannon won't move out of frame
            self.rect.centery += self.speed                     # move down

class Balloon(Sprite):
    def __init__(self):
        super().__init__((SCREEN_WIDTH * 1/8, SCREEN_HEIGHT / 2), BALLOON_SPEED, 'assets/balloon.png')
        self.direction = random() >= 0.5            # direction balloon is travelling in
        self.directionChange = FPS                  # number of frames to change direction
        self.count = 0                              # count for when to change direction  
    
    def move(self):
        '''
        move balloon randomly up or down
        '''
        if self.count == self.directionChange:      # if it is time for a direction change
            self.direction = random() >= 0.5        # randomly choose direction
            self.count = 0                          # restart count
        else:
            if self.direction:
                if inFrame(self.rect.x, self.rect.bottom + self.speed):   # if balloon won't move out of frame
                    self.rect.centery += self.speed     # move down
                else:                                   # if balloon has reached bottom
                    self.direction = False              # change direction to move up
            else:
                if inFrame(self.rect.x, self.rect.top - self.speed):  # if balloon won't move out of frame
                    self.rect.centery -= self.speed     # move up
                else:                                   # if balloon has reached top
                    self.direction = True               # change direction to move down
            self.count += 1                             # increment count


class Bullet(Sprite):
    def __init__(self, position):
        super().__init__(position, BULLET_SPEED, 'assets/bullet.png')

    def shoot(self):
        '''
        move bullet and return false if bullet has missed the target
        '''
        self.rect.centerx -= self.speed                         # move left
        if not inFrame(self.rect.centerx, self.rect.centery):   # if bullet missed (is out of frame)
            self.kill()                                         # remove bullet
            return False
        return True
    
def inFrame(x, y):
    '''
    return whether position is in the frame of the screen
    '''
    return x >= 0 and x <= SCREEN_WIDTH and y >= 0 and y <= SCREEN_HEIGHT

def main():
    ##### set up pygame #####
    pygame.init()                                                   # initialise modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # set window size
    pygame.display.set_caption('Balloon Shooting Game')             # set window name
    font = pygame.font.Font(None, 40)                               # load the fonts
    clock = pygame.time.Clock()
    
    ##### game variables #####
    close = False                           # if user closes game
    gameOver = False                        # if user finishes game
    missedShots = 0                         # number of bullets that have missed the balloon
    keyPressed = {                          # key that user is pressing
        'up': False,
        'down': False
    }
    
    ###### set up sprites ######
    sprites = pygame.sprite.Group()         # group of all sprites
    bullets = pygame.sprite.Group()         # group of all bullets
    cannon = Cannon()                       # create cannon
    balloon = Balloon()                     # create balloon
    sprites.add(cannon)                     # add cannon to group
    sprites.add(balloon)                    # add balloon to group

    while not close:                                    # while user has not closed the game
        screen.fill(BG_COLOUR)                          # set background colour
        if not gameOver:                                # if user has not won game
            for event in pygame.event.get():            # for each event in queue
                if event.type == pygame.QUIT:           # if user clicks x, close game
                    close = True
                elif event.type == pygame.KEYDOWN:      # if user presses a key
                    if event.key == pygame.K_UP:        # up arrow
                        keyPressed['up'] = True
                    elif event.key == pygame.K_DOWN:    # down arrow
                        keyPressed['down'] = True
                    elif event.key == pygame.K_SPACE:       # space to shoot
                        bullet = Bullet(cannon.rect.center) # create bullet
                        bullets.add(bullet)
                        sprites.add(bullet)
                elif event.type == pygame.KEYUP:        # if user releases key
                    keyPressed['up'] = False
                    keyPressed['down'] = False

            ###### cannon position ######
            if keyPressed['up']:                    # press up arrow
                cannon.moveUp()       
            elif keyPressed['down']:                # press down arrow
                cannon.moveDown()

            ###### balloon position ######
            balloon.move()

            ###### bullet position ######
            for bullet in bullets:                  # for all bullets
                if not bullet.shoot():              # shoot bullet and if bullet missed,
                    missedShots += 1                # increment

            ###### display sprites ######
            sprites.draw(screen)

            if pygame.sprite.spritecollide(balloon, bullets, True):    # if any bullet hits balloon
                gameOver = True                                        # game completed

        else:                                           # user has won game
            for event in pygame.event.get():            # for each event in queue
                if event.type == pygame.QUIT:           # if user clicks x, close game
                    close = True
            text = font.render("Game Won! " + "Missed Shots: " + str(missedShots), True, TEXT_COLOUR) # display missed shots
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)

        pygame.display.update()             # update game
        clock.tick(FPS)                     # max 60 loops per second

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
