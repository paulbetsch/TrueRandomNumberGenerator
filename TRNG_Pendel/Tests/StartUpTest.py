from math import fabs as fabs
from math import sqrt as sqrt
from scipy.special import erfc as erfc

def __contains_only_true(self, lst):
    return all(element is True for element in lst)

def StartUpTest(binary_String):
    binary_array = [int(x) for x in binary_String]
    
    if(__test_monobit(binary_array) and __poker_test(binary_array) and __boolean_test3(binary_array)):
        return True
    else:
        return False

def __test_monobit(self, binary_String):
    """
    Implements the Monobit Test on 20,000 bits sequences of a text file.
    Input:
        bits: an array with the bits as integers from the txt input file.
    Description and Evaluation rule:
        The Monobit Test is passed when the sum of all bits is in the interval [9654;10346]. Otherwise it failed.
    """
    lastPosition = 0
    results =[]
    trueCounter = 0

    while(lastPosition+20000 <= len(binary_String)):
        T1 = sum(binary_String[lastPosition:20000+lastPosition])

        if 9654 < T1 < 10346:
            results.append(True)
        else:
            results.append(False)
        lastPosition += 20000
    
    if(__contains_only_true(results)):
        return True
    else: 
        return False

def __poker_test(binary_array):
    """
    Implements the Poker Test on 20,000 bits sequences of a text file.
    Input:
        binary_array: an array with the bits as integers from the txt input file.
    Description and Evaluation rule:
        The Poker Test is passed when T2 is in the interval [1.03;57.4]. Otherwise it failed.
        It checks the occurences of 4-bit patterns.
    """
    lastPosition = 0
    results =[]
    trueCounter = 0

    while(lastPosition+20000 <= len(binary_array)):
        bit_sequence = binary_array[lastPosition:lastPosition+20000]
        f = [0] * 16

        for j in range(5000):
            c_j = 8*bit_sequence[4*j] + 4*bit_sequence[4*j+1] + \
                2*bit_sequence[4*j+2] + bit_sequence[4*j+3]
            f[c_j] += 1

        # Calculate T_2 using the formula given in the requirements
        T_2 = (16/5000) * sum([freq**2 for freq in f]) - 5000

        # Check if the sequence passes the test
        if 1.03 < T_2 < 57.4:
            results.append(True)
        else:
            results.append(False)
        lastPosition += 20000
    
    if(__contains_only_true(results)):
        return True
    else: 
        return False

def __boolean_test3(binary_array):
    """
    Implements the Runs Test on 20,000 bits sequences of a text file.
    Input:
        binary_array: an array with the bits as integers from the txt input file.
    Description and Evaluation rule:
        The Runs Test is passed when the runs for specific lengths are in a defined interval. Otherwise it failed.
        A run is defined as a consecutive sequence of the same number.
    """
    lastPosition = 1
    results =[]
    trueCounter = 0
    bitfieldB = binary_array
    lowerBound = [0, 2267, 1079, 502, 223, 90, 90]
    upperBound = [0, 2733, 1421, 748, 402, 223, 223]
    run = 1

    while(lastPosition+20000 <= len(binary_array)):
        run0field = [0] * 7
        run1field = [0] * 7
        for i in range(lastPosition, lastPosition+20000):
            if bitfieldB[i-1] == bitfieldB[i]:
                run += 1
            else:
                if run > 6:
                    run = 6
                if bitfieldB[i-1] == 1:
                    run1field[run] += 1
                else:
                    run0field[run] += 1
                run = 1
        if run > 6:
            run = 6
        if bitfieldB[i-1] == 1:
            run1field[run] += 1
        else:
            run0field[run] += 1
        for i in range(1, 7):
            if lowerBound[i] <= run0field[i] <= upperBound[i]:
                results.append(True)
            else:
                results.append(False)

            if lowerBound[i] <= run1field[i] <= upperBound[i]:
                results.append(True)
            else:
                results.append(False)
        lastPosition += 20000
    if(__contains_only_true(results)):
        return True
    else: 
        return False
