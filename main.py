import pygame
import itertools
import random
import math
import time

from perlin_noise import PerlinNoise, Interp


def draw_mark(surface, color, coord):
    pygame.draw.circle(surface, color, coord, 3)


def get_interp_name(interp):
    if interp is Interp.LINEAR:
        return 'Linear'
    elif interp is Interp.COSINE:
        return 'Cosine'
    else:
        return 'Cubic'


random.seed(time.time())

# define constants
WIDTH, HEIGHT = (1200, 600)
FONT_SIZE = 14
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('1D Perlin Noise') 
font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

# set initial parametrs for program
seed = random.randint(0, 2**32)
amplitude = 50
frequency = 1
octaves = 1
# number of integer values on screen
# (implicit frequency)
segments = 40
interpolation = Interp.COSINE
interp_iter = itertools.cycle((Interp.LINEAR, Interp.CUBIC, Interp.COSINE))
offset = 0
offset_speed = 2
show_marks = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                amplitude += 5
            elif event.key == pygame.K_z:
                amplitude -= 5
            elif event.key == pygame.K_f:
                frequency += 1
            elif event.key == pygame.K_v:
                frequency -= 1
            elif event.key == pygame.K_o:
                octaves += 1
            elif event.key == pygame.K_l:
                octaves -= 1
            elif event.key == pygame.K_RIGHT:
                offset_speed += 2
            elif event.key == pygame.K_LEFT:
                offset_speed -= 2
            elif event.key == pygame.K_UP:
                segments += 10
            elif event.key == pygame.K_DOWN:
                segments -= 10
            elif event.key == pygame.K_i:
                interpolation = next(interp_iter)
            elif event.key == pygame.K_s:
                seed = random.randint(0, 2**32)
            elif event.key == pygame.K_m:
                show_marks = False if show_marks else True

    # create PerlinNoise object
    noise = PerlinNoise(seed, amplitude, frequency, octaves, interpolation)

    screen.fill(WHITE)

    # print information about program parametrs
    text_surfaces = {
        (5, FONT_SIZE * 0): 
            font.render('(A/Z) Amplitude: ' + str(amplitude), True, BLACK),
        (5, FONT_SIZE * 1): 
            font.render('(F/V) Frequency: ' + str(frequency), True, BLACK),
        (5, FONT_SIZE * 2): 
            font.render('(O/L) Octaves: ' + str(octaves), True, BLACK),
        (5, HEIGHT - FONT_SIZE * 1): 
            font.render('(LEFT/RIGHT) Speed: ' + str(offset_speed), True, BLACK),
        (5, HEIGHT - FONT_SIZE * 2): 
            font.render('(UP/DOWN) Segments: ' + str(segments), True, BLACK),
        (5, HEIGHT - FONT_SIZE * 3): 
            font.render('(M) Marks: ' + str(show_marks), True, BLACK),
        }
    for dest, text_surface in text_surfaces.items():
        screen.blit(text_surface, dest=dest)

    # and two another parametrs on the right side of the screen
    interp_inform = '(I) Interpolation: ' + get_interp_name(noise.interp)
    text_surface = font.render(interp_inform, True, BLACK)
    screen.blit(text_surface, dest=(WIDTH - text_surface.get_width() - 5, 0))
    seed_inform = '(S) Seed: ' + str(seed)
    text_surface = font.render(seed_inform, True, BLACK)
    screen.blit(text_surface, dest=(WIDTH - text_surface.get_width() - 5, HEIGHT - FONT_SIZE))


    points = list()
    norma = WIDTH / segments
    for pix_x in range(WIDTH):
        # convert pixel position to real value
        x = (pix_x + offset) / norma
        # get perlin noise
        y = noise.get(x)

        # convert perlin noise to pixel height value
        pix_y = HEIGHT / 2 + y

        # check is x value integer in Perlin noise coordinates
        real_x = x * noise.frequency
        if show_marks and math.isclose(real_x, int(real_x), rel_tol=0.001):
            draw_mark(screen, RED, (pix_x, pix_y))

        points.append((pix_x, pix_y))

    # draw lines and update display
    pygame.draw.lines(screen, BLACK, False, points)
    pygame.display.flip()

    # move Perlin noise
    offset += offset_speed

pygame.quit()