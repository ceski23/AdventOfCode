from task_1 import calc_bits_frequency, parse_input

if __name__ == "__main__":
    numbers = parse_input('input.txt')

    oxygen_num = numbers.copy()
    i = 0
    while len(oxygen_num) > 1:
        freq = calc_bits_frequency(oxygen_num)
        dominant = '1' if freq[i] >= (len(oxygen_num) / 2) else '0'
        oxygen_num = list(filter(lambda x: x[i] == dominant, oxygen_num))
        i += 1

    co2_num = numbers.copy()
    i = 0
    while len(co2_num) > 1:
        freq = calc_bits_frequency(co2_num)
        dominant = '1' if freq[i] < (len(co2_num) / 2) else '0'
        co2_num = list(filter(lambda x: x[i] == dominant, co2_num))
        i += 1

    print(int(oxygen_num[0], 2) * int(co2_num[0], 2))
