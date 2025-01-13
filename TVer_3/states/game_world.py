import pygame, os
from states.state import State
from states.pause_menu import PauseMenu
from assets.sprites.game_objects import FallingObjects
from states.game_over_menu import GameOver
import random
import time

class Game_World(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.images_dir, "painting.PNG"))
        
        # objects
        self.base_file = (os.path.join(self.game.assets_dir, "sprites"))
        self.list = [
            FallingObjects(os.path.join(self.base_file, "plasticbottle.png"), 2, (0, 0), True),
            # FallingObjects(os.path.join(self.base_file, "chipbag.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "cigarette.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "plasticbag.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "bananapeel.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "can.png"), 2, (0, 0), True),
            FallingObjects(os.path.join(self.base_file, "pizza.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "cardboard.png"), 2, (0, 0), True),
            FallingObjects(os.path.join(self.base_file, "milkjug.png"), 2, (0, 0), True),
            FallingObjects(os.path.join(self.base_file, "paper.png"), 2, (0, 0), True),
            FallingObjects(os.path.join(self.base_file, "straw.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "battery.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "toothbrush.png"), 2, (0, 0), True)
        ]

        # Garbage Bin
        self.recyclebin = pygame.image.load(os.path.join(self.base_file, 'recyclebin.png'))
        self.recyclebin_rect = self.recyclebin.get_rect()
        self.vel = 3
        self.recyclebin_rect.bottom = self.game.GAME_H + 5
        self.recyclebin_rect.centerx = self.game.GAME_W / 2
        self.direction_x = self.recyclebin_rect.centerx

        self.score = 0
        self.score_change = 10
        self.cur_trash = self.spawn_new_trash()
        self.start_time = time.time()


    def spawn_new_trash(self):
        trash = self.list[int(random.uniform(0, len(self.list)))]
        trash.randomSpeed()
        trash.randomPosition()
        trash.rect.top = -100
        trash.rect.centerx = random.uniform(0, 480)
        return trash

    def update(self, delta_time, actions):
        if actions["action1"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        
        elapsed_time = time.time() - self.start_time
        if (elapsed_time >= 30):
            if self.score > self.game.high_score:
                self.game.high_score = self.score
                self.game.new_high = True
            else:
                self.game.new_high = False
            
            self.game.past_score = self.score
            new_state = GameOver(self.game)
            new_state.enter_state()
            print("hairline")
            print(elapsed_time)

        # Move the falling trash
        self.cur_trash.randomSpeed()
        self.cur_trash.randomPosition()
        self.cur_trash.rect.y += self.cur_trash.speed

        pygame.display.set_caption("Playing")
        
        # Check collisions
        if pygame.Rect.colliderect(self.recyclebin_rect, self.cur_trash.rect):
            if self.cur_trash.recycleable:
                self.score += self.score_change
            else:
                self.score -= self.score_change
            self.cur_trash = self.spawn_new_trash()

        # Handle missed trash
        if self.cur_trash.rect.top > 270: 
            self.cur_trash = self.spawn_new_trash()


        # Move the recycling bin
        if actions["left"] and self.recyclebin_rect.left > 0:
            self.recyclebin_rect.x -= self.vel
        if actions["right"] and self.recyclebin_rect.right < 480:
            self.recyclebin_rect.x += self.vel

        pygame.time.delay(7)


    def render(self, display):
        display.blit(self.background_img, (0,0))
        display.blit(self.recyclebin, self.recyclebin_rect)
        display.blit(self.cur_trash.image, self.cur_trash.rect)
        self.game.draw_text('Score: ', 15, 60, 10)
        self.game.draw_text('Press \'P\' to Pause!', 8, 400, 10)
        self.game.draw_text(f'{self.score}', 15, 120, 10)