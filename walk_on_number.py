# COMP1730/6730 Project-1.
# YOUR ANU ID: u7560547
# YOUR NAME: Yanin Wongtharua
import decimal as d
import matplotlib.pyplot as plt
import math
# Question 1: Define a function which accepts a 2-tuple comprising a numerator and a
# denominator, and a base of the numeral system in which to expand the rational
# number, and returns the period of the expansion sequence.
def expansion_sequence(fraction, base, n_steps):
    """function accepts a 2-tuple of numerator and denominator, a base of numeral system and number of steps"""
    d.getcontext().prec = n_steps #use n_steps as a benchmark
    remainders_dict = {} # store remainders in dict to detect repeating remainders
    decimal = "0."
    remainder = fraction[0] % fraction[1]
    rational_number = d.Decimal(fraction[0])/d.Decimal(fraction[1])
    if base == 10: # case 1 base 10
        while remainder not in remainders_dict:
            remainders_dict[remainder] = len(decimal)
            quotient = remainder * 10 // fraction[1]
            remainder = remainder * 10 % fraction[1]
            decimal += str(quotient)
        period = len(decimal) - remainders_dict[remainder] # when remainder is already added in the dict, the length of decimal is subtracted by position of the repeated place value
        return str(rational_number), period # return rational number in base 10 (first element in tuple) and period (second element in tuple)
    else: # case 2 other bases, by converting from base10 into desired base       
        while round(rational_number, 15) not in remainders_dict: # round the ratinal number to 15th decimal place to get accurate result
            remainders_dict[round(rational_number, 15)] = len(remainders_dict)
            full_rational_number = (rational_number * base) # multiply base10 value by desired base
            rational_number = full_rational_number - int(full_rational_number) # get the integer part
            decimal += str(int(full_rational_number)) # create the decimal in desired base by combining previous integer
        period = len(decimal) - remainders_dict[round(rational_number, 15)] - 2 # same as base 10 case, also subtracted by 2 (the length of new rational number includes '0.')

        while len(decimal) - 2 < n_steps: # repeatly generate repeating decimal until reach number of steps
            remainders_dict[round(full_rational_number, 15)] = len(remainders_dict) + 2
            full_rational_number = (rational_number * base)
            rational_number = full_rational_number - int(rational_number * base)
            decimal += str(int(full_rational_number))
        return decimal, period # return rational number in desired base (first element in tuple) and period (second element in tuple)
# Question 2: Define a function which accepts a 2-tuple of integers, a numerator and denominator representing a rational number, the base value and the positive integer
# nsteps, and returns the sequence of the expansion digits of this rational of the
# total length nsteps.
def find_sequence(fraction, base, n_steps):
    """function accepts a 2-tuple of numerator and denominator, a base of numeral system"""
    decimal_sequence = expansion_sequence(fraction, base, n_steps)[0] # use the new_rational_number result from expansion_sequence function
    expansion_list = [] # store the sequence in expansion list
    new_decimal_sequence = decimal_sequence[2:] + ("0" * (n_steps -  int(len(decimal_sequence[2:])))) # 1.do a list slicing to get decimal digits(decimal contains '0.'), 2.if length of decimal_sequence doesn't equal to number of steps, add zeros
    for i in new_decimal_sequence:
        expansion_list.append(int(i))
    return expansion_list 
# Question 3: Using the plotting library matplotlib, create a walk which a rational (defined
# by a 2-tuple of integers) generates on a square lattice.
def create_walk(fraction, base, n_steps):
    """function accepts a 2-tuple of numerator and denominator, a base of numeral system and number of steps"""
    # directions is {0: "East", 1: "North", 2: "West", 3: "South"}
    sequence = find_sequence(fraction, base, n_steps)
    x = 0 # starting point of x-coordinate
    y = 0 # starting point of y-coordinate
    x_coordinates = [x] 
    y_coordinates = [y]
    cmap = plt.cm.get_cmap("jet") # plot the scatter plot where the "jet" color defines the steps on the plane, starting from navy to red
    for i in sequence:
        if i == 0:
            x += 1 # x coordinate moves to the right when the sequence is 0
        elif i == 1:
            y += 1 # y coordinate moves up when the sequence is 1
        elif i == 2:
            x -= 1 # x coordinate moves to the left when the sequence is 2
        elif i == 3:
            y -= 1 # y coordinate moves down when the sequence is 3
        x_coordinates.append(x) 
        y_coordinates.append(y)
    plt.title(f"{fraction[0]}-{fraction[1]} Walk, n_steps = {n_steps}")
    plt.scatter(x_coordinates, y_coordinates, c=range(len(x_coordinates)), cmap=cmap, s=50)
    plt.show()
