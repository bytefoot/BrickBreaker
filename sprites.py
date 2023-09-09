import pygame
import pygame.mixer
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)
import pygame.gfxdraw
from random import choice

import config
from config import PY_SPEED, BALL_SPEEDS
from util import colors

def sgn(i):
    # to give sign of `i`
    return -1 if i < 0 else 1

# colour of paddle and ball
PLAYER_COLOR =  (207, 206, 198)

# Sound effects
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.wav")

class Brick(pygame.sprite.Sprite):
    # Brick spirte
    def __init__(self, x, y):
        super(Brick, self).__init__()
        self.surf = pygame.Surface((config.BRICK_W, config.BRICK_H))
        # fill bricks with random colors
        self.surf.fill(choice(colors))
        self.rect = self.surf.get_rect(top=y, left=x)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, limit_l, limit_r):
        super(Player, self).__init__()
        # self.surf = pygame.image.load("Paddle.png")
        self.surf = pygame.surface.Surface((100, 10))
        self.surf.fill(PLAYER_COLOR)
        self.rect = self.surf.get_rect(center=(x, y))
        self.limit_l, self.limit_r = limit_l, limit_r

    def update(self, pressed_keys):
        # Move the sprite based on user keypresses
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-PY_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(PY_SPEED, 0)

        # Keep player on the screen
        if self.rect.left < self.limit_l:
            self.rect.left = self.limit_l
        if self.rect.right > self.limit_r:
            self.rect.right = self.limit_r


class Ball(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, x, y, bounds):
        # Call the parent class (Sprite) constructor
        super().__init__()

        radius = 7
        self.surf = pygame.Surface((2*radius+1, 2*radius+1), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, PLAYER_COLOR, (radius, radius), radius)
        # setting position
        self.init_p = (x-radius,y-radius)
        self.rect = self.surf.get_rect(center = (x-radius,y-radius))

        self.bounds = bounds
        self.velocity = [0, 0]

    def update(self):
        # updating according to velocity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # to check in bound of the ball
        x1, y1, x2, y2 = self.bounds

        if self.rect.left < x1:
            self.rect.left = x1
            self.velocity[0] *= -1
            pygame.mixer.Sound.play(plob_sound)

        if self.rect.right > x2:
            self.rect.right = x2
            self.velocity[0] *= -1
            pygame.mixer.Sound.play(plob_sound)

        if self.rect.top < y1:
            self.rect.top = y1
            self.velocity[1] *= -1
            pygame.mixer.Sound.play(plob_sound)

        if self.rect.bottom > y2:
            self.rect.bottom = y2
            # self.velocity[1] *= -1
            self.velocity = [0, 0]
            return True
        return False
    
    def check_paddle_collision(self, rect):
        # checkking collision with paddle
        # velocity condition to avoid considering 1 collision as multiple collisions
        if self.rect.colliderect(rect):
            pygame.mixer.Sound.play(plob_sound)
            if abs(self.rect.top - rect.bottom) < 10 and self.velocity[1] < 0:
                self.rect.top = rect.bottom
                self.velocity[1] *= -1
            if abs(self.rect.bottom - rect.top) < 10 and self.velocity[1]> 0:
                self.rect.bottom = rect.top
                self.velocity[1] *= -1
            if abs(self.rect.right - rect.left) < 10 and self.velocity[0]> 0:
                self.velocity[0] *= -1
            if abs(self.rect.left - rect.right) < 10 and self.velocity[0] < 0:
                self.velocity[0] *= -1
            
    
    def check_brick_collision(self, bricks):
        # Checking if the ball hit any of the bricks
        t = pygame.sprite.spritecollide(self, bricks, True)
        if t:
            pygame.mixer.Sound.play(score_sound)
            brick= t[0]
            br_rect = brick.rect

            if abs(self.rect.right - br_rect.left) < 10 and self.velocity[0]> 0:
                self.velocity[0] *= -1
            if abs(self.rect.left - br_rect.right) < 10 and self.velocity[0] < 0:
                self.velocity[0] *= -1
            if abs(self.rect.top - br_rect.bottom) < 10 and self.velocity[1] < 0:
                self.rect.top = br_rect.bottom
                self.velocity[1] *= -1
            if abs(self.rect.bottom - br_rect.top) < 10 and self.velocity[1]> 0:
                self.rect.bottom = br_rect.top
                self.velocity[1] *= -1
    
            if len(bricks) <= config.NSPRITES//2:
                self.velocity = list(map(lambda x: BALL_SPEEDS[1]*sgn(x), self.velocity))
            config.SCORE += len(t)
    
    def reset_position(self):
        self.rect.centerx, self.rect.centery = self.init_p

    def reset_ball(self):
        self.velocity = [BALL_SPEEDS[0]*choice((1, -1)), -BALL_SPEEDS[0]]