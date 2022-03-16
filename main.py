import math
import os
from curses import *


def main():
    # Variables
    data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    seperator = "\n───┼───┼───\n"
    is_first_players_turn = True
    turn = 0
    game_running = True

    # Initialize curses
    screen = initscr()
    noecho()
    cbreak()
    start_color()
    curs_set(2)
    screen.keypad(True)

    # Color pairs
    init_pair(1, COLOR_CYAN, COLOR_BLACK)
    init_pair(2, COLOR_BLUE, COLOR_BLACK)
    init_pair(3, COLOR_RED, COLOR_BLACK)

    # Create window
    # TODO: center window
    # TODO: move things to seperate window
    window = newwin(20, 50, 0, 0)

    # Display the gird and stuff
    # Columns inverted to emulate what a numpad looks like
    print_block(window, data[::-1], seperator)

    # Main loop
    while game_running:
        # Check for the winner
        if turn >= 3:
            winner = check_for_winner(data)
            if winner:
                window.refresh()
                window.addstr(
                    8,
                    0,
                    f"the winner is {current_turn_symbol}! press Q to quit!!",
                    A_BOLD | color_pair(2 + is_first_players_turn),
                )
                break
            elif turn >= 9:
                # TODO: find a solutin or a better workaround
                window.refresh()
                window.addstr(8, 0, f"No one wins. press Q to quit.   ", A_BOLD)
                break

        # Ask the current turn's player to choose a number
        current_turn_symbol = "x" if is_first_players_turn else "o"
        window.refresh()
        window.addstr(
            8,
            0,
            f"It's {current_turn_symbol}'s turn - choose a number.",
            A_BOLD | color_pair(2 + is_first_players_turn),
        )

        # The input function
        window.refresh()
        chosen_coordinates = ask_for_input(window, data)

        # Quit game if q is pressed
        # ? a better way to do this
        if chosen_coordinates is None:
            game_running = False
            break

        # Modify data based on input
        data[chosen_coordinates[0]][chosen_coordinates[1]] = current_turn_symbol
        window.addstr(
            ((chosen_coordinates[0] + 1) * 2) - 1 + 1,
            ((chosen_coordinates[1] + 1) * 4) - 3,
            current_turn_symbol,
            A_BOLD | color_pair(2 + is_first_players_turn),
        )

        # Variables that change with turns
        # TODO: make is_first_players_turn based on turn
        is_first_players_turn = not is_first_players_turn
        turn = turn + 1

    # ? find a better solution than this
    while game_running:
        user_input = chr(window.getch())
        if user_input == "q":
            quit_game()
            break


def print_block(window, data, seperator):
    rows = []
    for row in data:
        rows.append(" " + " │ ".join(row) + " ")

    block = "\n" + seperator.join(rows)

    window.refresh()
    window.addstr(0, 0, "Tic tac toe!", A_BOLD | A_UNDERLINE | color_pair(1))
    window.addstr(0, 13, "press Q to quit.", color_pair(0))
    window.addstr(1, 0, block)


def ask_for_input(window, data):
    if not "user_input" in locals():
        user_input = ""

    while True:
        user_input = chr(window.getch())
        if user_input == "q":
            return None

        window.refresh()
        window.addstr(9, 0, f"Last detected input: {user_input} ")

        # Check if input is valid
        try:
            chosen_number = int(user_input)
        except ValueError:
            window.refresh()
            # TODO: again, find a solutin to this
            window.addstr(10, 0, "You have to press a number.     ")
        except:
            window.refresh()
            window.addstr(10, 0, "Something went wrong and i dont know what it is.")
        else:
            if not 1 <= chosen_number <= 9:
                window.refresh()
                window.addstr(10, 0, "Choose a number between 1 and 9.")
            else:
                # Convert number to coordinates
                # Columns inverted to emulate what a numpad looks like
                chosen_number = chosen_number - 1
                coordinates = [0, 0]
                coordinates[0] = 2 - math.floor(chosen_number / 3)
                coordinates[1] = chosen_number % 3
                # check if coordinate is occupied
                if (
                    data[coordinates[0]][coordinates[1]] == "o"
                    or data[coordinates[0]][coordinates[1]] == "x"
                ):
                    window.refresh()
                    window.addstr(10, 0, "Number already chosen.              ")
                else:
                    break

    return coordinates


def check_for_winner(data):
    # Checks if a column or diagonal line is identical
    if check_for_winner_vertically(data):
        return True

    # Then flip it and do it again
    if check_for_winner_vertically(list(zip(*reversed(data)))):
        return True

    # Returns False if there's no winner
    return False


def check_for_winner_vertically(data):
    for column in data:
        if column[0] == column[1] == column[2]:
            return True

    if data[0][0] == data[1][1] == data[2][2]:
        return True


def quit_game():
    echo()
    nocbreak()
    endwin()


if __name__ == "__main__":
    main()
