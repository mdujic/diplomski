'''
this visualizer will first make some groups of csv tables in
../../test_facebook_results/ directory, and then plot the results in matplotlib

csv files will be in same group if they differ only on the first variable,
source node, and the rest of the variables are the same and this will be the case
for csv files not starting with 'restricted_'

csv files starting with 'restricted_' will be in same group if they differ only
on selector and the rest of the variables are the same
'''

from collections import defaultdict
import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

def main():
    # get all the csv files in the directory
    csv_files = []
    for file in os.listdir("../../test_facebook_results/"):
        if file.endswith(".csv"):
            csv_files.append(file)

    # keys = [0, 1123, 1543, 3754]

    # any_shortest_walks is dictionary with keys being array keys and values
    # being list of csv files
    groups = defaultdict(list)
    # plot the results
    for csv_file in csv_files:
        print(csv_file)
        if "any_shortest_walk_" in csv_file:
            temp = csv_file.split("_")
            source = temp.pop(3)
            key = "_".join(temp)
            groups[key].append((csv_file, source))
        elif "all_shortest_walk_" in csv_file:
            temp = csv_file.split("_")
            source = temp.pop(3)
            key = "_".join(temp)
            groups[key].append((csv_file, source))
        else:
            temp = csv_file.split("_")
            selector = temp.pop(2)
            maybe_shortest = ""

            if not selector:
                selector = "nema"
            else:
                try:
                    int(temp[2])
                except ValueError:
                    maybe_shortest = "_" + temp.pop(2)

            key = "_".join(temp)
            groups[key].append((csv_file, selector + maybe_shortest))


    for key, value in groups.items():
        # key is name of table, value is list of pairs of csv files and some
        # other variable on which csv paths differ and which will be
        # concatenated into one plot
        plot(key, value)

def plot(key, csv_files):
    data = []

    for (csv_file, variable) in csv_files:
        # read the csv file
        with open("../../test_facebook_results/" + csv_file, 'r') as f:
            reader = csv.reader(f)
            # add first column to be whole equal to variable
            for row in reader:
                if len(row) == 0 or row[0] == "path":
                    continue
                row.insert(0, variable)
                data.append(row)

    # get the number of solutions and the time
    y = {}
    z = {}

    for i in range(1, len(data)):
        # if data[i] is empty, or header, skip
        if len(data[i]) == 0 or data[i][0] == "path":
            continue
        if data[i][0] not in y:
            y[data[i][0]] = []
            z[data[i][0]] = []

        y[data[i][0]].append(float(data[i][1]))
        z[data[i][0]].append(float(data[i][2]))

    y_avg = []
    y_std = []
    z_avg = []
    z_std = []

    for _key in y:
        y_avg.append(np.mean(y[_key]))
        y_std.append(np.std(y[_key]))
        z_avg.append(np.mean(z[_key]))
        z_std.append(np.std(z[_key]))

    # plot the data
    fig, ax1 = plt.subplots()

    try:
        int(variable)
        label = "izvor"
    except ValueError:
        label = "selektor"

    # plot the data
    ax1.set_xlabel(label)
    ax1.set_ylabel('ukupno puteva')
    ax1.errorbar(
        y.keys(), y_avg, yerr=y_std, fmt='o', label='ukupno puteva', color='blue'
    )
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    # plot the data
    ax2 = ax1.twinx()
    ax2.set_ylabel('vrijeme')
    ax2.errorbar(
        z.keys(), z_avg, yerr=z_std, fmt='.', label='vrijeme', color='red'
    )
    # other possible options for fmt are:
    # 'o' for circles
    # '-' for solid line
    # '--' for dashed line
    # '-.' for dash-dot line
    # ':' for dotted line

    ax2.tick_params(axis='y')
    ax2.legend(loc='upper right')

    # set the title
    plt.title(key)

    # save the plot to image file
    plt.savefig("../facebook_results/plots/" + key + ".png")

    # close the plot
    plt.close()

if __name__ == "__main__":
    main()
