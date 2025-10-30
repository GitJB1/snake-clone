import pygame
from enum import Enum
from random import randint

#defining game grid and screen size
ROWS = 20
COLLUMS = 20
TILE_SIZE = 40
SCREEN_WIDTH = TILE_SIZE * COLLUMS
SCREEN_HEIGHT = TILE_SIZE * ROWS
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Clone 2025')

#setting pygame clock
clock = pygame.time.Clock()

#Drawing functions
def draw_snake(display_surface,snake):
    for segment in snake:
        pygame.draw.rect(display_surface, (0, 255, 0), segment.rect)

def draw_fruits(display_surface,fruits):
    for fruit in fruits:
        pygame.draw.rect(display_surface, (255, 0, 0), fruit.rect)

def draw_grid(display_surface):
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(display_surface, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(display_surface, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


#Defining a Tile class
class Tile:
    def __init__(self, coordinates ):
        self.coordinates = coordinates
        self.x, self.y = coordinates
        self.rect = pygame.Rect((self.x * TILE_SIZE,self.y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))

#Snake and it's bahavior
snake = [Tile((COLLUMS/2, ROWS/2))]
snake_head = snake[0]

snake_tick_speed = 100 #in miliseconds
snake_timer = pygame.USEREVENT + 1
pygame.time.set_timer(snake_timer, snake_tick_speed)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0 , 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

snake_direction = Direction.RIGHT

def isOutOfBoundaries(grid_position):
    x, y = grid_position
    return not (0 <= x < COLLUMS and 0 <= y < ROWS)

def isHittingItself(next_move):
    for segment in snake[:-1]:
        if segment.coordinates == next_move:
            return True
    return False

def isFruit(next_move):
    global fruits_on_screen
    for fruit in fruits:
        if next_move == fruit.coordinates:
            fruits.remove(fruit)
            fruits_on_screen -= 1
            return True
    return False

can_change_direction = True
def snakeMovement():
    global can_change_direction
    global snake_head
    next_snake_movement = (snake_head.x + snake_direction.value[0],
                           snake_head.y + snake_direction.value[1])
    if isOutOfBoundaries(next_snake_movement) or isHittingItself(next_snake_movement): gameOver()
    else:
        snake.insert(0, Tile(next_snake_movement))
        snake_head = snake[0]
        can_change_direction = True
        if not isFruit(next_snake_movement): snake.pop()


def changeDirection(new_direction, snake_current_direction):
    if (new_direction, snake_current_direction) not in [(Direction.UP, Direction.DOWN),
                                                (Direction.DOWN, Direction.UP),
                                                (Direction.RIGHT, Direction.LEFT),
                                                (Direction.LEFT, Direction.RIGHT)]:
        return new_direction
    return snake_current_direction

#Fruit and it's behavior
fruits = []
max_fruits_on_screen = 1
fruits_on_screen = 0
def spawnFruit():
    global fruits_on_screen
    while fruits_on_screen < max_fruits_on_screen:
        new_fruit = Tile((randint(0, COLLUMS-1), randint(0, ROWS-1)))

        invalid_position = any(new_fruit.coordinates == fruit.coordinates for fruit in fruits) or \
        any(new_fruit.coordinates == segment.coordinates for segment in snake)

        if invalid_position:
            continue
        
        fruits.append(new_fruit)
        fruits_on_screen += 1

#game over
game_over = False
def gameOver():
    global game_over 
    game_over = True
    pygame.time.set_timer(snake_timer, 0)

#Game Loop
gameloop = True
while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if can_change_direction:
                if event.key == pygame.K_UP:
                    snake_direction = changeDirection(Direction.UP, snake_direction)
                    can_change_direction = False
                elif event.key == pygame.K_DOWN:
                    snake_direction = changeDirection(Direction.DOWN, snake_direction)
                    can_change_direction = False
                elif event.key == pygame.K_RIGHT:
                    snake_direction = changeDirection(Direction.RIGHT, snake_direction)
                    can_change_direction = False
                elif event.key == pygame.K_LEFT:
                    snake_direction = changeDirection(Direction.LEFT, snake_direction)
                    can_change_direction = False
            if event.key == pygame.K_r and game_over:
                game_over = False
                pygame.time.set_timer(snake_timer, snake_tick_speed)
                snake = [Tile((COLLUMS/2, ROWS/2))]
                snake_head = snake[0]
                fruits = []
                fruits_on_screen = 0
        if event.type == snake_timer:
            snakeMovement()
            spawnFruit()

    SCREEN.fill((0, 0, 0))
    draw_grid(SCREEN)
    draw_fruits(SCREEN, fruits)
    draw_snake(SCREEN, snake)

    pygame.display.flip()
    clock.tick(60)