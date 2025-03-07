import pygame
import random

# Inicialización de pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
FPS = 10

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Dirección inicial
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Extremo")

# Función para generar una posición aleatoria

def random_position():
    return (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

# Clase Snake
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * CELL_SIZE, head_y + self.direction[1] * CELL_SIZE)
        
        if new_head in self.body or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
        
        return True
    
    def grow(self):
        self.growing = True
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

# Clase Obstáculo
class Obstacle:
    def __init__(self):
        self.position = random_position()
    
    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))

# Función principal
def game_loop():
    clock = pygame.time.Clock()
    snake = Snake()
    apple = random_position()
    obstacles = []
    score = 0
    speed = FPS
    running = True
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
        
        if not snake.move():
            running = False
            continue
        
        if snake.body[0] == apple:
            snake.grow()
            apple = random_position()
            score += 1
            speed += 0.5
            if score % 3 == 0:  # Añadir obstáculos cada 3 puntos
                obstacles.append(Obstacle())
        
        for obstacle in obstacles:
            if snake.body[0] == obstacle.position:
                running = False
                break
            obstacle.draw()
        
        pygame.draw.rect(screen, BLUE, (*apple, CELL_SIZE, CELL_SIZE))
        snake.draw()
        
        pygame.display.flip()
        clock.tick(speed)
    
    print(f"Game Over! Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    game_loop()
