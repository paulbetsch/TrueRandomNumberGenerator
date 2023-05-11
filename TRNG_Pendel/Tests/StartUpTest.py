from math import fabs as fabs
from math import sqrt as sqrt
from scipy import stats
from scipy.special import erfc as erfc

def __contains_only_true(self, lst):
    return all(element is True for element in lst)

def StartUpTest(binary_String):
    binary_array = [int(x) for x in binary_String]
    #TODO: Test the tests and update to ensure 128 Bit array
    if(__test_monobit(binary_array) and __chi2_gof_test(binary_array)):
        return True
    else:
        return False

def __test_monobit(self, binary_String):
    """
    Implements the Monobit Test.
    Input:
        bits: an array with the bits as integers.
    Description and Evaluation rule:
        The Monobit Test is passed when the sum of all bits is in the interval [9654;10346]. Otherwise it failed.
    """
    length_of_bit_string = len(binary_String)

    # Variable for S(n)
    count = 0
    # Iterate each bit in the string and compute for S(n)
    for bit in binary_String:
        if bit == 0:
            # If bit is 0, then -1 from the S(n)
            count -= 1
        elif bit == 1:
            # If bit is 1, then +1 to the S(n)
            count += 1

    # Compute the test statistic
    sObs = count / sqrt(length_of_bit_string)

    # Compute p-Value
    p_value = erfc(fabs(sObs) / sqrt(2))

    # return a p_value
    return p_value >= 0.01



def __chi2_gof_test(self, binary_array):
    """
    Implements a chi-squared goodness of fit test on a binary array.
    Input:
        bits: an array with the bits as integers.
    Description and Evaluation rule:
        The Test is passed when the P-Value is smaller than 1.0. Otherwise it failed.
    """
    # Define the expected frequencies assuming a discrete uniform distribution
    n = len(binary_array)
    expected_freq = [n/2]*2

    # Count the observed frequencies
    observed_freq = [binary_array.count(0), binary_array.count(1)]

    # Perform the chi-squared goodness of fit test
    testStat, pValue = stats.chisquare(observed_freq, expected_freq)

    #print(f"Test statistic: {testStat:.2f}")
    #print(f"P-value: {pValue:.4f}")
    # According to the BSI Standard PTG2 the test variable of the X2-Test must be less than 65.0
    return testStat < 65.0