# Question 4: Write a function that is passed a sequence prefix, a sequence period and
# a base b, which will return a 2-tuple of mutually prime integers to uniquely
# represent a rational
def find_rational_number(prefix, period_sequence, base, n_steps):
    """function accepts prefix and period sequence that are tuple, a base of numeral system and number of steps"""
    # See more information about cases on memo
    decimal_of_sequence = "0."        
    if prefix == () and sum(period_sequence) == 0: # case 5, all digits are zero
        return 0
    elif sum(prefix) == 0 and sum(period_sequence) == 0: # case 6, all digits are zero
        return 0
    elif prefix != () or period_sequence != (0, ): # case 1,2,3,4 appending prefix and period sequence
        for i in range(0, len(prefix)):
            decimal_of_sequence += (str(prefix[i]))
        while len(decimal_of_sequence) - 2 < n_steps:
            for i in range(0, len(period_sequence)):
                decimal_of_sequence += (str(period_sequence[i]))
    
    # convert decimal to get only repeated decimals of case 1,2,3,4
    new_decimal_of_sequence = d.Decimal(decimal_of_sequence)
    if prefix != (): # case 1,3,4 when prefix is not an empty sequence, multiplied by prefix sequence to convert to repeating decimal without prefix
        new_decimal_of_sequence = new_decimal_of_sequence * (10 ** len(prefix))
    else: # case 2, when prefix is an empty sequence, multiplied by period sequence to convert to repeating decimal 
        new_decimal_of_sequence = new_decimal_of_sequence * (10 ** len(period_sequence))
    
    #Convert decimal number to fraction
    if prefix != () and sum(period_sequence) == 0: # find numerator and denominator of case 4
        numerator = int(new_decimal_of_sequence)
        denominator = (10 ** len(prefix)) # period consists of zero
    else: 
        period_dict = {}
        decimal_place = 1
        if prefix == () and sum(period_sequence) != 0: # find sequence of case2
            for digit in str(new_decimal_of_sequence)[len(period_sequence) + 1:]: # number 1 is the length of "." 
                while digit not in period_dict:
                    period_dict[digit] = decimal_place
                    decimal_place += 1
            sequence = len(period_dict)
        elif sum(prefix) == 0 and sum(period_sequence) != 0: # find sequence of case3
            for digit in str(new_decimal_of_sequence)[len(period_sequence) + 2:]: # number 2 is the length of "0." 
                while digit not in period_dict:
                    period_dict[digit] = decimal_place
                    decimal_place += 1
            sequence = len(period_dict)
        else: # find sequence of case1
            for digit in str(new_decimal_of_sequence)[len(prefix) + 1:]: # number 1 is the length of "."
                while digit not in period_dict:
                    period_dict[digit] = decimal_place
                    decimal_place += 1
            sequence = len(period_dict)

        # find numerator and denominator of case 1,2,3
        if prefix == () and sum(period_sequence) != 0: # case2
            numerator = round(new_decimal_of_sequence - d.Decimal(decimal_of_sequence))
            denominator = int("9" * len(period_sequence))
        elif sum(prefix) == 0 and sum(period_sequence) != 0: # case3
            multiplied_decimal_of_sequence = (new_decimal_of_sequence * (10 ** sequence))
            numerator = int(multiplied_decimal_of_sequence - new_decimal_of_sequence)
            denominator = int(("9" * len(period_sequence)) + ("0" * len(prefix)))
        else: # case 1
            multiplied_decimal_of_sequence = (new_decimal_of_sequence * (10 ** sequence))
            numerator = int(multiplied_decimal_of_sequence - new_decimal_of_sequence)
            denominator = int("9" * sequence)
            while denominator < numerator:
                denominator *= 10
    
    # find greatest common divisor)   
    gcd = find_GCD(numerator, denominator)
    rational_number = (numerator // gcd, denominator // gcd)
    return rational_number # the first element in tuple is numerator, the second element in tuple is denominator

def find_GCD(numerator, denominator):
    """function accepts numerator and denominator to return GCD"""
    GCD = math.gcd(numerator, denominator)
    return GCD
# Question 5:  Compute rationals which generate sample walk
def rationals_from_sample_walk():
    """function accepts an input from user to select a sample walk"""
    choose_sample = input("Choose sample walk (6x6 Square, Letter T, Heart): ")
    directions = [] # base4 directions: {0: "East", 1: "North", 2: "West", 3: "South"}
    if choose_sample == "6x6 Square":
        x, y = -3, 3 # starting point
        x_coordinates, y_coordinates = [-3], [3]
        cmap = plt.cm.get_cmap("jet")
        for i in range(1, 25): # n_steps = 24 and the code below is the walking direction of a "6x6 Square" picture
            if i < 7:
                x += 1
                directions.append(0)
            elif i < 13:
                y -= 1
                directions.append(3)
            elif i < 19:
                x -= 1
                directions.append(2)
            elif i < 25:
                y += 1
                directions.append(1)
            x_coordinates.append(x)
            y_coordinates.append(y)
    elif choose_sample == "Letter T":
        x, y = -1, 0 # starting point
        x_coordinates, y_coordinates = [-1], [0]
        cmap = plt.cm.get_cmap("jet")
        for i in range(1, 25): # n_steps = 24 and the code below is the walking direction of a "Letter T" picture
            if i < 3:
                x += 1
                directions.append(0)
            elif i < 7:
                y += 1
                directions.append(1)
            elif i < 9:
                x += 1
                directions.append(0)
            elif i < 11:
                y += 1
                directions.append(1)
            elif i < 17:
                x -= 1
                directions.append(2)
            elif i < 19:
                y -= 1
                directions.append(3)
            elif i < 21:
                x += 1
                directions.append(0)
            elif i < 25:
                y -= 1
                directions.append(3)
            x_coordinates.append(x)
            y_coordinates.append(y)
    elif choose_sample == "Heart":
        x, y = 0, 0 # starting point
        x_coordinates, y_coordinates = [0], [0]
        cmap = plt.cm.get_cmap("jet")
        for i in range(1, 25): # n_steps = 24 and the code below is the walking direction of a "Heart" picture
            if i < 5:
                y += 1 if i % 2 != 0 else 0
                x += 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(1)
                else:
                    directions.append(0)
            elif i < 8:
                x -= 1 if i % 2 != 0 else 0
                y -= 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(2)
                else:
                    directions.append(3)
            elif i < 11:
                y += 1 if i % 2 == 0 else 0
                x += 1 if i % 2 != 0 else 0
                if i % 2 == 0:
                    directions.append(1)
                else:
                    directions.append(0)                
            elif i < 13:
                y -= 1 if i % 2 != 0 else 0
                x -= 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(3)
                else:
                    directions.append(2)
            elif i < 15:
                x -= 1 if i % 2 != 0 else 0
                y += 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(2)
                else:
                    directions.append(1)
            elif i < 18:
                y -= 1 if i % 2 != 0 else 0
                x += 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(3)
                else:
                    directions.append(0)
            elif i < 21:
                x -= 1 if i % 2 == 0 else 0
                y += 1 if i % 2 != 0 else 0
                if i % 2 == 0:
                    directions.append(2)
                else:
                    directions.append(1)
            elif i < 25:
                x += 1 if i % 2 != 0 else 0
                y -= 1 if i % 2 == 0 else 0
                if i % 2 != 0:
                    directions.append(0)
                else:
                    directions.append(3)
            x_coordinates.append(x)
            y_coordinates.append(y)    
    plt.title(f"{choose_sample}, n_steps = 24")
    plt.scatter(x_coordinates, y_coordinates, c=range(len(x_coordinates)), cmap=cmap, s=50)
    plt.show()
    #convert base4 to decimal base10 to generate fraction    
    decimal_direction = 0
    i = 1
    base = 4
    for direction in directions:
        decimal_direction += (direction / (base ** i)) # keep summing until i = 24 (n_steps or len(directions))
        i += 1
    numerator = int(decimal_direction * (10 ** (len(str(decimal_direction)) - 2))) # number 2 is the length of "0."
    denominator = 10 ** (len(str(decimal_direction)) - 2) # number 2 is the length of "0."
    return numerator, denominator 
 
def find_fraction():
    """function use the value from rationals_from_sample_walk and find_GCD functions to return GCD"""
    numerator, denominator = rationals_from_sample_walk()
    GCD = find_GCD(numerator, denominator)
    rational_number = (numerator // GCD, denominator // GCD)
    return rational_number # the first element in tuple is numerator, the second element in tuple is denominator             

if __name__ == "__main__": # execute the code from question 1 to question 5
      print(expansion_sequence(fraction = (7, 11), base = 10, n_steps = 100)) # user can change the fraction, base, n_steps
      print(find_sequence(fraction = (7, 11), base = 4, n_steps = 100)) # user can change the fraction, base, n_steps
      print(create_walk(fraction = (7, 11), base = 4, n_steps = 100)) # user can change the fraction, base, n_steps
      print(find_rational_number(prefix = (1,1), period_sequence = (3,), base = 10, n_steps = 100)) # user can change prefix (could be () or (0,)) period_sequence (could be () or (0,)) and n_steps
      print(find_fraction())


