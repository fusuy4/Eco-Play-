import os, time, pygame
import pygame.pypm
from states.title import Title
import random


class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W,self.GAME_H = 480, 270
        self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
        self.dt, self.prev_time = 0, 0 # Delta Time (Change in Time), previous time
        self.high_score = 0
        self.past_score = 0
        self.new_high = True
        self.state_stack = []
        self.load_assets()
        self.load_states()
    
    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self): 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.actions['left'] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.actions['right'] = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.actions['up'] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.actions['down'] = True

                    if event.key == pygame.K_p:
                        self.actions['action1'] = True
                    if event.key == pygame.K_o:
                        self.actions['action2'] = True    
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = True  

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.actions['left'] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.actions['right'] = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.actions['up'] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.actions['down'] = False
                    if event.key == pygame.K_p:
                        self.actions['action1'] = False
                    if event.key == pygame.K_o:
                        self.actions['action2'] = False
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = False
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions) # check whatever is at the end of the stack/list

    def render(self): # updates the game window we see on screen
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()

    def get_dt(self): # computes delta time
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
    
    # def draw_text(self, surface, text, color, x, y): # surface we draw the text on
    #     text_surface = self.font.render(text, True, color) #  creates an image (Surface) of the text
    #     # text_surface.set_colorkey((0,0,0))
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x, y)
    #     surface.blit(text_surface, text_rect) # blits the image onto another Surface.
    def draw_text(self, text, size, x, y):
        fonto = pygame.font.Font(self.font, size)
        text_surface = fonto.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_canvas.blit(text_surface, text_rect)

    def load_assets(self): # creates different pointers to difference directories
        self.assets_dir = os.path.join("assets") # os makes file paths for us
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.font = (os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"))
        self.sounds_dir = (os.path.join(self.assets_dir, "sounds"))


    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)


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



if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()