
import turtle
import random
import numpy as np

# Constants
GRID_SIZE = 7
NUM_TREASURES = 5
NUM_TRAPS = 3
MAX_TURNS = 50
CELL_SIZE = 50
ACTION_SPACE = [0, 1, 2, 3]  # Up, Down, Left, Right


# Initialize grid with treasures (+10), traps (-5), and neutral tiles (0)
def initialize_grid(grid_size, num_treasures, num_traps):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Place treasures
    for _ in range(num_treasures):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        while grid[x][y] != 0:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        grid[x][y] = 10  # Treasure

    # Place traps
    for _ in range(num_traps):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        while grid[x][y] != 0:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        grid[x][y] = -5  # Trap

    return grid


# Player class
class Player:
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.score = 0
        self.color = color
        self.treasures_found = 0
        self.traps_crossed = 0
        self.path = [position]  # Track the player's path

    def move(self, action):
        x, y = self.position
        if action == 0:  # Move up
            x = max(0, x - 1)
        elif action == 1:  # Move down
            x = min(GRID_SIZE - 1, x + 1)
        elif action == 2:  # Move left
            y = max(0, y - 1)
        elif action == 3:  # Move right
            y = min(GRID_SIZE - 1, y + 1)
        self.position = (x, y)
        self.path.append(self.position)  # Add the new position to the path

    def update_score(self, grid):
        x, y = self.position
        if grid[x][y] == 10:  # Treasure
            self.score += 10
            self.treasures_found += 1
        elif grid[x][y] == -5:  # Trap
            self.score -= 5
            self.traps_crossed += 1


# Function to draw the grid using turtle graphics
def draw_grid(grid):
    turtle.penup()
    turtle.goto(-GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2)

    # Draw grid with treasures and traps
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            turtle.goto(-GRID_SIZE * CELL_SIZE / 2 + j * CELL_SIZE, GRID_SIZE * CELL_SIZE / 2 - i * CELL_SIZE)
            turtle.pendown()
            turtle.begin_fill()
            if grid[i][j] == 10:
                turtle.fillcolor("yellow")  # Treasure
            elif grid[i][j] == -5:
                turtle.fillcolor("black")  # Trap
            else:
                turtle.fillcolor("white")  # Empty space
            for _ in range(4):
                turtle.forward(CELL_SIZE)
                turtle.right(90)
            turtle.end_fill()
            turtle.penup()


# Function to update the turtle display with players' movements and paths
def update_display(grid, player1, player2):
    # Redraw the grid and player positions without clearing the entire screen
    draw_grid(grid)

    # Draw Player 1's path (blue)
    turtle.penup()
    turtle.color("blue")
    for pos in player1.path:
        turtle.goto(-GRID_SIZE * CELL_SIZE / 2 + pos[1] * CELL_SIZE + CELL_SIZE / 2,
                    GRID_SIZE * CELL_SIZE / 2 - pos[0] * CELL_SIZE - CELL_SIZE / 2)
        turtle.pendown()
        turtle.dot(10, "blue")
        turtle.penup()

    # Draw Player 2's path (red)
    turtle.penup()
    turtle.color("red")
    for pos in player2.path:
        turtle.goto(-GRID_SIZE * CELL_SIZE / 2 + pos[1] * CELL_SIZE + CELL_SIZE / 2,
                    GRID_SIZE * CELL_SIZE / 2 - pos[0] * CELL_SIZE - CELL_SIZE / 2)
        turtle.pendown()
        turtle.dot(10, "red")
        turtle.penup()

    turtle.update()


# Function to display the winner and scores on the Turtle screen
def display_winner_turtle(player1, player2):
    if player1.score > player2.score:
        winner = player1
    elif player1.score < player2.score:
        winner = player2
    else:
        winner = None

    # Display result on the Turtle screen
    turtle.penup()
    turtle.goto(0, -GRID_SIZE * CELL_SIZE / 2 - 20)
    turtle.color("black")
    if winner:
        message = f"Winner: {winner.name}\nScore: {winner.score}\nTreasures: {winner.treasures_found}\nTraps: {winner.traps_crossed}"
    else:
        message = f"It's a Tie!\nPlayer 1 Score: {player1.score}\nPlayer 2 Score: {player2.score}"

    turtle.write(message, align="center", font=("Arial", 16, "bold"))
    turtle.hideturtle()


# Game loop
def start_game():
    # Initialize grid and players
    grid = initialize_grid(GRID_SIZE, NUM_TREASURES, NUM_TRAPS)
    player1 = Player("Player 1", (0, 0), "blue")
    player2 = Player("Player 2", (GRID_SIZE - 1, GRID_SIZE - 1), "red")

    # Set up turtle
    turtle.speed(0)
    turtle.tracer(0)
    turtle.hideturtle()
    draw_grid(grid)

    # Game loop
    for turn in range(MAX_TURNS):
        for player in [player1, player2]:
            action = random.choice(ACTION_SPACE)  # Random move (replace with strategy as needed)
            player.move(action)
            player.update_score(grid)

        update_display(grid, player1, player2)

    # Final scores and winner display
    display_winner_turtle(player1, player2)
    turtle.done()


# Start the game
start_game()
