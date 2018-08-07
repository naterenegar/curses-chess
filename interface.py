import piece, game, player, curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    lines = curses.LINES - 1
    cols = curses.COLS - 1
    
    # Diving the screen into 3 parts

    board = stdscr.subwin(curses.LINES, int(3*(curses.COLS/5)), 0, int(curses.COLS/5) + 1)
    board.border()

    comm = stdscr.subwin(curses.LINES, int(curses.COLS/5), 0, 0)
    comm.border()
    
    info = stdscr.subwin(curses.LINES, int(curses.COLS/5), 0, int((4/5)*curses.COLS) + 1)
    info.border()

    # Passing numbers greater than 8 or so will break this (attempting to draw outside window)
    pos = draw_board(board, board.getmaxyx()[0], board.getmaxyx()[1], 3, 5)
    draw_pieces(board, pos)

    game1 = game.Game("Nate", "Olivia", pos)

    stdscr.refresh()
    stdscr.getkey()
        
    return pos

def draw_board(scr, lines, cols, box_lines, box_cols):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
 
    # Want dimensions to be odd so we can draw piece letter in the exact middle
    if(box_lines % 2 == 0):
        box_lines = box_lines + 1
    if(box_cols % 2 == 0):
        box_cols = box_cols + 1

    # Brush is used for drawing the board, pair will choose the color pair 
    brush = " " * box_cols
    pair = True 

    # The coordinate of each squares center will be stored here and returned
    positions = [None] * 8 
    for i in range(0, 8):
        positions[i] = [None] * 8

    # Mapping the looping variables to chess coordinates
    alph = {4:"A", 3:"B", 2:"C", 1:"D", 0:"E", -1:"F", -2:"E", -3:"F"}
    
    py = 7 
    for i in range(4, -4, -1):
        px = 0 
        pair = not pair
        
        # These draw the coordinates on the sides, using the alph dictonary
        scr.addstr(int(lines/2 - i*box_lines) + int(box_lines/2), int(cols/2 - 5*box_cols), str(i+4), curses.A_BOLD)
        scr.addstr(int(lines/2 - 5*box_lines) + int(box_lines/2), int(cols/2 - i*box_cols) + int(box_cols/2), alph[i], curses.A_BOLD)
    
        # Drawing the actual board using the brush str
        for j in range(4, -4, -1):
            pair = not pair
            
            # Taking note of the center of each box for managing pieces and moves later
            positions[py][px] = (int(lines/2 - i*box_lines) + int(box_lines/2), int(cols/2 - j*box_cols) + int(box_cols/2))
            for k in range(0, box_lines):
                scr.addstr(int(lines/2 - i*box_lines) + k, int(cols/2 - j*box_cols), brush, curses.color_pair(1 if pair else 2))

            px = px + 1
        py = py - 1

    scr.move(0, 0)

    return positions

def draw_pieces(scr, pos):
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    pieces = {0:"R", 1:"k", 2:"B", 3:"K", 4:"Q", 5:"B", 6:"k", 7:"R"}
        
    for i in range(0, 8):
        scr.addstr(pos[0][i][0], pos[0][i][1], pieces[i], curses.color_pair(3))  
        scr.addstr(pos[1][i][0], pos[1][i][1], 'P', curses.color_pair(3))  
        scr.addstr(pos[6][i][0], pos[6][i][1], 'P', curses.color_pair(4))
        scr.addstr(pos[7][i][0], pos[7][i][1], pieces[i], curses.color_pair(4))  

    scr.move(0, 0)
