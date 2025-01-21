import pygame, os
from states.state import State

class Learn(State):
    def __init__(self, game): 
        State.__init__(self, game)
        self.learnScreen = pygame.image.load(os.path.join(self.game.images_dir, "learn.png"))


    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.state_stack.pop()            

    def render(self, display):
        display.fill((255, 255, 255))
        self.game.get_events() # gathers player input info
        display.blit(self.learnScreen, (0,0))