import pygame, os
from states.state import State

class GameOver(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        # Set the menu
        self.menu_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "menu.png"))
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (self.game.GAME_W*.5, self.game.GAME_H*.4)
        self.background_img = pygame.image.load(os.path.join(self.game.images_dir, "background.png"))
        # Set the cursor and menu states
        self.menu_options = {0 :"Party", 1 : "Items", 2 :"Magic", 3 : "Exit"}
        self.index = 0
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 38
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_pos_y
        if (self.game.new_high):
            self.display_high = True
            self.game.new_high = False
        else:
            self.display_high = False


    def update(self, delta_time, actions):  
        self.update_cursor(actions)      
        if actions["start"]:
            self.transition_state()
        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        # self.prev_state.render(display)
        display.blit(self.background_img, (0,0))
        display.blit(self.menu_img, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)
        if (self.display_high):
            self.game.draw_text((f'New High Score! : {self.game.high_score}'), 15, self.game.GAME_W*.5, self.game.GAME_H*.3)
        else:
            self.game.draw_text((f'Best Score : {self.game.high_score}'), 15, self.game.GAME_W*.5, self.game.GAME_H*.3)
            self.game.draw_text((f'Your Score : {self.game.past_score}'), 15, self.game.GAME_W*.5, self.game.GAME_H*.2)

    def transition_state(self):
        from states.game_world import Game_World
        if self.menu_options[self.index] == "Party": # Restart
            self.game.state_stack.pop()
            new_state = Game_World(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Items": # Credits
            pass
        elif self.menu_options[self.index] == "Magic": 
            pass
        elif self.menu_options[self.index] == "Exit": # Exit
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()


    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)
