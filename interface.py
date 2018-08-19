import piece, game, player, curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    curses.curs_set(0)

    lines = curses.LINES - 1
    cols = curses.COLS - 1
    
    # Diving the screen into 3 parts

    board = stdscr.subwin(curses.LINES, int(3*(curses.COLS/5)), 0, int(curses.COLS/5) + 1)
    board.border()

    comm = stdscr.subwin(curses.LINES, int(curses.COLS/5), 0, 0)
    comm.border()

    c_pos = (1, 1)
    
    info = stdscr.subwin(curses.LINES, int(curses.COLS/5), 0, int((4/5)*curses.COLS) + 1)
    info.border()

    # Passing numbers greater than 8 or so will break this (attempting to draw outside window)
    pos = draw_board(board, board.getmaxyx()[0], board.getmaxyx()[1], 3, 6)
    set_pieces(board, pos)

    game1 = game.Game("Nate", "Olivia", pos, board)

    stdscr.refresh()
    stdscr.getkey()

        
    in_progress = True 
    while(in_progress):
        move = get_move(comm, c_pos) 
        game1.move(move[0], move[1], move[2])


    stdscr.refresh() 
    stdscr.getkey()

    return pos

def draw_board(scr, lines, cols, box_lines, box_cols):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
 
    # Brush is used for drawing the board, pair will choose the color pair 
    brush = " " * box_cols
    pair = True 

    # The coordinate of each squares center will be stored here and returned
    positions = [None] * 8 
    for i in range(0, 8):
        positions[i] = [None] * 8

    # Mapping the looping variables to chess coordinates
    alph = {4:"A", 3:"B", 2:"C", 1:"D", 0:"E", -1:"F", -2:"G", -3:"H"}
    
    py = 7 
    for i in range(4, -4, -1):
        px = 0 
        pair = not pair
        
        # These draw the coordinates on the sides, using the alph dictonary
        scr.addstr(int(lines/2 - i*box_lines) + int(box_lines/2), int(cols/2 - 5*box_cols), str(i+4), curses.A_BOLD)
        scr.addstr(int(lines/2 - 5*box_lines) + int(box_lines/2) , int(cols/2 - i*box_cols) + int(box_cols/2), alph[i], curses.A_BOLD)
    
        # Drawing the actual board using the brush str
        for j in range(4, -4, -1):
            pair = not pair
            
            # Taking note of the center of each box for managing pieces and moves later
            positions[py][px] = (int(lines/2 - i*box_lines) + int(box_lines/2), int(cols/2 - j*box_cols) + int(box_cols/2))
            for k in range(0, box_lines):
                scr.addstr(int(lines/2 - i*box_lines) + k, int(cols/2 - (j*box_cols - 1)), brush, curses.color_pair(1 if pair else 2))

            px = px + 1
        py = py - 1

    scr.move(0, 0)

    return positions

def set_pieces(scr, pos):
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    pieces = {0:"R1", 1:"k1", 2:"B1", 3:"Kg", 4:"Qn", 5:"B2", 6:"k2", 7:"R2"}
        
    for i in range(0, 8):
        scr.addstr(pos[0][i][0], pos[0][i][1], pieces[i], curses.color_pair(3))  
        scr.addstr(pos[1][i][0], pos[1][i][1], 'P' + str(i+1), curses.color_pair(3))  
        scr.addstr(pos[6][i][0], pos[6][i][1], 'P' + str(i+1), curses.color_pair(4))
        scr.addstr(pos[7][i][0], pos[7][i][1], pieces[i], curses.color_pair(4))  

    scr.move(0, 0)

def get_str(scr, max_len):

    curses.echo()
    curses.curs_set(2)
    
    usr_in = ''
    cur_len = 1;
    tmp = scr.getkey()   

    while(tmp != '\n' and cur_len < max_len):
        if tmp == 'KEY_BACKSPACE' and cur_len > 1:
            #cur_len -= 1                
            #usr_in = usr_in[:-1]
            #curs_pos = scr.getyx()
            #scr.move(curs_pos[0], curs_pos[1] - 1)
            scr.erase() 
 
        usr_in += tmp
        cur_len += 1
        tmp = scr.getkey()
           
    if(cur_len == max_len):
        usr_in += tmp
 
    curses.noecho()
    curses.curs_set(0)

    return usr_in 

def get_max_len(scr, message):
    return scr.getmaxyx()[1] - 2 - len(message) 


def get_move(scr, in_pos):

    cur_line = 0 
    move = [None] * 3

    need_input = True
    while(need_input):
        # Get the player number
        message = "Enter player number: " 
        scr.addstr(in_pos[0] + cur_line, in_pos[1], message) 
        tmp = get_str(scr, get_max_len(scr, message))
        cur_line += 1
    
        try:
            player_num = int(tmp) - 1
            if(player_num != 0 and player_num != 1):
                raise ValueError()

            # If we make it here, the input is good!
            move[0] = player_num

            need_input = False
        except ValueError:
            scr.addstr(in_pos[0] + cur_line, in_pos[1], "Please enter a valid player number") 
            cur_line += 1          

    need_input = True
    while(need_input):
        # Get the piece number
        message = "Enter piece number: " 
        scr.addstr(in_pos[0] + cur_line, in_pos[1], message) 
        tmp = get_str(scr, get_max_len(scr, message))
        cur_line += 1
    
        try:
            piece_num = int(tmp) - 1
            if(piece_num > 15 or piece_num < 0):
                raise ValueError()

            # If we make it here, the input is good!
            move[1] = piece_num
        
            need_input = False
        except ValueError:
            scr.addstr(in_pos[0] + cur_line, in_pos[1], "Please enter a valid piece number") 
            cur_line += 1          

    need_input = True
    while(need_input):
        # Get the move coordinates 
        message = "Enter move coordinates: " 
        scr.addstr(in_pos[0] + cur_line, in_pos[1], message) 
        tmp = get_str(scr, get_max_len(scr, message))
        cur_line += 1
    
        try:
            if(len(tmp) != 3):
                raise ValueError()

            row = int(tmp[0]) - 1       
            if(row < 1 or row > 8):
                raise ValueError()

            col = ord(tmp[2])
            if(col >= 97 and col <= 104):
                col = col - 97   
            elif(col >= 64 and col <= 72):
                col = col - 64  
            else:
                raise ValueError() 
            
            move_coords = (row, col)

            # If we make it here, the input is good!
            move[2] = move_coords 
        
            need_input = False
        except ValueError:
            scr.addstr(in_pos[0] + cur_line, in_pos[1], "Enter valid coordinates in form:\n [row col]") 
            cur_line += 2          
            scr.border()

    scr.erase()
    scr.border()
 
    return move 
 

