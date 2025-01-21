import pygame, os
from states.state import State
from states.game_world import Game_World
from states.credits import Credits
from states.learn import Learn

class Menu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        # Set the menu
        self.menu_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "mainmenu.PNG"))
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (self.game.GAME_W*.5, self.game.GAME_H*.6)
        self.background_img = pygame.image.load(os.path.join(self.game.images_dir, "painting.PNG"))
        # Set the cursor and menu states
        self.menu_options = {0 :"Play", 1 : "Credits", 2 :"Learn", 3 : "Exit"}
        self.index = 0
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 65
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 26, self.cursor_pos_y

    def update(self, delta_time, actions):  
        self.update_cursor(actions)      
        if actions["start"]:
            self.transition_state()
        if actions["action1"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        # self.prev_state.render(display)
        display.blit(self.background_img, (0,0))
        display.blit(self.menu_img, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)

    def transition_state(self):
        if self.menu_options[self.index] == "Play": # Play Game
            new_state = Game_World(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Credits": # Credits
            new_state = Credits(self.game)
            self.game.state_stack.pop()
            new_state.enter_state()
        elif self.menu_options[self.index] == "Learn": 
            new_state = Learn(self.game)
            self.game.state_stack.pop()
            new_state.enter_state()
        elif self.menu_options[self.index] == "Exit": # Exit
            self.game.playing = False
            self.game.running = False


    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 40)
