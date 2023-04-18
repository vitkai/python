import random
import curses

# Set up the curses environment
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Define the map layout
map_size = (25, 25)
map_layout = [['.' for _ in range(map_size[0])] for _ in range(map_size[1])]

# Place the player on the map
player_x = random.randint(0, map_size[0] - 1)
player_y = random.randint(0, map_size[1] - 1)
map_layout[player_y][player_x] = '@'

# Print the map
def print_map():
    for row in map_layout:
        stdscr.addstr(' '.join(row) + '\n')
    stdscr.move(player_y, player_x * 2)

# Move the player
def move_player(x_offset, y_offset):
    global player_x, player_y
    if 0 <= player_x + x_offset < map_size[0] and 0 <= player_y + y_offset < map_size[1]:
        map_layout[player_y][player_x] = '.'
        player_x += x_offset
        player_y += y_offset
        map_layout[player_y][player_x] = '@'

while True:
    stdscr.clear()
    print_map()
    stdscr.refresh()
    key = stdscr.getch()
    if key == curses.KEY_UP:
        move_player(0, -1)
    elif key == curses.KEY_DOWN:
        move_player(0, 1)
    elif key == curses.KEY_LEFT:
        move_player(-1, 0)
    elif key == curses.KEY_RIGHT:
        move_player(1, 0)
    elif key == ord('q'):
        break

# Clean up the curses environment
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
