import tkinter as tk

from tkinter import *
from PIL import Image
from PIL import ImageTk

# Code taken from (https://www.geeksforgeeks.org/create-a-sideshow-application-in-python/)

# Adjust window
root = tk.Tk()
root.geometry("200x200")

# Loading the images
img = ImageTk.PhotoImage(Image.open("Pictures/Normal/norm1.jpg"))
img2 = ImageTk.PhotoImage(Image.open("Pictures/Normal/norm2.jpg"))
img3 = ImageTk.PhotoImage(Image.open("Pictures/Normal/norm3.jpg"))
img4 = ImageTk.PhotoImage(Image.open("Pictures/Normal/norm4.jpg"))
img5 = ImageTk.PhotoImage(Image.open("Pictures/Normal/norm5.jpg"))

de_img = ImageTk.PhotoImage(Image.open("Pictures/Dehydrated/de1.jpg"))
de_img2 = ImageTk.PhotoImage(Image.open("Pictures/Dehydrated/de2.jpg"))
de_img3 = ImageTk.PhotoImage(Image.open("Pictures/Dehydrated/de3.jpg"))
de_img4 = ImageTk.PhotoImage(Image.open("Pictures/Dehydrated/de4.jpg"))
de_img5 = ImageTk.PhotoImage(Image.open("Pictures/Dehydrated/de5.jpg"))

l = Label()
l.pack()

# Using recursion to slide to next image
x = 1


# function to change to next image
def move():
    file = open("detection.txt", "r")
    results = file.read()
    file.close()

    if results == "False":
        global x
        if x == 6:
            x = 1
        if x == 1:
            l.config(image=img)
        elif x == 2:
            l.config(image=img2)
        elif x == 3:
            l.config(image=img3)
        elif x == 4:
            l.config(image=img4)
        elif x == 5:
            l.config(image=img5)
        x = x + 1

    if results == "True":
        if x == 6:
            x = 1
        if x == 1:
            l.config(image=de_img)
        elif x == 2:
            l.config(image=de_img2)
        elif x == 3:
            l.config(image=de_img3)
        elif x == 4:
            l.config(image=de_img4)
        elif x == 5:
            l.config(image=de_img5)
        x = x + 1

    root.after(3000, move)


# Calling the function
move()

root.mainloop()
