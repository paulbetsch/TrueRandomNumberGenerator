from math import log as log
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc
import logging


def TotalFailureTest(binary_data:str, verbose=False, pattern_length = 10):
        """
        Aufruf Pattern_length muss angepasst werden - 5 sollte gut sein (TotalFailureTest(bits, False, 5))
    
        :param      binary_data:        a binary string
        :param      verbose             True to display the debug message, False to turn off debug message
        :param      pattern_length:     the length of the pattern (m)
        :return:    ((p_value1, bool), (p_value2, bool)) A tuple which contain the p_value and result of serial_test(True or False)
        """
        length_of_binary_data = len(binary_data)

        # Augment the n-bit sequence to create n overlapping m-bit sequences by appending m-1 bits
        # from the beginning of the sequence to the end of the sequence.
        # NOTE: documentation says m-1 bits but that doesnt make sense, or work.
        binary_data += binary_data[:pattern_length + 1:]

        # Get max length one patterns for m, m-1, m-2
        max_pattern = ''
        for i in range(pattern_length + 2):
            max_pattern += '1'

        # Keep track of each pattern's frequency (how often it appears)
        vobs_01 = zeros(int(max_pattern[0:pattern_length:], 2) + 1)
        vobs_02 = zeros(int(max_pattern[0:pattern_length + 1:], 2) + 1)

        for i in range(length_of_binary_data):
            # Work out what pattern is observed
            vobs_01[int(binary_data[i:i + pattern_length:], 2)] += 1
            vobs_02[int(binary_data[i:i + pattern_length + 1:], 2)] += 1

        # Calculate the test statistics and p values
        vobs = [vobs_01, vobs_02]

        sums = zeros(2)
        for i in range(2):
            for j in range(len(vobs[i])):
                if vobs[i][j] > 0:
                    sums[i] += vobs[i][j] * log(vobs[i][j] / length_of_binary_data)
        sums /= length_of_binary_data
        ape = sums[0] - sums[1]

        xObs = 2.0 * length_of_binary_data * (log(2) - ape)

        p_value = gammaincc(pow(2, pattern_length - 1), xObs / 2.0)

        if verbose:
            logging.debug('Approximate Entropy Test DEBUG BEGIN:')
            logging.debug("\tLength of input:\t\t\t", length_of_binary_data)
            logging.debug('\tLength of each block:\t\t', pattern_length)
            logging.debug('\tApEn(m):\t\t\t\t\t', ape)
            logging.debug('\txObs:\t\t\t\t\t\t', xObs)
            logging.debug('\tP-Value:\t\t\t\t\t', p_value)
            logging.debug('DEBUG END.')

        return (p_value, (p_value >= 0.01))



