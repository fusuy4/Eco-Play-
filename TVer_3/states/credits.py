import pygame, os
from states.state import State
from states.game_world import Game_World


class Credits(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.images_dir, "background.png"))

    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.state_stack.pop()

    def render(self, display):
        display.blit(self.background_img, (0,0))
        self.game.get_events() # gathers player input info
        self.game.draw_text('Credits', 20, self.game.GAME_W / 2, self.game.GAME_H / 2 - 20)
        self.game.draw_text('Made by me', 15, self.game.GAME_W / 2, self.game.GAME_H / 2 + 10)
