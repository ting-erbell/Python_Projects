"""
File: jmps_and_hlts.py
Author: Ting Hong
Date: 11/4/2021
Section: 61
E-mail: t64@umbc.edu
Description: This file simulates chutes and ladders with a modification in which scores can be 
accounted for through types of spaces that the player lands on.
"""

import random

GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6


def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(['nop', f'add {random_points}', f'sub {random_points}', f'mul {random_points}', f'jmp {random_position}', 'hlt'], weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)

    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 1 + r][column_start + 1 + k] = c


def roll_dice():
    """
        Call this function once per turn.
        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)


def math_commands(command, x, score):
    """
    Updates the current score.
    :param command: determines how the score will change from the type of space landed on
    :param x: the integer after the command that will be adjusted accordingly to the command
    :param score: the new score
    :return: the new score
    """

    x = int(x) #converting the x value into an integer
    if (command == "nop"):
        return score #returns the score without any change
    elif (command == "add"):
        score += x
        return score
    elif (command == "sub"):
        score -= x
        return score
    elif (command == "mul"):
        score *= x
        return score
    elif (command == "jump"):
        return score #returns the score without any change

    
def jump_command(jump_position, board_size):
    """
    Updates the position to where the jump command says to go.
    :param jump_position: the new position
    :board_size: size of the board
    :return: the new position where jump command says to go
    """

    position = int(jump_position) % board_size #jumping to where the "jump" position is on the board
    return position
    

def display_grid(game_map, the_grid):
    """
    Displays the completed board grid.
    :param map: the generated map based on the inputted seed and board size
    :the_grid: the grid modified after fill_grid_square
    """
    
    for i in range(len(game_map)): #loop to fill every square on the board
        fill_grid_square(the_grid, len(game_map), i, str(i) + "\n" + game_map[i])
        
    for i in range(len(the_grid)): #loop to join the star items in the list
        print("".join(the_grid[i]))

        
def play_game(game_map):
    """
    Plays the game based on modified spaces that can contribute to final score or move current position.
    :param map: the generated map based on the inputted seed and board size
    :return: replay the game if user chooses to continue
    """
    
    display_grid(game_map, make_grid(len(game_map)))

    position = 0 #initial position of the player
    score = 0 #initial score of the player
    dice_value = 0 #initial value of the dice to call later during a turn
    
    while game_map[position] != "hlt":
        instruction = game_map[position]
        not_jump_instruction = True #boolean flag for non jump command conditions to call roll_dice() later

        if ("add" in instruction) or ("sub" in instruction) or ("mul" in instruction):
            instruction = game_map[position].split()
            command = instruction[0]
            x = instruction[1]
            score = math_commands(command, x, score)

        elif ("jmp" in instruction):
            instruction = game_map[position].split()
            jump_position = instruction[1] #redefining the x integer as the jump_position
            position = jump_command(jump_position, len(game_map))

            print("Pos: " + str(position) + " " + "Score: " + str(score) + ", instruction" +
                  " " + str(game_map[position]) + " " + "Rolled: " + str(dice_value))

        if not_jump_instruction:
            dice_value = roll_dice() #calling the roll_dice() function when command is not jump
            position += dice_value #adding the number of steps to take to the current position
            position %= len(game_map) #circling the board when dice roll is greater than len(game_map)

            print("Pos: " + str(position) + " " + "Score: " + str(score) + ", instruction" +
                  " " + str(game_map[position]) + " " + "Rolled: " + str(dice_value))
            
    print("Final Pos: " + str(position) + " " + "Final Score: " + str(score) + ", Instruction hlt")

    choice = input("continue? ")

    while choice == "y" or choice == "yes":
        return replay(choice)

    
def replay(choice):
    """
    Continues the game if choice is "yes."
    :param choice: the user's inputted answer
    :return: starting the game again if choice is "yes"
    """

    while choice == "y" or choice == "yes": #when the player's choice is "yes", the function continues
        num = input("Board Size and Seed: ").split() #splitting the board size and seed
        board_size = int(num[0])
        the_seed = int(num[1])

        game_map = generate_random_map(board_size, the_seed)
        play_game(game_map)
        return play_game #replaying the game


if __name__ == '__main__':
    num = input("Board Size and Seed: ").split()

    board_size = int(num[0])
    the_seed = int(num[1])

    game_map = generate_random_map(board_size, the_seed)
    play_game(game_map) 

