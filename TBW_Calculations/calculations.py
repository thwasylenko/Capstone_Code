import numpy as np
import csv

def calculate_bmi(height_m, weight):
    bmi = weight / height_m ** 2
    return bmi

def tbw_calc_bmi(ro, rinf, height_m, weight, bmi):
    height_cm = height_m * 100

    re = ro
    kef = (0.188 / bmi) + 0.2883
    ecw = kef * ((((height_cm ** 2) * (np.sqrt(weight))) / re) ** (2 / 3))

    ri = np.abs(((1 / rinf) - (1 / ro)) ** (-1))
    kif = (5.875 / bmi) + 0.4194
    icw = kif * ((((height_cm ** 2) * (np.sqrt(weight))) / ri) ** (2 / 3))

    tbw = ecw + icw
    tbw_weight = (tbw / weight) * 100
    return tbw, tbw_weight

def tbw_calc_bis(ro, rinf, height_cm, weight, gender):
    re = ro
    ri = np.abs(((1 / rinf) - (1 / ro)) ** (-1))
    kb = 4.3
    db = 0.00105
    pe = 0
    pi = 0
    if (gender == "male"):
        pe = 40.5
        pi = 273.9
    else:
        pe = 39
        pi = 264.9

    ecw = (1/1000)*((((kb**2)*(pe**2))/db)**(1/3))*((((np.sqrt(weight))*(height_cm**2))/re)**(2/3))
    icw = (1/1000)*((((kb**2)*(pe**2))/db)**(1/3))*((((np.sqrt(weight))*(height_cm**2))/re)**(2/3))

    tbw = ecw + icw
    tbw_weight = (tbw / weight) * 100
    return tbw, tbw_weight


def parse_impedance_file(path_to_file):

    with open(path_to_file) as raw_data:
        reader = csv.reader(raw_data)
        row = list(reader)

        freq_5k_string = row[5][3]
        freq_105k_string = row[105][3]
        freq_250k_string = row[250][3]

        freq_5k_int = int(freq_5k_string)
        freq_105k_int = int(freq_105k_string)
        #freq_250k_int = int(freq_250k_string)

    return freq_5k_int, freq_105k_int, #freq_250k_int

def main():
    user_name = input("Name: ").lower()
    date = input("Date (MM-DD-YY): ")
    height = input("Height: ")
    weight = input("Weight: ")
    test_num = 1
    user_bmi = calculate_bmi(float(height), float(weight))
    filepath = "../tbw_data/calc_data/"
    user_file = user_name + "_" + date + ".txt"
    #raw_data_filepath = "../tbw_data/raw_data/test_" + test_num + "_" + date

    tbw_list = []
    tbw_weight_list = []


    while test_num < 11:
        raw_data_filepath = "../tbw_data/raw_data/"+ user_name +"/test_" + str(test_num) + "_" + date + ".csv"
        freq_5k, freq_105k, freq_250k = parse_impedance_file(raw_data_filepath)
        tbw, tbw_weight = tbw_calc_bmi(freq_105k, freq_5k,float(height), float(weight), user_bmi)
        tbw_list.append(tbw)
        tbw_weight_list.append(tbw_weight)

        test_num += 1

    sum_tbw = 0
    sum_tbw_weight = 0
    for num1 in tbw_list:
        sum_tbw += num1
    for num2 in tbw_weight_list:
        sum_tbw_weight += num2
    avg_tbw = sum_tbw / 10
    avg_tbw_weight = sum_tbw_weight / 10

    with open(filepath + user_file, "w") as tbw_data:
        tbw_data.write("name:" + user_name + "\n")
        tbw_data.write("TBW:\n")
        counter = 1
        for num in tbw_list:
            tbw_data.write("test" + str(counter) + " TBW:" + str(num) + "\n")
            counter += 1
        tbw_data.write("Avg:" + str(avg_tbw) + "\n\n")
        tbw_data.write("TBW with weight:\n")
        counter2 = 1
        for num2 in tbw_weight_list:
            tbw_data.write("test" + str(counter2) + " TBW/Weight:" + str(num2) + "\n")
            counter2 += 1
        tbw_data.write("Avg:" + str(avg_tbw_weight) + "\n")

        tbw_data.close()


main()