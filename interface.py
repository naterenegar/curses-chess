import piece, game, player, curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.curs_set(0)

    lines = curses.LINES - 1
    cols = curses.COLS - 1

    # Menu screen section
    result = menu_screen(stdscr)
    
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
        display_info(info, game1)
        move = get_move(comm, c_pos) 
        game1.move(move[0], move[1], move[2])


    stdscr.refresh() 
    stdscr.getkey()

    return pos

def menu_screen(scr):
    mid_line = int(curses.LINES/2)
    mid_col = int(curses.COLS/2)
   
    menu_options = ["Welcome to PyChess!", "Start Game", "Quit"]
   
    scr.addstr(mid_line - int(len(menu_options) / 2), mid_col-int(len(menu_options[0])/2), menu_options[0], curses.A_BOLD)
    scr.keypad(True)

    key = -1 
    attrs = [curses.A_REVERSE, 0]
    while(key != '\n'):
        if key == 'KEY_DOWN':
            attrs[0] = 0
            attrs[1] = curses.A_REVERSE               
        elif key == 'KEY_UP':
            attrs[0] = curses.A_REVERSE
            attrs[1] = 0
 
        scr.addstr(mid_line - int(len(menu_options) / 2) + 2, mid_col-int(len(menu_options[1])/2), menu_options[1], attrs[0])
        scr.addstr(mid_line - int(len(menu_options) / 2) + 3, mid_col-int(len(menu_options[2])/2), menu_options[2], attrs[1])
        scr.refresh() 
        
        key = scr.getkey() 

    scr.clear()

    if attrs[0] == curses.A_REVERSE:
        game_options = ["1 Player", "2 Player"] 

        key = -1
        while(key != '\n'):
            if key == 'KEY_DOWN':
                attrs[0] = 0
                attrs[1] = curses.A_REVERSE               
            elif key == 'KEY_UP':
                attrs[0] = curses.A_REVERSE
                attrs[1] = 0
    
            scr.addstr(mid_line - int(len(game_options) / 2), mid_col-int(len(game_options[0])/2), game_options[0], attrs[0])
            scr.addstr(mid_line - int(len(game_options) / 2) + 1, mid_col-int(len(game_options[1])/2), game_options[1], attrs[1])

            scr.refresh() 
            
            key = scr.getkey() 
    else:
        exit()   

    scr.clear()

    if attrs[0] == curses.A_REVERSE:
        mes = "Enter player name: " 
        scr.addstr(mid_line, mid_col-int(len(mes)/2), mes)
        name = get_str(scr, 16)
        scr.clear() 
        return 1
    else:
        mes = "Enter player 1's name: " 
        mes2 = "Enter player 2's name: "
        scr.addstr(mid_line, mid_col-int(len(mes)/2), mes)
        name1 = get_str(scr, 16)
        scr.addstr(mid_line + 1, mid_col-int(len(mes2)/2), mes2)
        name2 = get_str(scr, 16)
        scr.clear()
        return 2 
    
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

def display_info(scr, game):
    pair_0, pair_1 = 0, 0
    divs = int(scr.getmaxyx()[0]/4) 

    # Column headers
    scr.addstr(1, 1 + divs * 0, "Piece")
    scr.addstr(1, 1 + divs * 1, "Player 1")
    scr.addstr(1, 1 + divs * 2, "Player 2")

    for i in range(0, 16):
        pair_0 = 5 if game.players[0].pieces[i].isAlive() else 6
        pair_1 = 5 if game.players[1].pieces[i].isAlive() else 6
    
        scr.addstr(i + 3, 1 + divs * 0, str(game.players[0].pieces[i]))
        scr.addstr(i + 3, 1 + divs * 1, "Alive" if pair_0 == 5 else "Dead ", curses.color_pair(pair_0))
        scr.addstr(i + 3, 1 + divs * 2, "Alive" if pair_1 == 5 else "Dead ", curses.color_pair(pair_1))

    scr.refresh()

def set_pieces(scr, pos):
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    pieces = {0:"R1", 1:"K1", 2:"B1", 3:"Kg", 4:"Qn", 5:"B2", 6:"K2", 7:"R2"}
        
    for i in range(0, 8):
        scr.addstr(pos[0][i][0], pos[0][i][1], pieces[i], curses.color_pair(3))  
        scr.addstr(pos[1][i][0], pos[1][i][1], 'P' + str(i+1), curses.color_pair(3))  
        scr.addstr(pos[6][i][0], pos[6][i][1], 'P' + str(i+1), curses.color_pair(4))
        scr.addstr(pos[7][i][0], pos[7][i][1], pieces[i], curses.color_pair(4))  

    scr.move(0, 0)

def get_str(scr, max_len):

    curses.echo()
    curses.curs_set(2)
    scr.keypad(True)   
 
    usr_in = ''
    cur_len = 1;
    tmp = scr.getkey()   

    while(tmp != '\n' and cur_len < max_len):
        if tmp == 'KEY_BACKSPACE' and cur_len > 1:
            cur_len -= 1                
            usr_in = usr_in[:-1]
            curs_pos = scr.getyx()
            scr.addstr(curs_pos[0], curs_pos[1], " ")
            scr.move(curs_pos[0], curs_pos[1])
        elif tmp == 'KEY_BACKSPACE' and cur_len <= 1:
            curs_pos = scr.getyx()
            scr.move(curs_pos[0], curs_pos[1] + 1)
        elif tmp != 'KEY_BACKSPACE':
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


# Parses user input into a move
def get_move(scr, in_pos):
    cur_line = 0 
    move = [None] * 3

    pieces = {"R1": 0, "K1": 1, "B1": 2, "KG": 3, "QN": 4, "B2": 5, "K2": 6, "R2": 7, 
              "P1": 8, "P2": 9, "P3": 10, "P4": 11, "P5": 12, "P6": 13, "P7": 14, "P8": 15}
    
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
        message = "Enter piece: " 
        scr.addstr(in_pos[0] + cur_line, in_pos[1], message) 
        tmp = get_str(scr, get_max_len(scr, message))
        cur_line += 1
    
         
        try:
            tmp = tmp.upper()
            move[1] = pieces[tmp[0:2]]
            need_input = False
        except KeyError:
            scr.addstr(in_pos[0] + cur_line, in_pos[1], "Please enter a valid piece") 
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
            if(row < 0 or row > 7):
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
