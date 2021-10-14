import numpy as np


def LehmerEncoder(ordered_array, lehmer_code):
    min_index = np.argmin(ordered_array)
    min_value = ordered_array.array[min_index]

    count = 0
    for index in range(0, min_index):
        value = ordered_array[index]
        if value > min_value:
            count += 1

    ordered_array.delete(min_index)
    lehmer_code.append(count)

    LehmerEncoder(ordered_array,lehmer_code)


