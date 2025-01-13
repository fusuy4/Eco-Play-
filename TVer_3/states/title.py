import pygame, os
from states.state import State
from states.game_world import Game_World
from states.menu import Menu


class Title(State):
        # this init is basically a constructor thats automatically called when 
        # an instance of the class is created
        def __init__(self, game): 
            State.__init__(self, game)
            self.titleScreen = pygame.image.load(os.path.join(self.game.images_dir, "titlescreen.PNG")) # change
            self.menu_mus = pygame.mixer.music.load(os.path.join(self.game.sounds_dir, "MainMenu.mp3"))


        def update(self, delta_time, actions):
            # if actions["start"]:
            #     new_state = Game_World(self.game)
            #     new_state.enter_state()
            # self.game.reset_keys()
            if actions["start"]:
                new_state = Menu(self.game)
                new_state.enter_state()
                pygame.mixer.music.play()                
            self.game.reset_keys()
            

        def render(self, display):
              display.fill((255, 255, 255))
              display.blit(self.titleScreen, (0,0))
