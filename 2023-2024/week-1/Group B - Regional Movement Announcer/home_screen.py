# import tkinter
# from turtle import Screen
# import project1 as project1

# screen = Screen()
# screen.setup(width=800, height=600)
# screen.bgcolor("#2E3548")


# def next_project():
#     tkinter.messagebox.showinfo("Next Project",  "Coming Soon...")

# def first_project():
#     obj = project1.Project1()
#     obj.run()

# canvas = screen.getcanvas()

# button = tkinter.Button(
#     background="#4A4D9E",
#     foreground="WHITE",
#     activebackground="#111111",
#     width=13,
#     height=2,
#     border=0,
#     cursor='hand1',
#     text="First Project",
#     font= ("Arial", 16, "bold"),
#     command=first_project)

# button2 = tkinter.Button(
#     background="#111111",
#     foreground="white",
#     activebackground="#111111",
#     width=13,
#     height=2,
#     border=0,
#     cursor='hand1',
#     text="Next Project",
#     font=("Arial", 16, "bold"),
#     command=next_project)

# button.pack()
# button.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)  # place the button anywhere on the screen

# button2.pack()
# button2.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

# canvas.itemconfig(screen._bgpic, anchor="n") #must be   n, ne, e, se, s, sw, w, nw, or center
# screen.bgpic("./images/ai.gif")

# screen.mainloop()

import sys 
sys.path.append('..') 

from turtle import Screen
from tkinter import *
from tkinter import messagebox
import project1

screen = Screen()
screen.setup(width=900, height=700)
screen.bgcolor("#2E3548")

index=0
image_list = [
    "./images/ai1.gif",
    "./images/ai2.gif",
]

def next_project():
    messagebox.showinfo("Next Project",  "Coming Soon...")

def first_project():
    global index
    obj = project1.Project1()
    obj.run()

    index =0
    screen.bgpic(image_list[index])

def second_project():
    global index
    index=1
    screen.bgpic(image_list[index])

canvas = screen.getcanvas()

button = Button(
    # canvas.master,
    background="#4A4D9E",
    foreground="WHITE",
    activebackground="#111111",
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text="First Project",
    font= ("Arial", 16, "bold"),
    command=first_project)

button2 = Button(
    background="#4A4D9E",
    foreground="WHITE",
    activebackground="#111111",
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text="Second Project",
    font=("Arial", 16, "bold"),
    command=second_project)

button_last = Button(
    background="#111111",
    foreground="white",
    activebackground="#111111",
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text="Coming Soon",
    font=("Arial", 16, "bold"),
    command=next_project)

button.pack()
button.place(relx=0.39, rely=0.1, anchor=CENTER)  # place the button anywhere on the screen
button2.pack()
button2.place(relx=0.61, rely=0.1, anchor=CENTER)

button_last.pack()
button_last.place(relx=0.5, rely=0.215, anchor=CENTER)

canvas.itemconfig(screen._bgpic, anchor="center") #must be   n, ne, e, se, s, sw, w, nw, or center
screen.bgpic(image_list[index])
screen.mainloop()