import pygame, os
from states.state import State
from states.pause_menu import PauseMenu
from assets.sprites.game_objects import FallingObjects
import random

class Game_World(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.images_dir, "background.png"))
        self.player = Player(self.game)

        # Initialize trash objects
        self.base_file = os.path.join(self.game.assets_dir, "sprites")
        self.list = [
            FallingObjects(os.path.join(self.base_file, "plasticbottle.png"), 2, (0, 0), True),
            FallingObjects(os.path.join(self.base_file, "chipbag.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "cigarette.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "plasticbag.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "bananapeel.png"), 2, (0, 0), False),
            FallingObjects(os.path.join(self.base_file, "can.png"), 2, (0, 0), True)
        ]

        # Garbage bin
        self.recyclebin = pygame.image.load(os.path.join(self.base_file, 'recyclebin.png'))
        self.recyclebin_rect = self.recyclebin.get_rect()
        self.vel = 3
        self.recyclebin_rect.bottom = self.game.GAME_H - 97
        self.recyclebin_rect.centerx = self.game.GAME_W / 2

        self.score = 0
        self.score_change = 10
        self.cur_trash = self.spawn_new_trash()

    def spawn_new_trash(self):
        trash = self.list[int(random.uniform(0, len(self.list)))]
        trash.randomSpeed()
        trash.randomPosition()
        trash.rect.top = -100
        trash.rect.centerx = random.uniform(0, 480)
        return trash

    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()

        # Move the falling trash
        self.cur_trash.randomSpeed()
        self.cur_trash.randomPosition()
        self.cur_trash.rect.y += self.cur_trash.speed

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

        self.game.reset_keys()
        self.player.update(delta_time, actions)

    def render(self, display):
        display.blit(self.background_img, (0, 0))
        display.blit(self.recyclebin, self.recyclebin_rect)
        display.blit(self.cur_trash.image, self.cur_trash.rect)
        self.game.draw_text(f'Score: {self.score}', 0.2, self.game.GAME_W / 2, 5)
        self.player.render(display)

class Player:
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 200, 200
        self.current_frame, self.last_frame_update = 0, 0

        self.base_file = os.path.join(self.game.assets_dir, "sprites")  
        self.recyclebin = pygame.image.load(os.path.join(self.base_file, 'recyclebin.png'))
        self.recyclebin_rect = self.recyclebin.get_rect()
        self.vel = 3
        self.recyclebin_rect.bottom = 400
        self.recyclebin_rect.centerx = 250

    def update(self, delta_time, actions):
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        self.position_x += 100 * delta_time * direction_x
        self.position_y += 100 * delta_time * direction_y

        # Keep player within screen bounds
        self.position_x = max(0, min(self.position_x, self.game.GAME_W - self.recyclebin_rect.width))
        self.position_y = max(0, min(self.position_y, self.game.GAME_H - self.recyclebin_rect.height))

    def render(self, display):
        display.blit(self.curr_image, (self.position_x, self.position_y))

    def load_sprites(self):
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [], [], [], []
        for i in range(1, 5):
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) + ".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) + ".png")))
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites
