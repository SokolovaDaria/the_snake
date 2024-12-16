import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BLOCK_COLOR = (100, 100, 100)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def randomize_position(self, exclude_positions=[]):
        """Устанавливает случайную позицию объекта на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in exclude_positions:
                self.position = new_position
                break

    def draw(self, display):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(display, self.body_color, rect)


class Apple(GameObject):
    """Класс для объекта 'Яблоко'."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.randomize_position()


class Snake(GameObject):
    """Класс для объекта 'Змейка'."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку в направлении движения."""
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        self.length += 1

    def draw(self, display):
        """Отрисовывает змейку"""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(display, self.body_color, rect)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(display, self.body_color, head_rect)

    def get_head_position(self):
        """Возвращает позицию головы"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки в исходное."""
        self.randomize_position()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


class Block(GameObject):
    """Класс для блоков-препятствий."""

    def __init__(self, body_color=BLOCK_COLOR):
        super().__init__(body_color=body_color)


def generate_blocks(num_blocks, snake_positions, apple_position):
    """
    Генерирует заданное количество блоков, исключая позиции змейки и яблока.

    :param num_blocks: количество блоков
    :param snake_positions: позиции сегментов змейки
    :param apple_position: позиция яблока
    :return: список объектов Block
    """
    blocks = []
    exclude_positions = snake_positions + [apple_position]
    for _ in range(num_blocks):
        block = Block()
        block.randomize_position(exclude_positions)
        blocks.append(block)
        exclude_positions.append(block.position)
    return blocks


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    blocks = generate_blocks(randint(1, 5), snake.positions, apple.position)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            blocks = generate_blocks(randint(1, 5),
                                     snake.positions, apple.position)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            blocks = generate_blocks(randint(1, 5),
                                     snake.positions, apple.position)

        for block in blocks:
            if snake.get_head_position() == block.position:
                pygame.quit()
                raise SystemExit("Змея столкнулась с блоком. Игра окончена!")

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        for block in blocks:
            block.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
