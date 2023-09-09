import pygame
import pygame.mixer

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    K_SPACE
)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption('BrickBreaker')  # title
pygame.mixer.music.load("bg_music.mp3")

import config
from sprites import Brick, Player, Ball
import util

clock = pygame.time.Clock()
font1 = pygame.font.SysFont('firacode.ttf', 32)
font2 = pygame.font.SysFont('firacode.ttf', 42)

text1 = font1.render('press <space> to start ...', True, (255,161,153))
text3 = font2.render(f'Max Score {config.SCORE} Achieved!!!', True, (131, 183, 153))

# Set up the drawing window
screen = pygame.display.set_mode([config.SCREEN_WIDTH, config.SCREEN_HEIGHT])

all_sprites = pygame.sprite.Group()
brick_sprites = pygame.sprite.Group()

player = Player(config.SCREEN_WIDTH//2, config.PY_Y_LOC, config.PAD_X, config.SCREEN_WIDTH-config.PAD_X)

ball = Ball(config.SCREEN_WIDTH//2, config.PY_Y_LOC - 50,
            (config.PAD_X, config.PAD_Y, config.SCREEN_WIDTH-config.PAD_X, config.SCREEN_HEIGHT))

all_sprites.add(player)
all_sprites.add(ball)

# Run until the user asks to quit
running = True
paused = True

# Timer conditions
timer =  False
timer_s = clock.get_time()

pygame.mixer.music.play(-1)

while running:

    # CHkeing events
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

            if paused:
                # For unpause event
                if event.key == K_SPACE:
                    paused = False
                    config.SCORE = 0

                    # Clearing bricks
                    for brick in brick_sprites:
                        brick.kill()
                    brick_sprites.empty()

                    # generating new brick set
                    for x in util.generate_cls(config.SCREEN_WIDTH-config.PAD_X*2, config.BRICK_W, config.PAD_X):
                        for y in util.generate_cls(config.BRICKS_PANE, config.BRICK_H, config.PAD_Y):
                            b = Brick(x, y)
                            brick_sprites.add(b)
                            all_sprites.add(b)
                    config.NSPRITES = len(brick_sprites)

                    # For starting timer
                    timer = True
                    ball.reset_position()
                    timer_s = pygame.time.get_ticks()

        
        # For window close
        if event.type == pygame.QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    if ball.update():
        paused = True

    ball.check_brick_collision(brick_sprites)
    ball.check_paddle_collision(player.rect)

    # Fill the background with black
    screen.fill((39, 35, 36))

    # Rendering all sprites 
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # Score message
    if config.NSPRITES == config.SCORE != 0:
        paused = True
        text2 = text3
    else:
        text2 = font2.render(f'Score: {config.SCORE:0<}', True, (232,99,117))
    
    # Coditional code if timer is going on
    if timer:
        t = pygame.time.get_ticks() - timer_s
        if t <= 1000:
            text2 = font2.render('3', True, (232,99,117))
        elif t <= 2000:
            text2 = font2.render('2', True, (232,99,117))
        elif t <= 3000:
            text2 = font2.render('1', True, (232,99,117))
        else:
            timer = False
            ball.reset_ball()
    else:
        # Paused game text
        if paused:
            screen.blit(text1, text1.get_rect(center=(500, 500)))

    screen.blit(text2, text2.get_rect(center=(500, 460)))


    # Flip the display
    pygame.display.flip()
    clock.tick(120)

# Done! Time to quit.
pygame.quit()