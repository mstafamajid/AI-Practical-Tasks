from tkinter import *
from app import Project3

window = Tk()
window.geometry("800x500")

frame = Frame(window)
frame.pack()

table = None
input_word = ""  # is the input word
selected_word = None
array_of_buttons = []

# Create a list to keep track of the buttons
for _ in range(5):
    array_of_buttons.append(Button(frame))

# Five words button method
def words(word):
    global selected_word
    entry.delete(0, 'end')
    entry.insert(0, word[2])
    selected_word = word


def submit():
    global input_word, selected_word

    word = selected_word

    window2 = Tk()
    window2.geometry("800x500")

    frame2 = Frame(window2)
    frame2.config(width=100, height=100)

    input = input_word
    input_length = len(input)
    input_count = 0

    # Constants
    TABLE_WIDTH = 2
    TABLE_HEIGHT = 1
    BG_COLOR = "white"
    FG_COLOR = "blue"

    table_frame = frame2

    for column in range(len(word[3][0])):
        if column == 1:
            create_text_widget(table_frame, 0, 1, TABLE_WIDTH, TABLE_HEIGHT, '0', BG_COLOR, FG_COLOR)
            counter_grid = 1
            for loopChar in range(len(word[2])):
                create_text_widget(table_frame, 0, counter_grid + 1, TABLE_WIDTH, TABLE_HEIGHT, word[2][loopChar], BG_COLOR, FG_COLOR)
                counter_grid += 1

    for row in range(len(word[3])):
        if row == 0:
            create_text_widget(table_frame, 0, 1, TABLE_WIDTH, TABLE_HEIGHT, '0', BG_COLOR, FG_COLOR)
        else:
            create_text_widget(table_frame, row + 1, 0, TABLE_WIDTH, TABLE_HEIGHT, '0', BG_COLOR, FG_COLOR)
            if input_count < input_length:
                create_text_widget(table_frame, row + 1, 0, TABLE_WIDTH, TABLE_HEIGHT, input[input_count], BG_COLOR, FG_COLOR)
                input_count += 1

        for column in range(len(word[3][0])):
            create_text_widget(table_frame, row + 1, column + 1, 3, 1, word[3][row][column], "black", "white")
           

    
    # to indicate the arrows
    row, column = len(word[3]) - 1, len(word[3][1]) - 1
    while row > 0 and column > 0:
                if word[3][row - 1][column] == word[3][row][column - 1] and input_word[row - 1] == word[2][column - 1]:
                    create_text_widget(table_frame, row + 1, column + 1, 3, 1, word[3][row][column], "green", "white")
                    row -= 1
                    column -= 1
                elif word[3][row - 1][column] > word[3][row][column - 1]:
                    create_text_widget(table_frame, row + 1, column + 1, 3, 1, word[3][row][column], "green", "white")
                    row -= 1
                else:
                    create_text_widget(table_frame, row + 1, column + 1, 3, 1, word[3][row][column], "green", "white")
                    column -= 1

                if word[3][row][column] == 0:
                    create_text_widget(table_frame, row + 1, column + 1, 3, 1, word[3][row][column], "green", "white")
                    break
    

    frame3 = Frame(window2)
    table = Text(frame3, wrap=CHAR,  bg="black", fg="white")
    table.config(font=15)
    table.tag_config('center', justify='center')
    table.insert(INSERT, f"The number of matcher words are {word[4][::-1]}")
    table.pack()

    frame2.pack()
    frame3.pack()




def create_text_widget(frame, row, column, width, height, text, bg, fg):
    table = Text(frame, width=width, height=height, bg=bg, fg=fg)
    table.config(font=15)
    table.tag_config('center', justify='center')
    table.grid(row=row, column=column)
    table.insert(INSERT, text)



# Check button method
def check():
    global frame, input_word, array_of_buttons
    input_word = entry.get()
    word = entry.get()

    obj = Project3(word)

    number_of_words = 5
    match_values = obj.get_most(number_of_words)

    # Destroy the old buttons if they exist
    for button in array_of_buttons:
        button.destroy()

    # Create and add new buttons to the list and display them
    for loop in range(number_of_words):
        array_of_buttons[loop] = Button(
            frame,
            text=match_values[loop][2],
            command=lambda word_prop=match_values[loop]: words(word_prop),
            font=15
        )
        array_of_buttons[loop].grid(row=2 + loop, column=0, pady=4)

    # Add the "Submit" button back to the frame
    submit_button = Button(frame, text="Submit", command=submit, font=15)
    submit_button.grid(row=0, column=0, pady=4)

check_button = Button(
    frame,
    text="Check",
    command=check,
    font=15
)
check_button.grid(row=1, column=0, pady=4)

entry = Entry(frame)
entry.config(font=(50))
entry.config(width=30)
entry.grid(row=0, column=1, pady=2)

frame.grid(row=0, column=0)

window.mainloop()