import numpy as np
import tkinter as tk

from tkinter import *
from PIL import Image
from PIL import ImageTk

# Global Variables to hold everything
results = False
last_tbw_value = 70
flagged_tbw_value = 0
avg_tbw_value = 70


# All functions for use
def calculate_bmi(height_m, weight):
    # BMI calculator taking in height and weight, returning BMI
    bmi = weight / height_m ** 2
    return bmi


def tbw_calc_bmi(ro, rinf, height_m, weight, bmi):
    # TBW calculator function taking in Ro and Rinf, height, weight and BMI for calculations
    # Return calculated values of TBW and TBW dived by weight
    height_cm = height_m * 100

    # Calculating the Extra Cellular Water using Ro
    re = ro
    kef = (0.188 / bmi) + 0.2883
    ecw = kef * ((((height_cm ** 2) * (np.sqrt(weight))) / re) ** (2 / 3))

    # Calculating the Intra Cellular Water using Rinf
    ri = np.abs(((1 / rinf) - (1 / ro)) ** (-1))
    kif = (5.875 / bmi) + 0.4194
    icw = kif * ((((height_cm ** 2) * (np.sqrt(weight))) / ri) ** (2 / 3))

    # Calculating the Total Body Water from the Extra and Intra Cellular Water
    tbw = ecw + icw
    tbw_weight = (tbw / weight) * 100
    return tbw_weight


def detection(new_value):
    detection_status = False

    old_value_adjust = last_tbw_value - (last_tbw_value * 0.02)
    if new_value <= old_value_adjust and new_value <= avg_tbw_value:
        detection_status = True

    return detection_status


def data_calc(raw_data_5k, raw_data_105k):
    height = 71.75
    weight = 147.4

    # Convert feet to meters
    height_m = (float(height)) / 39.37

    # convert lbs to kg
    weight_kg = (float(weight)) / 2.205

    # calculate BMI
    user_bmi = calculate_bmi(height_m, weight_kg)

    # Get the tbw and tbw with weight from 5k and 105k
    tbw_weight = tbw_calc_bmi(raw_data_105k, raw_data_5k, height_m, weight_kg, user_bmi)

    detection_status = detection(tbw_weight)

    return detection_status


# Below code taken from (https://www.geeksforgeeks.org/create-a-sideshow-application-in-python/)

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

    # Check to see if data is available
    data_available = True

    # If there is data perform analysis
    if data_available:
        file = open("detection.txt", "r")
        data_raw_5k = file.readline()
        data_raw_105k = file.readline()
        file.close()

        data_5k = int(data_raw_5k.strip())
        data_105k = int(data_raw_105k.strip())

        results = data_calc(data_5k, data_105k)

    # Display image according to results
    if not results:
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

    if results:
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
