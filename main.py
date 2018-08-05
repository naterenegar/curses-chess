import piece, board, player, curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr(int((curses.LINES-1)/2), int((curses.COLS-1)/2), "Welcome to pychess!")    

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
#name1 = input("Please enter Player 1's name: ")
#name2 = input("Please enter Player 2's name: ")


#game = board.board(name1, name2, startGame=True)
#print(str(game.atPos((0, 6))))
