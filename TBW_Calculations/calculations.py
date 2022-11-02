import numpy as np
import csv
from os.path import exists


def calculate_bmi(height_m, weight):
    # BMI calculator taking in height and weight, returning BMI
    bmi = weight / height_m ** 2
    return bmi


def calculate_avg(data):
    # Average calculator function taking in a list, returning the average
    total = 0
    for num in data:
        total += num
    avg = total / len(data)
    return avg


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
    return tbw, tbw_weight


def parse_impedance_file(path_to_file):
    # Parse function taking in file path locating the data based upon defined sections
    # Returns the resistance at the specific frequency
    with open(path_to_file) as raw_data:
        reader = csv.reader(raw_data)
        row = list(reader)

        freq_5k_string = row[5][3]
        freq_105k_string = row[105][3]
        freq_250k_string = row[250][3]

        freq_5k_int = int(freq_5k_string)
        freq_105k_int = int(freq_105k_string)
        freq_250k_int = int(freq_250k_string)

    return freq_5k_int, freq_105k_int, freq_250k_int


def file_reader(filepath):
    # Take in a filepath, read in the lines, then print them out
    calc_data = open(filepath, "r")
    lines = calc_data.readlines()
    for row in lines:
        print(row.strip())


def main():
    # Main function to take in files, calculate the data, write data to text file for analysis
    print("Enter exit at anytime to end program")
    user_name = input("Name: ").lower()
    if user_name == "exit":
        exit()
    date = input("Date (MM-DD-YY): ")
    if date == "exit":
        exit()
    height = input("Height[in]: ")
    if height == "exit":
        exit()
    weight = input("Weight[lbs]: ")
    if weight == "exit":
        exit()

    test_num = 1

    # Convert feet to meters
    height_m = (float(height)) / 39.37

    # convert lbs to kg
    weight_kg = (float(weight)) / 2.205

    # calculate BMI
    user_bmi = calculate_bmi(height_m, weight_kg)

    filepath = "../tbw_data/calc_data/"
    user_file = user_name + "_" + date + ".txt"

    # Check to ensure raw data is available
    checker_path = "../tbw_data/raw_data/" + user_name + "/test_1_" + date + ".csv"
    if exists(checker_path) is False:
        print("There is no available data in 'raw_data' folder, please enter test data results")
        checker = input("Would you like to try again? [Y/N] ").lower()
        if checker == "y":
            main()
        else:
            exit()

    # Create lists to hold data
    tbw_list_105 = []
    tbw_weight_list_105 = []

    tbw_list_250 = []
    tbw_weight_list_250 = []

    # grab the data then calculate the TBW and TBW with weight
    while test_num < 11:
        raw_data_filepath = "../tbw_data/raw_data/" + user_name + "/test_" + str(test_num) + "_" + date + ".csv"
        freq_5k, freq_105k, freq_250k = parse_impedance_file(raw_data_filepath)

        # Get the tbw and tbw with weight from 5k and 105k
        tbw_105, tbw_weight_105 = tbw_calc_bmi(freq_105k, freq_5k, height_m, weight_kg, user_bmi)
        tbw_list_105.append(tbw_105)
        tbw_weight_list_105.append(tbw_weight_105)

        # Get the tbw and tbw with weight from 5k and 250k
        tbw_250, tbw_weight_250 = tbw_calc_bmi(freq_250k, freq_5k, height_m, weight_kg, user_bmi)
        tbw_list_250.append(tbw_250)
        tbw_weight_list_250.append(tbw_weight_250)

        test_num += 1

    # calculate the average from both of the lists
    avg_tbw_105 = calculate_avg(tbw_list_105)
    avg_tbw_weight_105 = calculate_avg(tbw_weight_list_105)
    avg_tbw_250 = calculate_avg(tbw_list_250)
    avg_tbw_weight_250 = calculate_avg(tbw_weight_list_250)

    # Open the file and begin to write user info and their data to it
    with open(filepath + user_file, "w") as tbw_data:
        # Write preliminary data about the user
        tbw_data.write("name:" + user_name + "\n" + "date:" + date + "\n")
        tbw_data.write("weight[kg]:" + str(weight_kg) + "\n" + "height[m]:" + str(height_m) + "\n\n")

        # Write the data for 5K and 105K
        tbw_data.write("5K and 105K" + "\n" + "TBW:\n")
        counter = 1
        for num in tbw_list_105:
            tbw_data.write("test" + str(counter) + " TBW:" + str(num) + "\n")
            counter += 1
        tbw_data.write("Avg:" + str(avg_tbw_105) + "\n\n" + "TBW with weight:\n")

        counter = 1
        for num in tbw_weight_list_105:
            tbw_data.write("test" + str(counter) + " TBW/Weight:" + str(num) + "\n")
            counter += 1
        tbw_data.write("Avg:" + str(avg_tbw_weight_105) + "\n\n")

        # Write the data for 5K and 250K
        tbw_data.write("5K and 250K" + "\n" + "TBW:\n")
        counter = 1
        for num in tbw_list_250:
            tbw_data.write("test " + str(counter) + ": " + str(num) + "\n")
            counter += 1
        tbw_data.write("Avg:" + str(avg_tbw_250) + "\n\n" + "TBW with weight:\n")

        counter = 1
        for num in tbw_weight_list_250:
            tbw_data.write("test" + str(counter) + " TBW/Weight:" + str(num) + "\n")
            counter += 1
        tbw_data.write("Avg:" + str(avg_tbw_weight_250) + "\n")

        tbw_data.close()

        file_reader(filepath + user_file)


main()
#tbw, tbw_weight = tbw_calc_bmi(-2988.81, 2997, 1.778, 74.03, 23.416)
#print(tbw)
#print(tbw_weight)
