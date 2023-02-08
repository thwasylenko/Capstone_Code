import numpy as np


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

def impedance_data():
    freq_5k = 5
    freq_105k = 5
    return freq_5k, freq_105k


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
    # Open data file and save the value for detection
    file = open("data_save.txt", "r")
    value_txt = file.read()
    file.close()

    file2 = open("avg_value.txt", "r")
    avg_value = float(file2.read())
    file2.close()

    old_value = float(value_txt)
    old_value_adjust = old_value - (old_value * 0.05)
    if new_value <= old_value_adjust and new_value <= avg_value:
        detection_status = True

    return detection_status


def main():
    test_num = 1
    test_amount = 10
    height = 5
    weight = 5

    # Convert feet to meters
    height_m = (float(height)) / 39.37

    # convert lbs to kg
    weight_kg = (float(weight)) / 2.205

    # calculate BMI
    user_bmi = calculate_bmi(height_m, weight_kg)

    # Create lists to hold data
    tbw_list_105 = []
    tbw_weight_list_105 = []

    # grab the data then calculate the TBW and TBW with weight
    while test_num <= test_amount:
        freq_5k, freq_105k = impedance_data()

        # Get the tbw and tbw with weight from 5k and 105k
        tbw_105, tbw_weight_105 = tbw_calc_bmi(freq_105k, freq_5k, height_m, weight_kg, user_bmi)
        tbw_list_105.append(tbw_105)
        tbw_weight_list_105.append(tbw_weight_105)

        test_num += 1

    # calculate the average from both of the lists
    avg_tbw_weight_105 = calculate_avg(tbw_weight_list_105)

    results = detection(avg_tbw_weight_105)

    # Write to a file to keep track of tbw value
    file = open("data_save.txt", "w")
    file.write(str(avg_tbw_weight_105))
    file.close()

    return results
