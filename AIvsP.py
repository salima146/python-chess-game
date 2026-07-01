import random
import pygame
import tkinter as tki
import threading
from Timer import Timer_game

pygame.init()

#screen dimensions
Width = 1000
Height = 800
screen = pygame.display.set_mode([Width, Height])  # show the size of the screen
pygame.display.set_caption('PLAYER vs PLAYER')

# Setting the fonts
font = pygame.font.Font(None, 23)  #here i have used a default font 
M_font = pygame.font.Font(None, 40)# medium size font
Larger_font = pygame.font.Font(None, 60)  # this is using a bigger default font

# Timer and FPS settings
timer = pygame.time.Clock()  # controls the speed at which the game updates
FPS = 90 # frame per second

#chessboard foundation(what the basics of the board will look like)
SquareSize = Width // 8 # dividing it by 8, as it would be an 8 by 8 board
Light_colour = (255, 182, 193) #colour of light pink squares, using RGB values
Dark_colour = (252, 142,172) #colour of pink squares, using RGB values

window = None
def begin_timer():
    global window
    window = tki.Tk()
    app_use  = Timer_game(window)
    window.mainloop()

threading.Thread(target = begin_timer, daemon = True).start()



# Chess pieces and the positions
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)] # this would be the locations of where the pieces would be initally

pink_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
pink_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), # 1st row
                 (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)] # 2nd row for pawns


Captured_WhitePieces = [] #these are piece that would have been captured by the player or opponent(white pieces)
Captured_PinkPieces = []#these are piece that would have been captured by the player or opponent(pink pieces)
step_turns = 0  # allows us to know what pieces are currently on the board
select = 99
ValidMoves = []

#pink chess pieces, this would load the images onto the display, is done for all 6 pieces
pink_king = pygame.image.load('pieces/pink_king.png')
pink_queen = pygame.image.load('pieces/pink_queen.png')                          
pink_bishop = pygame.image.load('pieces/pink_bishop.png')                        
pink_knight = pygame.image.load('pieces/pink_knight.png')                         
pink_rook = pygame.image.load('pieces/pink_rook.png')                         
pink_pawn = pygame.image.load('pieces/pink_pawn.png')

#image resize
pink_king = pygame.transform.scale(pink_king,(80, 80)) #resize the image depending on the size of the square on the board                           
pink_queen = pygame.transform.scale(pink_queen,(80, 80))# this is the size of the queen in the board, the x and y value
pink_bishop = pygame.transform.scale(pink_bishop,(80, 80))
pink_knight = pygame.transform.scale(pink_knight,(80, 80))
pink_rook = pygame.transform.scale(pink_rook,(80, 80))
pink_pawn = pygame.transform.scale(pink_pawn,(80, 80))                              

#here is the smaller version that will be put to the side when it has been captured
smaller_pink_king = pygame.transform.scale(pink_king, (45, 45)) #have divided by 2 becuase it will make it smaller and be able to fit on the side when discard/captured
smaller_pink_queen = pygame.transform.scale(pink_queen, (45, 45))
smaller_pink_bishop = pygame.transform.scale(pink_bishop, (45, 45))
smaller_pink_knight = pygame.transform.scale(pink_knight, (45, 45))
smaller_pink_rook = pygame.transform.scale(pink_rook, (45, 45))
smaller_pink_pawn = pygame.transform.scale(pink_pawn, (45, 45))


#This part is where the uploads of the images of the chess piece will be for both white
white_king = pygame.image.load('pieces/white_king.png')
white_queen = pygame.image.load('pieces/white_queen.png')
white_bishop = pygame.image.load('pieces/white_bishop.png')
white_knight = pygame.image.load('pieces/white_knight.png')
white_rook = pygame.image.load('pieces/white_rook.png')
white_pawn = pygame.image.load('pieces/white_pawn.png')

