from math import fabs as fabs
from math import sqrt as sqrt
from scipy import stats
from scipy.special import erfc as erfc
import logging

"""
    Example Run Implementation of function StartUpTest():
    if(__name__ == '__main__'):
        bits = random.getrandbits(128)
        bitString = str(bin(bits)[2:])
        print('0:' + str(bitString.count('0')) +  ', 1:' + str(bitString.count('1')))
        print(StartUpTest.StartUpTest(bin(bits)[2:]))
    else:
        pass
"""

def StartUpTest(binaryString: str):
    """
    Implements two statistical Test to ensure the provided Bit Array has a good randomness.
    Input:
        binaryString: an string with bits. Canbe Provided by bin()[2:] method.
    Return:
        True if both statistical tests (monobit and chi-squared gof) are successful. False if one of them is not passed.
    """
    #TODO: Test the tests and update to ensure X Bit array is used
    if(__test_monobit(binaryString) and __chi2_gof_test(binaryString)):
        return True
    else:
        return False

def __test_monobit(binaryString: str):
    """
    Implements the Monobit Test on a binary array.
    Input:
        bits: an array with the bits as integers.
    Description and Evaluation rule:
        The Monobit Test is passed when the sum of all bits is in the interval [9654;10346]. Otherwise it failed.
    """
    length_of_bit_string = len(binaryString)

    # Variable for S(n)
    count = 0
    # Iterate each bit in the string and compute for S(n)
    for bit in binaryString:
        if bit == "0":
            # If bit is 0, then -1 from the S(n)
            count -= 1
        elif bit == "1":
            # If bit is 1, then +1 to the S(n)
            count += 1

    # Compute the test statistic
    sObs = count / sqrt(length_of_bit_string)

    # Compute p-Value
    p_value = erfc(fabs(sObs) / sqrt(2))

    # return a p_value and randomness result
    logging.info("Monobit: " + str(p_value >= 0.01))
    return (p_value >= 0.01)



def __chi2_gof_test(binaryString: str):
    """
    Implements a chi-squared goodness of fit test on a binary array.
    Input:
        bits: an array with the bits as integers.
    Description and Evaluation rule:
        The Test is passed when the P-Value is smaller than 1.0. Otherwise it failed.
    """
    # Define the expected frequencies assuming a discrete uniform distribution
    n = len(binaryString)
    # Count the observed frequencies
    observed_freq = [binaryString.count('0'), binaryString.count('1')]

    # Calculate the expected frequencies
    expected_freq = [n/2, n/2]

    #print('Expexted Frequency: ' + str(expected_freq) + 'Observed Frequency: ' + str(observed_freq))

    # Perform the chi-squared goodness of fit test
    testStat, pValue = stats.chisquare(observed_freq, expected_freq)

    #print(f"Test statistic: {testStat:.2f}")
    #print(f"P-value: {pValue:.4f}")
    logging.info("Chi-Squared: " + str(pValue >= 0.01))
    # According to the BSI Standard PTG2 the test variable of the X2-Test must be less than 65.0 # TODO: Figure out which variable should be tested
    return pValue >= 0.01