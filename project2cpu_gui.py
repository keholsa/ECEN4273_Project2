import pygame
import sys
import random
import numpy as np


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
GRID_SIZE = 13
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Create a grid with a fence and an exit
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Create a fence around the perimeter
for i in range(GRID_SIZE):
    grid[i][0] = 1  # Left side
    grid[i][GRID_SIZE - 1] = 1  # Right side
    grid[0][i] = 1  # Top side
    grid[GRID_SIZE - 1][i] = 1  # Bottom side

# Place the exit randomly on the fence
exit_position = (random.randint(1, GRID_SIZE - 2), random.choice([0, GRID_SIZE - 1]))
grid[exit_position[0]][exit_position[1]] = 2  # Exit sets the exit grid to the value of 2

# Goat class
class Goat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collisionCount = 0
        self.direction = self.available_directions()
        self.exit = False
        grid[self.x][self.y] = 3

    def move_towards_exit(self):
        # Attempt to move towards the exit
        self.is_next_to_exit()
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        # Check for collisions with other Goat and the fence
        if not self.exit:
            if (
                1 <= new_x < GRID_SIZE - 1
                and 1 <= new_y < GRID_SIZE - 1
                and grid[new_x][new_y] != 3  # Check for collision with the Goat
                and grid[new_x][new_y] != 1  # Check for collision with the fence
            ):
                grid[self.x][self.y] = 0
                self.x = new_x
                self.y = new_y
                grid[self.x][self.y] = 3
            else: self.collisionCount += 1

            if self.collisionCount > 1: #there was a collision so it needs to check the rest of it's available directions
                self.direction = self.available_directions()
                self.collisionCount = 0
        else: #Get rid of goat out of grid because it exited
            grid[self.x][self.y] = 0
            self.x = new_x
            self.y = new_y


    def available_directions(self):
        # Check for collisions with other Goat and the fence
        available_directions = []
        check_directions = [[1,0], [-1,0], [0,1], [0,-1]]
        for i in range(4):
            new_x = self.x + check_directions[i][0]
            new_y = self.y + check_directions[i][1]
            if (
                grid[new_x][new_y] != 3  # Check for collision with the Goat
                and grid[new_x][new_y] != 1  # Check for collision with the fence
            ):
                available_directions.append(check_directions[i])

        # Return [0,0] if there are no available directions
        if available_directions == []:
           return [0,0]
        # Select a random direction from the available directions
        else:
           switch = random.randint(0, len(available_directions)-1)
           return available_directions[switch]

    def is_next_to_exit(self):
        # Check if the Goat is adjacent to the exit
        exit_next = ((abs(self.x - exit_position[1]) == 1 and self.y == exit_position[0]) or
                    (self.x == exit_position[1] and abs(self.y - exit_position[0]) == 1))

        if exit_next:
            x_direction = exit_position[1] - self.x
            y_direction = exit_position[0] - self.y
            self.direction = [x_direction, y_direction]
            self.exit = True
        return exit_next

    def is_on_exit(self):
        # Check if the Goat is on the exit
        return (self.x == exit_position[1] and self.y == exit_position[0])

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Create a list of Goat
num_Goat = 61
Goat_list = [Goat(random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)) for _ in range(num_Goat)]


# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goat Simulation")
iteration = 0
done = False

# Main loop
clock = pygame.time.Clock()
while done == False:
    iteration += 1

    # Pygame event handling (Press Esc to exit)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Move Goat towards the exit and check if they are next to it
    for Goat in Goat_list:
        Goat.move_towards_exit()
        if Goat.is_on_exit():
            Goat_list.remove(Goat)

    # Pygame drawing
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, BROWN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 2:
                pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw Goat
    for Goat in Goat_list:
        Goat.draw(screen)

    # Check if all Goat have exited
    if len(Goat_list) == 0:
        print("Done in %d iterations" % iteration)
        done = True

    pygame.display.flip()
    clock.tick(50)  # Adjust the speed of the simulation