#image resize
white_king = pygame.transform.scale(white_king,(80, 80))                           
white_queen = pygame.transform.scale(white_queen,(80, 80))
white_bishop = pygame.transform.scale(white_bishop,(80, 80))
white_knight = pygame.transform.scale(white_knight,(80, 80))
white_rook = pygame.transform.scale(white_rook,(80, 80))
white_pawn = pygame.transform.scale(white_pawn,(80, 80))

#here is the smaller version that will be put to the side when it has been captured
smaller_white_king = pygame.transform.scale(white_king, (45, 45))
smaller_white_queen = pygame.transform.scale(white_queen, (45, 45))
smaller_white_bishop = pygame.transform.scale(white_bishop, (45, 45))
smaller_white_knight = pygame.transform.scale(white_knight, (45, 45))
smaller_white_rook = pygame.transform.scale(white_rook, (45, 45))
smaller_white_pawn = pygame.transform.scale(white_pawn, (45, 45))

#list for all the pink piece images
images_white = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
#list that will help to know which white piece has been captured
smaller_white_pieces = [smaller_white_pawn, smaller_white_queen, smaller_white_king, smaller_white_knight,
                        smaller_white_rook, smaller_white_bishop]
                                    
#list for all the pink piece images
images_pink = [pink_pawn, pink_queen, pink_king, pink_knight, pink_rook, pink_bishop]
#list that will help to know which pink piece has been captured
smaller_pink_pieces = [smaller_pink_pawn, smaller_pink_queen, smaller_pink_king, smaller_pink_knight,
                       smaller_pink_rook, smaller_pink_bishop]

list_for_pieces = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop' ]
count = 0
victory = ''
Game_End = False


def Display_board():
    for k in range(32):
        vertically = k % 4
        horizontally = k // 4
        if horizontally % 2 == 0:
            pygame.draw.rect(screen, Light_colour, [600 - (vertically * 200), horizontally * 100, 100, 100])
        else:
            pygame.draw.rect(screen, Light_colour, [700 - (vertically * 200), horizontally * 100, 100, 100])
        pygame.draw.rect(screen, Dark_colour, [0, 800, Width, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, Width, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, Height], 5)
        state_text_update = ['White: Select a piece in order to move', 'White: Select a location',
                             'Pink: Select a piece in order to move', 'Pink: Select a location']
        screen.blit(Larger_font.render(state_text_update[step_turns], True, 'pink'), (20, 820))
        for k in range(9):
            pygame.draw.line(screen, 'pink', (0, 100 * k), (800, 100 * k), 2)
            pygame.draw.line(screen, 'pink', (100 * k, 0), (100 * k, 800), 2)
        screen.blit(M_font.render('YIELD', True, 'pink'), (810, 830))

def display_pieces_images():
    for k in range(len(white_pieces)):
        index = list_for_pieces.index(white_pieces[k])
        if white_pieces[k] == 'pawn':
            screen.blit(white_pawn, (white_location[k][0] * 100 + 22, white_location[k][1] * 100 + 30))
        else:
            screen.blit(images_white[index], (white_location[k][0] * 100 + 10, white_location[k][1] * 100 + 10))
        if step_turns < 2:
            if select == k:
                pygame.draw.rect(screen, 'white', [white_location[k][0] * 100 + 1, white_location[k][1] * 100 + 1,
                                                 100, 100], 2)

    for k in range(len(pink_pieces)):
        index = list_for_pieces.index(pink_pieces[k])
        if pink_pieces[k] == 'pawn':
            screen.blit(pink_pawn, (pink_location[k][0] * 100 + 22, pink_location[k][1] * 100 + 30))
        else:
            screen.blit(images_pink[index], (pink_location[k][0] * 100 + 10, pink_location[k][1] * 100 + 10))
        if step_turns >= 2:
            if select == k:
                pygame.draw.rect(screen, 'pink', [pink_location[k][0] * 100 + 1, pink_location[k][1] * 100 + 1,
                                                   100, 100], 2)
                


