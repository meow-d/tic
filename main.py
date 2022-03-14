import math
import os


def main():
    data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    seperator = "\n ───┼───┼───\n"
    is_first_players_turn = False
    chosen_coordinates = 0

    while True:
        winner = check_for_winner(data, is_first_players_turn)
        if winner:
            print_with_colours(f"the winner is {current_turn_symbol}!", "\u001b[36;1m")
            break

        print_block(data, seperator)

        chosen_coordinates = ask_for_input(data)

        current_turn_symbol = "x" if is_first_players_turn else "o"
        data[chosen_coordinates[0]][chosen_coordinates[1]] = current_turn_symbol

        is_first_players_turn = not is_first_players_turn


def print_block(data, seperator):
    rows = [get_row(data, 0), get_row(data, 1), get_row(data, 2)]
    block = "\n" + seperator.join(rows)

    os.system("cls||clear")
    print_with_colours("tic tac toe!", "\u001b[36;1m")
    print(block)


def get_row(data, row_number):
    return f"  {data[row_number][0]} │ {data[row_number][1]} │ {data[row_number][2]} "


def print_with_colours(text, colour_code, end="\n"):
    print(colour_code + text + "\u001b[0m", end=end)


def ask_for_input(data):
    while True:
        print_with_colours("Select a number: ", "\u001b[36;1m", end="")
        user_input = input()

        # Verify input
        try:
            chosen_number = int(user_input.strip())
        except ValueError:
            print("Please enter a number.")
        except:
            print("Something went wrong and i dont know what it is.")
        else:
            if not 1 <= chosen_number <= 9:
                print("Choose a number between 1 and 9.")
            else:
                # Convert number to coordinates
                chosen_number = chosen_number - 1
                coordinates = [0, 0]
                coordinates[0] = math.floor(chosen_number / 3)
                coordinates[1] = chosen_number % 3
                # check if coordinate is occupied
                if (
                    data[coordinates[0]][coordinates[1]] == "o"
                    or data[coordinates[0]][coordinates[1]] == "a"
                ):
                    print("Number already chosen.")
                else:
                    break

    return coordinates


def check_for_winner(data, is_first_players_turn):
    # TODO check is anyone wins, and if so, return the winner
    # Checks if a row is identical
    if check_for_winner_column(data):
        return True

    # Checks if a column is identical
    if check_for_winner_column(zip(*reversed(data))):
        return True

    # Checks if \ and /
    # Returns None if there's no winner
    return False


def check_for_winner_column(data):
    for column in data:
        if column[0] == column[1] == column[2]:
            return True


if __name__ == "__main__":
    main()
