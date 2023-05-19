from numpy import zeros as zeros
from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

def monobit_test(binary_data: str):

    length_of_bit_string = len(binary_data)

    # Variable for S(n)
    count = 0
    # Iterate each bit in the string and compute for S(n)
    for bit in binary_data:
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
    return p_value, (p_value >= 0.01)

def block_frequency_test(binary_data: str, block_size=128):

    length_of_bit_string = len(binary_data)

    if length_of_bit_string < block_size:
        block_size = length_of_bit_string

    # Compute the number of blocks based on the input given.  Discard the remainder
    number_of_blocks = floor(length_of_bit_string / block_size)

    if number_of_blocks == 1:
        # For block size M=1, this test degenerates to test 1, the Frequency (Monobit) test.
        return monobit_test(binary_data[0:block_size])

    # Initialized variables
    block_start = 0
    block_end = block_size
    proportion_sum = 0.0

    # Create a for loop to process each block
    for counter in range(number_of_blocks):
        # Partition the input sequence and get the data for block
        block_data = binary_data[block_start:block_end]

        # Determine the proportion 蟺i of ones in each M-bit
        one_count = 0
        for bit in block_data:
            if bit == "1":
                one_count += 1
        # compute π
        pi = one_count / block_size

        # Compute Σ(πi -½)^2.
        proportion_sum += pow(pi - 0.5, 2.0)

        # Next Block
        block_start += block_size
        block_end += block_size

    # Compute 4M Σ(πi -½)^2.
    result = 4.0 * block_size * proportion_sum

    # Compute P-Value
    p_value = gammaincc(number_of_blocks / 2, result / 2)

    return p_value, (p_value >= 0.01)

def run_test(binary_data: str):

    vObs = 0
    length_of_binary_data = len(binary_data)

    # Predefined tau = 2 / sqrt(n)
    tau = 2 / sqrt(length_of_binary_data)

    # Step 1 - Compute the pre-test proportion πof ones in the input sequence: π = Σjεj / n
    one_count = binary_data.count("1")

    pi = one_count / length_of_binary_data

    # Step 2 - If it can be shown that absolute value of (π - 0.5) is greater than or equal to tau
    # then the run test need not be performed.
    if abs(pi - 0.5) >= tau:
        return 0.00000, False
    else:
        # Step 3 - Compute vObs
        for item in range(1, length_of_binary_data):
            if binary_data[item] != binary_data[item - 1]:
                vObs += 1
        vObs += 1

        # Step 4 - Compute p_value = erfc((|vObs − 2nπ * (1−π)|)/(2 * sqrt(2n) * π * (1−π)))
        p_value = erfc(abs(vObs - (2 * length_of_binary_data * pi * (1 - pi))) / (2 * sqrt(2 * length_of_binary_data) * pi * (1 - pi)))

    return p_value, (p_value > 0.01)

def longest_one_block_test(binary_data: str):

    length_of_binary_data = len(binary_data)

    # Initialized k, m. n, pi and v_values
    if length_of_binary_data < 128:
        # Not enough data to run this test
        return 0.00000, 'Error: Not enough data to run this test'
    elif length_of_binary_data < 6272:
        k = 3
        m = 8
        v_values = [1, 2, 3, 4]
        pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
    elif length_of_binary_data < 750000:
        k = 5
        m = 128
        v_values = [4, 5, 6, 7, 8, 9]
        pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    else:
        # If length_of_bit_string > 750000
        k = 6
        m = 10000
        v_values = [10, 11, 12, 13, 14, 15, 16]
        pi_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

    number_of_blocks = floor(length_of_binary_data / m)
    block_start = 0
    block_end = m
    xObs = 0
    # This will initialize an array with a number of 0 you specified.
    frequencies = zeros(k + 1)

    # print('Number of Blocks: ', number_of_blocks)

    for count in range(number_of_blocks):
        block_data = binary_data[block_start:block_end]
        max_run_count = 0
        run_count = 0

        # This will count the number of ones in the block
        for bit in block_data:
            if bit == "1":
                run_count += 1
                max_run_count = max(max_run_count, run_count)
            else:
                max_run_count = max(max_run_count, run_count)
                run_count = 0

        max(max_run_count, run_count)

        # print('Block Data: ', block_data, '. Run Count: ', max_run_count)
        if max_run_count < v_values[0]:
            frequencies[0] += 1
        for j in range(k):
            if max_run_count == v_values[j]:
                frequencies[j] += 1
        if max_run_count > v_values[k - 1]:
            frequencies[k] += 1

        block_start += m
        block_end += m

    # Compute xObs
    for count in range(len(frequencies)):
        xObs += pow((frequencies[count] - (number_of_blocks * pi_values[count])), 2.0) / (
                number_of_blocks * pi_values[count])

    p_value = gammaincc(float(k / 2), float(xObs / 2))

    return p_value, (p_value > 0.01)



def onlineTest(binary_data: str):
    print("Monobit: "+str(monobit_test(binary_data)))
    print("Block: "+str(block_frequency_test(binary_data)))
    print("Run: "+str(run_test(binary_data)))
    print("Longest: "+str(longest_one_block_test(binary_data)))


String = "11011110110011111010101011100010001000011110000010111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110010010000011000001011011101001110001111001100101110100000001100110111001011010011001100001111100110111011110000000100000011101010011000101000001000011011001000011001000101011011000001000100110110000011101001010010011111110000000010100001110100111101110101100011011010010001010010111100100111010100110101010001111010010101111101000101100100100101010010001011101111110101001001000111000101011100000100000010110111011010010010101111110010110100001100011100110110001100000110110010111100111101011001111011001010110001111001111110110101011110000101010010100001000101110001010101101100000011000111010111110010100011100111110010011100010101011110111101101000101110100101110010110010110011110011000010101110110110010010010100110110111001111010111011000001111101001010001101110010111001110000111111111110100111011110000110010011011000010000100101101101000100001111001011000000110011101110101110011000101010010000110100101100010001100111010111011100100010110000000010010010100010011010010010100100001100000000000000000010110111001101111011000101100001010101010000111000111100000010001000011001010111110010011010000011011010111100110111000000111011110110110011100100010010101101010101101011111011010110011110001011000010110100111001001001111100101011011010011111001001001010101000101011111111011011001111101000111111001000010010001011111001100101101100011101010011111011101011101101000101111000000010110101001101011000101111110110000011001001001111101101100001011001011011110110111010001001001000011111000011100000110010001000111111000000011011101010011001111000010101010001111110100110111011100110111100110111110010001101011110000000111010001111110110011001010011101111101000111100011011101111010101010110101101000010000001010110111101111010111110110100001110110101111100010111111011011110111011001100011100101001101001011000111000010111101111011001011001101110010000111000110111011110000101011011011011110111001010110100101011011110100100110010111110110100100110110011011010010010101010011100100110000100100101101110101101111111100000001001111000101000001001110010010001001011000110010110000111111010100101111110000100101111110110101001100011010000111101100100111010010001000011011011011101000011001110110011111000100011001110101000011100011000001110110110011111101100110100011100111001101110100000010100110010001010000111011001001010111110001001011100010101111100001111111100011101011001101010101010110110011010101000111111110010011101001000000110101101100110100100101011011001101000100101100100101000000010100101101001100011101111111010010111001011001001001100110010100000011111010100101101010001110100010010000001011100111001110001100000101001110100111001111111000110101000000111111111001100100000111001110100010110101011111101110001110001100100101011111100111000100010111010001110010010010010100101100001010101010100110011010111110111101100011110001011100101001011011011010100000111100001101000111100011101110101010111101010"
print(len(String))
onlineTest(String)