#function: checks valid moves
def Check_Option(pieces, location, player_turn):
    list_of_moves = [] #list of all moves, empty now becuase it can be append later on
    full_list_moves = []
    for j in range((len(pieces))):
       locations = location[j]
       piece = pieces[j]

        #checks what the piece is
       if piece == 'pawn':
           list_of_moves = Valid_Check_pawn(locations, player_turn)#a seperate function that will check the valid moves for a king
       elif piece == 'rook':
            list_of_moves = Valid_Check_rook(locations, player_turn)#a seperate function that will check the valid moves for a queen
       elif piece == 'knight':
            list_of_moves = Valid_Check_knight(locations, player_turn)#a seperate function that will check the valid moves for a bishop
       elif piece == 'bishop':
            list_of_moves = Valid_Check_bishop(locations, player_turn)#a seperate function that will check the valid moves for a knight
       elif piece == 'queen':
            list_of_moves = Valid_Check_queen(locations, player_turn)#a seperate function that will check the valid moves for a rook
       elif piece == 'king':
            list_of_moves = Valid_Check_king(locations, player_turn)#a seperate function that will check the valid moves for a pawn
       full_list_moves.append(list_of_moves)
    return full_list_moves # return a list of all the moves a piece can take


#Below is a function that checks the valid moves for a king
def Valid_Check_king(setting, colour_turn):
    list_of_moves = []
    if colour_turn == 'white': #if the colour were to be white for the piecces
        opponent_list = pink_location #then make the list of the opponents be the pinks
        ally_list = white_location # and make the ally the whites as they are on the same team
    else:
        ally_list = pink_location
        opponent_list = white_location
    aim_marks = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8): #reason for 8 is becuase a king can move one square in any direction possible
        aim_mark = (setting[0] + aim_marks[i][0], setting[1] + aim_marks[i][1]) #what would be targetted
        if aim_mark not in ally_list and 0 <= aim_mark[0] <= 7 and 0 <= aim_mark[1] <= 7:
            list_of_moves.append(aim_mark) #change what the target for the kning would be
    
    return list_of_moves

#Below is a function that checks the valid moves for a queen
def Valid_Check_queen(setting, colour_turn):
    list_of_moves = Valid_Check_bishop(setting, colour_turn)#this would return all the moves as if the queen were to be a bishop
    list_num2 = Valid_Check_rook(setting, colour_turn)#this would return all the moves as if the queen were to be a rook
    for i in range(len(list_num2)):
        list_of_moves.append(list_num2[i]) # adds the rook moves into the list of moves
    return list_of_moves




#Below is a function that checks the valid moves for a bishop
def Valid_Check_bishop(setting, colour_turn):
    list_of_moves = []
    if colour_turn == 'white':
        opponent_list = pink_location
        ally_list = white_location
    else:
        ally_list = pink_location
        opponent_list = white_location
    for i in range(4): # this is a loop that will check down-right, up-right, up-left and down-left
        lane = True #checks if we have a valid path for the bishop to go through
        total_chain = 1 #variable means the chain of pieces in bishop way is 1 but value will change as if there is another open space
        if i == 0: #all the valid moves for a bishop
            x_val = 1 #the x value, up-right
            y_val = -1 #the y value

        elif i == 1: #up-left
            x_val = -1
            y_val = -1

        elif i == 2: #down-right
            x_val = 1
            y_val = 1
        else: #down-left
            x_val = -1 
            y_val = 1
        while lane:#line of code below checks if that bishop can continue going in a certain direction condition in order to move the bishop: the square has to have the opponent in it or it has to be empty
            if (setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val)) not in ally_list and \
                    0 <= setting[0] + (total_chain * x_val) <= 7 and 0 <= setting[1] + (total_chain * y_val) <= 7:
                list_of_moves.append((setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val))) #allows us to add it to the list of moves
                if (setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val)) in opponent_list:#this is for the opponent list
                    lane = False #stop moving if it is in the opponent area
                total_chain += 1
            else:
                lane = False
    return list_of_moves

