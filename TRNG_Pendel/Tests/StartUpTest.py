from math import fabs as fabs
from math import sqrt as sqrt
from scipy.special import erfc as erfc


class StartUPTest:

    @staticmethod
    def monobit_test(binary_data: str):

        length_of_bit_string = len(binary_data)

        # Variable for S(n)
        count = 0
        # Iterate each bit in the string and compute for S(n)
        for bit in binary_data:
            if bit == 48:
                # If bit is 0, then -1 from the S(n)
                count -= 1
            elif bit == 49:
                # If bit is 1, then +1 to the S(n)
                count += 1

        # Compute the test statistic
        sObs = count / sqrt(length_of_bit_string)

        # Compute p-Value
        p_value = erfc(fabs(sObs) / sqrt(2))

        # return a p_value and randomness result
        return p_value, (p_value >= 0.01)

    @staticmethod
    def autocorrelation_test(binary_data: str):

        shift_feld = [0] * 5000
        max_korr_feld = [0] * 5000

        # Fill BitFeldB with data

        for tau in range(1, 5001):
            z_tau = 0
            for i in range(5000):
                z_tau += binary_data[i] ^ binary_data[i + tau]
            shift_feld[tau - 1] = z_tau

        # Debugging
        # for i in range(5000):
        #    print(shift_feld[i], end=' ')

        # Find the index of the maximum deviation from 2500
        max_deviation = 0
        for tau in range(5000):
            deviation = abs(shift_feld[tau] - 2500)
            if deviation > max_deviation:
                max_deviation = deviation

        # Find all indices with the maximum deviation
        j = 0
        for tau in range(5000):
            deviation = abs(shift_feld[tau] - 2500)
            if deviation == max_deviation:
                max_korr_feld[j] = tau
                j += 1

        print("Maximale z_tau-Abweichung von 2500:", max_deviation)
        print("Aufgetreten für Shifts:")
        for k in range(j):
            print("Shift:", max_korr_feld[k] + 1)

        tau = max_korr_feld[0]
        z_tau = 0
        for i in range(10000, 15000):
            z_tau += StartUPTest.char_to_int(i, binary_data) ^ StartUPTest.char_to_int(i + tau + 1, binary_data)
        tau += 1

        ok = 2326 < z_tau < 2674
        return z_tau, ok

    @staticmethod
    def char_to_int(index, binary_data: str):
        if binary_data[index] == 49:
            value = 1
        else:
            value = 0
        return value
