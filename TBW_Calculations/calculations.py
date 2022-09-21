import math

def calculate_bmi(height_m, weight):
    bmi = weight / height_m ** 2
    return bmi

def tbw_calc(ro, rinf, height_cm, weight, bmi):
    re = ro
    kef = (0.188/bmi) + 0.2883
    ecw = kef * (((height_cm ** 2) * (math.sqrt(weight)))/re) ** (2/3)

    ri = ((1/rinf) - (1/ro)) ** (-1)
    kif = (5.875/bmi) + 0.4194
    icw = kif * (((height_cm ** 2) * (math.sqrt(weight)))/ri) ** (2/3)

    tbw = ecw + icw
    tbw_weight = (tbw/weight) * 100
    return tbw, tbw_weight


def collect_info():
    user_name = input("Name: ").title()
    height_stft = input("Height: ")
    weight_stlbs = input("Weight: ")
    ro_string = input("Ro: ")
    rinf_string = input("Rinf: ")

    height_ft = float(height_stft)
    weight_lbs = float(weight_stlbs)
    ro = float(ro_string)
    rinf = float(rinf_string)

    height_cm = height_ft * 30.48
    height_m = height_cm / 100
    weight_kg = weight_lbs * 0.45359237

    bmi = calculate_bmi(height_m, weight_kg)
    tbw, tbw_weight = tbw_calc(ro, rinf, height_cm, weight_kg, bmi)
    inverse_tbw, inverse_tbw_weight = tbw_calc(rinf, ro, height_cm, weight_kg, bmi)

    print("Total Body Water: " + str(tbw) + " Total Body with weight: " + str(tbw_weight))
    print("Inverse Total Body Water: " + str(inverse_tbw) + " Inverse Total Body with weight: " + str(inverse_tbw_weight))

def tester():
    height_cm = 172
    height_m = height_cm / 100
    weight_kg = 82.1
    ro = 412
    rinf = 1083



    bmi = calculate_bmi(height_m, weight_kg)
    tbw, tbw_weight = tbw_calc(ro, rinf, height_cm, weight_kg, bmi)
    inverse_tbw, inverse_tbw_weight = tbw_calc(rinf, ro, height_cm, weight_kg, bmi)

    print("Total Body Water: " + str(tbw) + " Total Body with weight: " + str(tbw_weight))
    print("Inverse Total Body Water: " + str(inverse_tbw) + " Inverse Total Body with weight: " + str(inverse_tbw_weight))

tester()