#Below is a function that checks the valid moves for a rook
def Valid_Check_rook(setting, colour_turn):
    list_of_moves = []
    if colour_turn == 'white':
        opponent_list = pink_location
        ally_list = white_location
    else:
        ally_list = pink_location
        opponent_list = white_location
    for i in range(4): # this is a loop that will check down, up, right and left
        lane = True #checks if we have a valid path for the rook to go through
        total_chain = 1 #variable means the chain of pieces in rook way is 1 but value will change as if there is another open space
        if i == 0: #all the valid moves for a rook
            x_val = 0 #the x value, going down
            y_val = 1 #the y value

        elif i == 1: # going up
            x_val = 0
            y_val = -1

        elif i == 2: #going to the right
            x_val = 1
            y_val = 0
        else:
            x_val = -1 #going to the left
            y_val = 0
        while lane: # line of code below checks if that rook can continue going in a certain direction condition in order to move the rook: the square has to have the opponent in it or it has to be empty
            if (setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val)) not in ally_list and \
                    0 <= setting[0] + (total_chain * x_val) <= 7 and 0 <= setting[1] + (total_chain * y_val) <= 7:
                list_of_moves.append((setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val))) #allows us to add it to the list of moves
                if (setting[0] + (total_chain * x_val), setting[1] + (total_chain * y_val)) in opponent_list:#this is for the opponent list
                    lane = False 
                total_chain += 1
            else:
                lane = False
    return list_of_moves
                




#Below is a function that checks the valid moves for a pawn (setting = position)
def Valid_Check_pawn(setting, colour_turn):
    list_of_moves = []
    if colour_turn == 'white':
        #below this means move the white pawn is currently not take by a white piece
        if (setting[0], setting[1] + 1) not in white_location and \
               (setting[0], setting[1] + 1) not in pink_location and setting[1] < 7:
            list_of_moves.append((setting[0], setting[1] + 1))  #allowed to go one piece toward the color
        if (setting[0], setting[1] + 2) not in white_location and \
                (setting[0], setting[1] + 2) not in pink_location and setting[1] == 1:
            list_of_moves.append((setting[0], setting[1] + 2))
        if (setting[0] + 1, setting[1] + 1) in pink_location:
            list_of_moves.append((setting[0] + 1, setting[1] + 1))
        if (setting[0] - 1, setting[1] + 1) in pink_location:
            list_of_moves.append((setting[0] - 1, setting[1] + 1))
        #above code creates guide on where the pawn can be put on the white side
    else:
        #below this means move the pink pawn is currently not take by a pink piece
         if (setting[0], setting[1] - 1) not in white_location and \
                (setting[0], setting[1] - 1) not in pink_location and setting[1] > 0:
            list_of_moves.append((setting[0], setting[1] - 1))  #allowed to go one piece toward the color
         if (setting[0], setting[1] - 2) not in white_location and \
                (setting[0], setting[1] - 2) not in pink_location and setting[1] == 6:
            list_of_moves.append((setting[0], setting[1] - 2))
         if (setting[0] + 1, setting[1] - 1) in white_location:
            list_of_moves.append((setting[0] + 1, setting[1] - 1))
         if (setting[0] - 1, setting[1] - 1) in white_location:
            list_of_moves.append((setting[0] - 1, setting[1] - 1))
        #above code creates guide on where the pawn can be put on the pink side
    return list_of_moves

#below is a function that checks the valid moves for a knight
def Valid_Check_knight(setting, colour_turn):
    list_of_moves = []
    if colour_turn == 'white':
        opponent_list = pink_location #this is when the colour white is chosen then enemy would be pink
        ally_list = white_location # this is when the color white is chosen then ally would be white
    else:
        ally_list = pink_location#this is when the colour pink is chosen then ally would be pink
        opponent_list = white_location # this is when the color pink is chosen then enemy would be white
    aim_marks = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8): #reason for 8 is becuase a knight can somewhat move in a circle-like shape, the corners, front, back, left and right
        aim_mark = (setting[0] + aim_marks[i][0], setting[1] + aim_marks[i][1]) #what would be targetted
        if aim_mark not in ally_list and 0 <= aim_mark[0] <= 7 and 0 <= aim_mark[1] <= 7:
            list_of_moves.append(aim_mark) #change what the target for the knight would be
    return list_of_moves



