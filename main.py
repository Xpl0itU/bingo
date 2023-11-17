import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (600, 600)
CELL_SIZE = 200
NUM_ROWS = 3
NUM_COLS = 3
BG_COLOR = (255, 255, 255)
NORMAL_COLOR = (255, 255, 255)
SELECTED_COLOR = (255, 0, 0)  # Red
OUTLINE_COLOR = (0, 0, 0)  # Black outline
FONT_SIZE = 24
FONT_COLOR = (0, 0, 0)


# Function to read words from a file
def read_words_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


# Function to create a random bingo card
def create_bingo_card(word_list):
    card = random.sample(word_list, NUM_ROWS * NUM_COLS)
    return [card[i : i + NUM_COLS] for i in range(0, len(card), NUM_COLS)]


# Initialize Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Bingo Game")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Read words from a file
file_path = "patricia.txt"  # Replace with your file path
word_list = read_words_from_file(file_path)

# Check if there are enough words for the bingo card
if len(word_list) < NUM_ROWS * NUM_COLS:
    print("Error: Not enough words for the bingo card.")
    pygame.quit()
    sys.exit()

# Create a random bingo card
bingo_card = create_bingo_card(word_list.copy())

# Keep track of selected cells
selected_cells = set()

clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked_column = x // CELL_SIZE
            clicked_row = y // CELL_SIZE

            # Toggle cell selection
            if 0 <= clicked_row < NUM_ROWS and 0 <= clicked_column < NUM_COLS:
                cell = (clicked_row, clicked_column)
                if cell in selected_cells:
                    selected_cells.remove(cell)
                else:
                    selected_cells.add(cell)

    # Draw the bingo card
    screen.fill(BG_COLOR)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            cell_color = (
                SELECTED_COLOR if (row, col) in selected_cells else NORMAL_COLOR
            )
            pygame.draw.rect(
                screen,
                cell_color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                screen,
                OUTLINE_COLOR,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                2,
            )
            word = bingo_card[row][col]
            text = font.render(word, True, FONT_COLOR)
            text_rect = text.get_rect(
                center=(
                    col * CELL_SIZE + CELL_SIZE // 2,
                    row * CELL_SIZE + CELL_SIZE // 2,
                )
            )
            screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(5)
