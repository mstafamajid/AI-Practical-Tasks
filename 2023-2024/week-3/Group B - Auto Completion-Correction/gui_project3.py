from tkinter import *
from tkinter import Tk
from app import Project3



window = Tk()
window.geometry("800x500")

frame = Frame(window)

table = None

input_word = "" # is the input word
selected_word = None
#five words button method
def words(word):
    global selected_word
    entry.delete(0, 'end')
    entry.insert(0, word[2])
    selected_word = word


#submit button method
def submit():
    global table, input_word, selected_word

    word = selected_word

    window2 = Tk()
    window2.geometry("800x500")


    frame2 = Frame(window2)
    frame2.config(width=100, height=100)

    list = ["0"]
    for loop in range(len(word[2]) ):
        list.append( word[2][loop] )
    
    # button = Button(root, image=icon, text="Click Me", compound="left", command=lambda: print("Button clicked!"))

    input = input_word
    input_length = len( input )
    input_count = 0
    canvas = Canvas(table, width=100, height=50, background="white")
    # canvas.pack()

    for row in range( len(word[3]) ):
        
        for column in range( len(word[3][1]) ):
            if row==0 and column == 1:
                table = Text(frame2, width=2, height=1, bg="white", fg="blue")
                table.config( font=5 )
                table.tag_config( 'center', justify='center' )
                table.grid(row=0, column=1)
                table.insert(INSERT, '0')
                counter_grid=1
                for loopChar in range( len(word[2]) ):
                    table = Text(frame2, width=2, height=1, bg="white", fg="blue")
                    table.config( font=5 )
                    table.tag_config( 'center', justify='center' )
                    table.grid(row=row, column=counter_grid+1)
                    table.insert(INSERT, word[2][loopChar])
                    counter_grid+=1

            if column == 0 and row > 0 and input_count<input_length:
                table = Text(frame2, width=2, height=1, bg="white", fg="blue")
                table.config( font=5 )
                table.tag_config( 'center', justify='center' )
                table.grid(row=1, column=0)
                table.insert(INSERT, '0')

                table = Text(frame2, width=2, height=1, bg="white", fg="blue")
                table.config( font=5 )
                table.tag_config( 'center', justify='center' )
                table.grid(row=row+1, column=0)
                table.insert(INSERT, input[input_count] )
                input_count+=1


            table = Text(frame2, width=3, height=1, bg="black", fg="white")
            table.config( font=5 )
            table.tag_config( 'center', justify='center' )
            
            
            canvas.grid( row=row+1, column=column+1 )
            table.grid(row=row+1, column=column+1)
            table.insert(INSERT, word[3][row][column])



    frame2.pack()


submit = Button( 
    frame,
    text = "Submit",
    command = submit
)

submit.grid( row=0, column=0, pady = 4)

#check button method
def check():
    global frame, input_word
    input_word = entry.get()
    word = entry.get()


    obj = Project3(word)

    number_of_words = 5
    match_values = obj.get_most(number_of_words) 

    for loop in range(number_of_words):
        button = Button(
            frame,
            text=match_values[loop][2],
            command=lambda word_prop=match_values[loop]:words(word_prop)#to pass the word to the funciton words
        )
        button.grid( row = 2+loop, column=0, pady = 4)

check = Button( 
    frame,
    text = "Check",
    command = check
)
check.grid( row = 1, column = 0, pady = 4)


entry = Entry(frame)
entry.config( font=(50) )
entry.config( width=30 )
entry.grid( row = 0, column = 1, pady = 2)

frame.grid(row=0, column=0)

window.mainloop()



# import tkinter as tk
# from tkinter import Button, PhotoImage

# # Create the main window
# root = tk.Tk()
# root.title("Icon Button Demo")

# # Load the image
# icon = PhotoImage(file="icon.png")

# # Create a button with the image
# button = Button(root, image=icon, text="Click Me", compound="left", command=lambda: print("Button clicked!"))
# button.pack(pady=20)

# root.mainloop()