def Check_moves_valid():
    if step_turns < 2:
        list_of_options = white_piece_options
    else:
        list_of_options = pink_piece_options
    options_valid = list_of_options[select]
    return options_valid
        
#here is a function that will allow valid moves to be drawn onto the board           
def Valid_moves_draw(moves):
    if step_turns < 2:
        colour_turn = 'white'
    else:
        colour_turn = 'pink'
    for k in range(len(moves)):
        pygame.draw.circle(screen, colour_turn, (moves[k][0] * 100 + 50, moves[k][1] * 100 + 50), 5)

def display_captured_pieces():
    for k in range(len(Captured_WhitePieces)):
        CapturedPiece = Captured_WhitePieces[k]
        index = list_for_pieces.index(CapturedPiece)
        screen.blit(smaller_pink_pieces[index], (825, 5 + 50 * k))
    for k in range(len(Captured_PinkPieces)):
        CapturedPiece = Captured_PinkPieces[k]
        index = list_for_pieces.index(CapturedPiece)
        screen.blit(smaller_white_pieces[index], (925, 5 + 50 * k))

def display_check():
    if step_turns < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            location_king = white_location[king_index]
            for k in range(len(pink_piece_options)):
                if location_king in pink_piece_options[k]:
                    if count < 15:
                        pygame.draw.rect(screen, 'white', [white_location[king_index][0] * 100 + 1,
                                                           white_location[king_index][1] * 100 + 1, 100, 100], 5)
    else:

        if 'king' in pink_pieces:
            king_index = pink_pieces.index('king')
            location_king = pink_location[king_index]
            for k in range(len(white_piece_options)):
                if location_king in white_piece_options[k]:
                    if count < 15:
                        pygame.draw.rect(screen, 'pink', [pink_location[king_index][0] * 100 + 1,
                                                          pink_location[king_index][1] * 100 + 1, 100, 100], 5)




def display_Game_End():
    pygame.draw.rect(screen, 'pink', [200, 200, 400, 70])
    screen.blit(font.render(f'{victory} is the winner!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press enter to Restart', True, 'white'), (210, 240))

def AI_movement():
    ava_moves = []
    for k in range(len(pink_pieces)):
        piece = pink_pieces[k]
        locations = pink_location[k]
        if piece == 'pawn':
            moves = Valid_Check_pawn(locations, 'pink')
        elif piece == 'rook':
            moves = Valid_Check_rook(locations, 'pink')
        elif piece == 'knight':
            moves = Valid_Check_knight(locations, 'pink')
        elif piece == 'bishop':
            moves = Valid_Check_bishop(locations, 'pink')
        elif piece == 'queen':
            moves = Valid_Check_queen(locations, 'pink')
        elif piece == 'king':
            moves = Valid_Check_king(locations, 'pink')
        if moves:
            ava_moves.append((k, moves))

    
    if ava_moves:
        piece_index, ValidMoves = random.choice(ava_moves)
        movement = random.choice(ValidMoves)
        pink_location[piece_index] = movement

        if movement in white_location:
            CapturedPiece = white_pieces[white_location.index(movement)]
            Captured_PinkPieces.append(CapturedPiece)
            white_pieces.pop(white_location.index(movement))
            white_location.remove(movement)
        return True
    return False
#function for a border around piece that has been selected

