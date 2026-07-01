import pygame
import sys
import subprocess

pygame.init()

#this is the part where the dimensions of the screen are made created
width_display = 800
height_display = 600

display = pygame.display.set_mode((width_display, height_display))#where the screen will be displayed

#where the title will be written
pygame.display.set_caption('Welcome to Chess')

#this is the font size that will say what the game mode it is for example: AI vs PLayer
pygame.font.init()
Large_font = pygame.font.Font(None, 50)

#colours of the items on the screen
light_pink = (255, 182, 193) #colour of light pink background, using RGB values
dark_pink = (252, 142,172) #colour of pink for buttons, using RGB values
hover_colour = (216, 160, 166)# this is the colour for when the user is hovering over the button
title_colour = (255, 20, 147)
#now a class will be used for the button control
class button:
    def __init__(self, content, x_coord, y_coord, WIDTH, HEIGHT, COLOUR, HOVER_COLOUR):
        self.content = content # this is for the content of text that will be displayed on the button
        self.rect = pygame.Rect(x_coord, y_coord, WIDTH, HEIGHT)# this is the shape of the button, which is a rectangle, including botht width and height
        self.COLOUR = COLOUR # colour of the button
        self.HOVER_COLOUR = HOVER_COLOUR # this is the colour when the hover effect is implemented

    #this section is drawing the button in the accurate area on the screen for user display
    def draw_button(self, display, mouse_pos):
        #Here it will consider depending on where the user is hovering over the button or not the colour of the button
        present_colour = self.HOVER_COLOUR if self.rect.collidepoint(mouse_pos) else self.COLOUR
        pygame.draw.rect(display, present_colour, self.rect) # this will draw the shape of the buttons which is a rectangle

        #this is to modifiy the text
        display_text = Large_font.render(self.content, True, title_colour)
        text_rect = display_text.get_rect(center=self.rect.center) # this will position the text in the center of the buttons
        display.blit(display_text, text_rect) # this section is where the text is drawn on the screen for user display

    def click(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0] == 1
    #above section of code checks if the button has been clicked on,
    #it will return True if the mouse has hovering over the button and is pressed


#a class is created to create the main menu section of the program
class Main_Menu:
    def __init__(self, display):
        self.display = display
        self.BUTTONS = [#these are going to be the buttons for the game mode
            button("Player VS Player", 280, 200, 300, 70, dark_pink, hover_colour), # player vs player game mode button
            button("AI VS Player", 280, 300, 300, 70, dark_pink, hover_colour), # AI vs player game mode button
            button("Quit", 280, 400, 300, 70, dark_pink, hover_colour) # quit button
        ]
        #the bow will be for design above the player vs player
        #Here is the way the image is loaded
        self.queen = pygame.image.load("queen.png") #load the image
        self.queen = pygame.transform.scale(self.queen, (210, 190)) #this will the size the image
    def Game_file(self, Game_Mode):
        try:
            subprocess.run(["python", Game_Mode], check=True)
        except Exception as e:
            print("error occured")

        
    def run(self):
        operate = True
        while operate:
            self.display.fill(light_pink) #this will fill the background with a light pink colour
            mouse_pos = pygame.mouse.get_pos() # this will tell us what the current position of the mouse is
            mouse_click = pygame.mouse.get_pressed() # this will check is the mouse has been pressed or not

            #Here the queen image will be drawn
            self.display.blit(self.queen, (320, 10)) # this will place the queen in the accurate area


            #this section of code is drawing the button
            for Button in self.BUTTONS:
                Button.draw_button(self.display, mouse_pos) # this will drawn the button
                if Button.click(mouse_pos, mouse_click): # checking if the button has been clicked or not
                    if Button.content == "Player VS Player":
                        print("Player VS Player game mode will be on display!")
                        self.Game_file("PvsP.py")

                    elif Button.content == "AI VS Player":
                        print("AI VS Player game mode will be on display!")
                        self.Game_file("AIvsP.py")

                    elif Button.content == "Quit":
                        pygame.quit() #quit the game
                        sys.exit() # this will exist the program

            #this is for the event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # this will check the user has closed the window
                    operate = False # this will bring a stop to the main loop

            pygame.display.flip() #update the screen

        pygame.quit() #end the loop



#where the main menu will run
main_menu = Main_Menu(display)
main_menu.run()
