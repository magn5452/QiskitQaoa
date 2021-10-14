import numpy as np
from matplotlib import pyplot as plt

class BarPlotter():
    def __init__(self):
        pass

    def plot(self, dictionary):
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111)

        n = 24
        dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)[:n])
        filtered_values = dictionary.values()
        filtered_keys = dictionary.keys()
        index = range(len(filtered_keys))

        ax.bar(index, filtered_values)
        plt.xticks(index, filtered_keys, rotation=70)
        fig.subplots_adjust(bottom=0.2)