# Game loop
pink_piece_options = Check_Option(pink_pieces, pink_location, 'pink')
white_piece_options = Check_Option(white_pieces, white_location, 'white')
run = True
while run:
    timer.tick(FPS)  #frame rate
    if count < 30:
        count += 1
    else:
        count = 0
    screen.fill((255, 105, 180))  # use RGB colours to make a different shade of pink, background colour
    Display_board()
    display_pieces_images()
    display_captured_pieces()
    display_check()

    
    if select != 99:
        ValidMoves = Check_moves_valid()
        Valid_moves_draw(ValidMoves)


    # this gets all the computer inputs on here such as the mouse and keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check if the player has decided to quit by closing windows
            run = False #this will exist the game loop that will stop the game completely

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not Game_End:#this checks if it is only a left mouse click
            x_coordinate = event.pos[0] // 100 #tell the x and y clicks that the mouse has done
            y_coordinate = event.pos[1] // 100
            total_click_coords = (x_coordinate, y_coordinate)
            if step_turns <= 1:
                if total_click_coords == (8, 8) or total_click_coords == (9, 8):
                    victory = 'pink'
                if total_click_coords in white_location:
                    select = white_location.index(total_click_coords) #what piece that the player has selected
                    if step_turns == 0: #do not have anything selected
                        step_turns = 1 #now you have selected
                if total_click_coords in ValidMoves and select != 99: #checks if it is a valid move
                    white_location[select] = total_click_coords
                    if total_click_coords in pink_location: #takes us to the location where the pink piece was initally
                        pink_piece = pink_location.index(total_click_coords)
                        Captured_WhitePieces.append(pink_pieces[pink_piece]) # the list of captured pieces for the white
                        if pink_pieces[pink_piece] == 'king':
                            victory = 'white'
                        pink_pieces.pop(pink_piece)
                        pink_location.pop(pink_piece)
                    #below it shows the options and valid moves piece can do
                    
                    pink_piece_options = Check_Option(pink_pieces, pink_location, 'pink')
                    white_piece_options = Check_Option(white_pieces, white_location, 'white')
                    step_turns = 2
                    select = 99
                    ValidMoves = []
                    
            if step_turns > 1:
                if total_click_coords == (8, 8) or total_click_coords == (9, 8):
                    victory = 'white'
                if total_click_coords in pink_location:
                    select = pink_location.index(total_click_coords) #what piece that the player has selected
                    if step_turns == 2: # selection of piece
                        step_turns = 3 #now you have selected
                if total_click_coords in ValidMoves and select != 99: #checks if it is a valid move
                    pink_location[select] = total_click_coords
                    if total_click_coords in white_location: #takes us to the location where the pink piece was initally
                        white_piece = white_location.index(total_click_coords)
                        Captured_PinkPieces.append(white_pieces[white_piece]) # the list of captured pieces for the white
                        if white_pieces[white_piece] == 'king':
                            victory = 'pink'
                        white_pieces.pop(white_piece)
                        white_location.pop(white_piece)
                    #below it shows the options and valid moves piece can do
                    pink_piece_options = Check_Option(pink_pieces, pink_location, 'pink')
                    white_piece_options = Check_Option(white_pieces, white_location, 'white')
                    
                    step_turns = 0
                    select = 99
                    ValidMoves = []
                    
        if step_turns == 2: # this is the pinks turn
            if AI_movement(): # this is if the AI makes the move
                pink_piece_options = Check_Option(pink_pieces, pink_location, 'pink')#the pink options available
                white_piece_options = Check_Option(white_pieces, white_location, 'white')#the white options available
                step_turns = 0

        if Game_End:
            display_Game_End()
            
        if event.type == pygame.KEYDOWN and Game_End:
            if event.key == pygame.K_RETURN:
                Game_End = False
                victory = ''

                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                
                pink_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                               'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                pink_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), # 1st row
                                 (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)] # 2nd row for pawns
                    
                Captured_WhitePieces = []
                Captured_PinkPieces = []
                step_turns = 0
                select = 99
                ValidMoves = []
                pink_piece_options = Check_Option(pink_pieces, pink_location, 'pink')
                white_piece_options = Check_Option(white_pieces, white_location, 'white')

    if victory != '':
        Game_End = True
        display_Game_End()

    # display everything onto the screen
    pygame.display.flip()

# Quit the game
pygame.quit()

if window:
    window.quit()
            
                












                
                
                
                
