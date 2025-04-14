import pygame as pg
import numpy as np
import math

pg.init()
win = pg.display.set_mode((600, 600))
pg.display.set_caption("Zad1")

# kolory
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
purple = (128, 0, 128)
light_blue = (0, 255, 255)
orange = (255, 165, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
empty = (0, 0, 0, 0)

x = 300
y = 300

RADIUS = 150
NUM_SIDES = 10
CENTER = (RADIUS, RADIUS)  # Center for the polygon surface

# Function to get polygon points
def get_polygon_points(center, radius, sides):
    cx, cy = center
    points = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides - math.pi / 2  # Start from the top
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

# Create polygon surface
size = RADIUS * 2
polygon_surface = pg.Surface((size, size), pg.SRCALPHA)
points = get_polygon_points(CENTER, RADIUS, NUM_SIDES)
pg.draw.polygon(polygon_surface, red, points)
polygon_rect = polygon_surface.get_rect(center=(100, 100))

# Function to create a polygon surface
def create_polygon(size, radius, sides):
    surface = pg.Surface((size, size), pg.SRCALPHA)
    center = (size // 2, size // 2)
    points = get_polygon_points(center, radius, sides)
    pg.draw.polygon(surface, red, points)
    return surface

# Function to Shear Surface
def shear_surface(surface, shear_x=0, shear_y=0):
    width, height = surface.get_size()
    array = pg.surfarray.pixels3d(surface)  # Access the surface pixels
    new_array = np.zeros((height + shear_y, width + shear_x, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Apply shear transformation
            new_x = x + int(shear_x * (y / height))  # Horizontal shear
            new_y = y + int(shear_y * (x / width))  # Vertical shear
            if 0 <= new_x < width + shear_x and 0 <= new_y < height + shear_y:
                new_array[new_y, new_x] = array[y, x]

    # Create new sheared surface
    sheared_surface = pg.surfarray.make_surface(new_array)
    return sheared_surface

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        # change on button press
        if event.type == pg.KEYDOWN:
            # reset button
            win.fill(black)
            x = 300
            y = 300
            if event.key == pg.K_r:
                polygon_surface = pg.Surface((size, size), pg.SRCALPHA)
                points = get_polygon_points(CENTER, RADIUS, NUM_SIDES)
                pg.draw.polygon(polygon_surface, red, points)

            # scale down x2
            if event.key == pg.K_1:
                nsize = size / 2
                win.fill(black)
                polygon_surface = pg.transform.scale(polygon_surface, (nsize, nsize))

            # rotate
            if event.key == pg.K_2:
                win.fill(black)
                #pg.draw.rect(polygon_surface, yellow, (75, 75, 150, 150))
                polygon_surface = pg.transform.rotate(polygon_surface, 45)

            # flip and stretch
            if event.key == pg.K_3:
                win.fill(black)
                polygon_surface = pg.transform.rotate(polygon_surface, 90)
                polygon_surface = pg.transform.scale(polygon_surface, (size, size*1.5))

            # skew
            if event.key == pg.K_4:
                win.fill(black)
                polygon_surface = create_polygon(size, RADIUS, NUM_SIDES)
                sheared_surface = shear_surface(polygon_surface, shear_x=30)
                polygon_surface = sheared_surface

            # move to the top and stretch
            if event.key == pg.K_5:
                win.fill(black)
                polygon_surface = pg.transform.scale(polygon_surface, (size, size / 2))
                y -= 225

            # skew and rotate
            if event.key == pg.K_6:
                win.fill(black)
                polygon_surface = create_polygon(size, RADIUS, NUM_SIDES)
                sheared_surface = shear_surface(polygon_surface, shear_y=30)
                polygon_surface = sheared_surface
                polygon_surface = pg.transform.rotate(polygon_surface, 90)
                polygon_surface = pg.transform.scale(polygon_surface, (size, size * 1.5))

            # flip and stretch
            if event.key == pg.K_7:
                win.fill(black)
                #pg.draw.polygon(polygon_surface, yellow, ((150, 200), (250, 250), (50, 250)))
                polygon_surface = pg.transform.rotate(polygon_surface, 180)
                polygon_surface = pg.transform.scale(polygon_surface, (size / 3, size / 2))

            # move, stretch and rotate
            if event.key == pg.K_8:
                win.fill(black)
                polygon_surface = pg.transform.scale(polygon_surface, (size/2, size))
                polygon_surface = pg.transform.rotate(polygon_surface, 60)
                x -= 50
                y += 150

            # skew, move and flip
            if event.key == pg.K_9:
                win.fill(black)
                polygon_surface = create_polygon(size, RADIUS, NUM_SIDES)
                sheared_surface = shear_surface(polygon_surface, shear_x=50)
                polygon_surface = sheared_surface
                polygon_surface = pg.transform.rotate(polygon_surface, 90)
                x += 150

            # ex 2
            if event.key == pg.K_0:
                win.fill(white)
                pg.draw.rect(win, white, (1, 1, 600, 600))
                pg.draw.rect(win, green, (200, 200, 200, 200))
                pg.draw.polygon(win, white, ((400, 400), (200, 400), (300, 300)))

    rect = polygon_surface.get_rect(center=(x, y))
    win.blit(polygon_surface, rect.topleft)
    pg.display.update()

pg.quit()