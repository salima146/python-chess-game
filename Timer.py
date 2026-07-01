import tkinter as tki
from tkinter import ttk #this is a themed tkinter
import time #library module needed to handle the time based duties
import threading # this would be heloful to be used in a countdown

#This is the main time application
class Timer_game:
    def __init__(self, window):
        #the main window object
        self.window = window
        self.window.title("timer")# creates the title for the window

        #here the main frame with a background colour is created
        self.outline_frame = tki.Frame(window, bg ="pink", padx = 19, pady = 19)#the size x and y and the colour of the background
        self.outline_frame.pack(padx = 9, pady = 9) # this will add the main frame to the window with empty space

        #the timer value at the beginning, this will be the default value
        self.default_value = tki.IntVar(value = 5)

        #Here it will inform the user as to what they are able to choose from in the timer in minutes
        timer_selection = tki.Label(self.outline_frame, text = "Select Time :", font = ("Arial", 13), bg ="pink", fg="white")
        #above, the background colour has been set a value of pink and the font colour to white with the size and small text to make the users aware where they select ime
        timer_selection.pack(pady = 8) # adding a padding around the label area

        #give the option to the user to choise between timing intervals (5,10,15,20,25...)
        time_intervals = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        #create the main where the timings can be selected by the user
        self.menu = ttk.Combobox(self.outline_frame, textvariable = self.default_value, values = time_intervals, state = "readonly")
        #above, #this "readonly" is from the list chosen from the Combobox as it limites the user to choose from the options given
        self.menu.pack(pady = 4) #this will add the padding needed for the spaoce that is around the combobox

        #now the button will be created where the timer will starts once it has been clicked
        self.button = tki.Button(
            self.outline_frame,
            text = "Start",
            command = self.timer_starter, # this function is created in order to call the button once clicked
            font = ("Arial", 13),#font type and size
            bg = "hotpink",#the background colour of the button
            fg = "white",#this is for the font colour on the button
        )
        self.button.pack(pady = 9) # adding the padding for the space around the button

        #this will create a frame tyoe that will display the timer with background colour
        self.frame = tki.Frame(self.outline_frame, bg = "hotpink", width = 199, height = 79) #outline the height and width of thw frame
        self.frame.pack(pady=19) # this will add the padding for the soace that is around the timer
        self.frame.pack_propagate(False) # this will help to reduce the frame being resized due to its amount of content
            
        #create a inital display format
        self.initial_format = tki.Label(self.frame, text = "00:00", font = ("Arial", 23), bg = "hotpink", fg = "white") 
        self.initial_format.pack(expand = True) # this will expand the area and then fill the empty space that is inside the frame

        #below the line of code will be used to track if the timer is running currently
        self.operate = False
    


    def timer_starter(self): # this will start the timer once it has been clicked
        if not self.operate:#this will check if the timer is not running beforehand
            self.operate = True # allow when to know the timer is running
            self.button.config(state = tki.DISABLED) #prevent the user from clicking on the start button multile times, it disables the start button
            countdown = self.default_value.get() * 60 #this will convert the default value and timing selected into seconds
            threading.Thread(target = self.timer_running, args = (countdown,)).start() #this will start a thread(allows to have mutliple takes operating concurrently) for the countdown

    def timer_running(self, countdown):#help to handle the countdown
        while countdown > 0 and self.operate: # the timer will operate until it has reached 0 and then stopp
            mins, secs = divmod(countdown, 60) # allow to convert seconds into minuites and seconds
            self.initial_format.config(text = f"{mins:02d} : {secs:02d}") # keep updating the inital format from "00:00" to whatever time is left
            self.window.update() # this will fresh window for updated format
            time.sleep(1) #will wait for one seconds and then update the timer format
            countdown -= 1 #this will decrease the countdown by 1 second each time

        #this here will update the format of the timer once the timer has come to the end
        self.initial_format.config(text = "Time is up!" if countdown == 0 else "Stop!")
        self.button.config(state = tki.NORMAL) #allow for the start button to be clicked again
        self.operate = False # this will tell when the timer has been stopped


            
    def Time_Stop(self): # this here will stop the timer once countdown has come to the end
            self.operate = False

 #here the the timer will be run   
if __name__ == "__main__":
    window = tki.Tk() # creates the main application
    application = Timer_game(window) #this will create the instance for the timer
    window.mainloop() # this will start the Tkinter event loop
