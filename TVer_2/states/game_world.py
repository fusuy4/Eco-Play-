import pygame, os
from states.state import State

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.assests_dir, "map", "background.jpg"))

    def update(self, delta_time, actions):
        pass

    def render(self, display):
        display.blit(self.background_img, (0,0))