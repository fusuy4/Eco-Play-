import os, time, pygame
from menu import * # imports everything from menu
import random


class Game():
    def __init__(self):
        # pygame.init()
        # self.running, self.playing = True, False
        # self.DISPLAY_W, self.DISPLAY_H = 480, 270
        # self.font_name = pygame.font.get_default_font()
        # self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        # self.main_menu = MainMenu(self)
        # self.options = OptionsMenu(self)
        # self.credits = CreditsMenu(self)
        # self.curr_menu = self.main_menu
        pygame.init()
        self.GAME_W,self.GAME_H = 480, 270
        self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540

        # self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        
        self.running, self.playing = True, True

        self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
        # self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

        self.dt, self.prev_time = 0, 0 # Delta Time (Change in Time), previous time
        self.state_stack = []
        self.load_assets()
        self.load_states()

    # def check_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running, self.playing = False, False
    #             self.curr_menu.run_display = False
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RETURN: # enter key
    #                 self.START_KEY = True
    #             if event.key == pygame.K_BACKSPACE: 
    #                 self.BACK_KEY = True
    #             if event.key == pygame.K_DOWN: 
    #                 self.DOWN_KEY = True
    #             if event.key == pygame.K_UP: 
    #                 self.UP_KEY = True
    #             if event.key == pygame.K_RIGHT: 
    #                 self.RIGHT_KEY = True
    #             if event.key == pygame.K_LEFT:
    #                 self.LEFT_KEY = True
    # def reset_keys(self):
    #     self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

    def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
                    if event.key == pygame.K_a:
                        self.actions['left'] = True
                    if event.key == pygame.K_d:
                        self.actions['right'] = True
                    if event.key == pygame.K_w:
                        self.actions['up'] = True
                    if event.key == pygame.K_s:
                        self.actions['down'] = True
                    if event.key == pygame.K_p:
                        self.actions['action1'] = True
                    if event.key == pygame.K_o:
                        self.actions['action2'] = True    
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = True  

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.actions['left'] = False
                    if event.key == pygame.K_d:
                        self.actions['right'] = False
                    if event.key == pygame.K_w:
                        self.actions['up'] = False
                    if event.key == pygame.K_s:
                        self.actions['down'] = False
                    if event.key == pygame.K_p:
                        self.actions['action1'] = False
                    if event.key == pygame.K_o:
                        self.actions['action2'] = False
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = False  



    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.playing = False
            self.display.fill(self.BLACK) # canvas
            self.draw_text("Thanks for playing jit", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update() # moves image on screen
            self.reset_keys()

    
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


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
