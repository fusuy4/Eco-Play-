import os, time, pygame
from menu import * # imports everything from menu
import random


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing, self.runningyerr, self.game_playing = True, False, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 733
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.background = pygame.image.load("images/background.jpg")
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'opensans.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.playing = False
            self.window.blit(self.display, (0,0))
            # self.draw_text("Thanks for playing jit", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)

            # test
            #######
            recyclebin = pygame.image.load('images/recyclebin.png')
            recyclebin_rect = recyclebin.get_rect()
            vel = 3
            recyclebin_rect.bottom = 800
            recyclebin_rect.centerx = 250

            # individual Falling Objects, using hand-drawn images
            plasticBottle = FallingObjects("images/plasticbottle.png", 2, (300, 125), True)
            chipBag = FallingObjects("images/chipbag.png", 2, (300, 125), False)
            cigarette = FallingObjects("images/cigarette.png", 2, (300, 125), False) # not recycle
            plasticBag = FallingObjects("images/plasticbag.png", 2, (300, 125), False )
            bananaPeel = FallingObjects("images/bananapeel.png", 2, (300, 125), False)
            can = FallingObjects("images/can.png", 2, (300, 125), True)

            # score counter
            score = 0
            score_change = 10

            # list to randomize what trash object falls from sky
            list = [plasticBottle, chipBag, cigarette, plasticBag, bananaPeel, can]

            # assigns initial random piece of trash, and initial random values of trash 
            fallingtrash = list[int (random.uniform(0, 6))]
            fallingtrash.randomSpeed()
            fallingtrash.randomPosition()

            # Running game
            self.runningyerr = True
            self.game_playing = True

            while self.runningyerr:
                self.check_events()

                pygame.display.set_caption("Playing")
                
                self.window.blit(self.display, (0,0))
                
                if self.game_playing == True:

                    self.display.blit(self.background, (0,0))

                    
                    # checks if recyclable trash is collected
                    if pygame.Rect.colliderect(recyclebin_rect, fallingtrash.rect) and fallingtrash.recycleable == True:
                        score = score + score_change
                        fallingtrash = list[int (random.uniform(0, 6))]
                        fallingtrash.randomSpeed()
                        fallingtrash.randomPosition()
                        fallingtrash.rect.top = -320
                        fallingtrash.rect.centerx = random.uniform(150, 450)
                
                    # checks if non-recyclable trash is collected
                    if pygame.Rect.colliderect(recyclebin_rect, fallingtrash.rect) and fallingtrash.recycleable == False:
                        score = score - score_change
                        fallingtrash = list[int (random.uniform(0, 6))]
                        fallingtrash.randomSpeed()
                        fallingtrash.randomPosition()
                        fallingtrash.rect.top = -320
                        fallingtrash.rect.centerx = random.uniform(150, 450)

                    # checks if player has missed trash
                    if fallingtrash.rect.top > 800: 
                        fallingtrash = list[int (random.uniform(0, 6))]
                        fallingtrash.randomSpeed()
                        fallingtrash.randomPosition()
                        fallingtrash.rect.top = -320
                        fallingtrash.rect.centerx = random.uniform(150, 450)

                    # this is what updates the position of trash
                    else:
                        fallingtrash.rect.y += fallingtrash.speed
                        
                    # event handler
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                game_paused = True
                        if event.type == pygame.QUIT:
                            self.runningyerr = False
                            self.playing = False
                            self.game_playing = False

                    # player input controls
                    keys = pygame.key.get_pressed()
                    

                    # if left arrow key is pressed
                    if keys[pygame.K_LEFT] and recyclebin_rect.left > 0:
                        # decrement in x co-ordinate, move trashbin left 
                        recyclebin_rect.x -= vel

                    # if right arrow key is pressed, move trashbin right
                    if keys[pygame.K_RIGHT] and recyclebin_rect.right < 800:
                        # increment in x co-ordinate
                        recyclebin_rect.x += vel

                    # draws updated position of objects on screen
                    self.display.blit(recyclebin, recyclebin_rect)  
                    self.display.blit(fallingtrash.image, fallingtrash.rect)
                    
                    # score is incremented here
                    self.draw_text(f'Score: {score}', 20, 10, 10)

                    # updates display
                    pygame.display.update()



            self.window.blit(self.display, (0,0))
            pygame.display.flip() # moves image on screen
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                self.runningyerr = False
                self.game_playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # enter key
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE: 
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN: 
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP: 
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT: 
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False



# class dedicated to the falling pieces of trash
class FallingObjects:
    def __init__(self, image_path, speed, position, num):
        self.recycleable = bool(num)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.top = self.rect.top
        self.speed = speed
        self.position = position

    def randomSpeed(self):
        self.speed = random.uniform(2, 4.5)

    def randomPosition(self):
        self.position = random.uniform(0, 800)


