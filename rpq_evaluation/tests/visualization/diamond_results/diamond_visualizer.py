'''
for each csv file in ../../test_diamond_results/ directory, plot the results in
matplotlib
csv files are in the format:

n,total_paths,time
1,1,0
4,5,2.956390380859375e-05
7,13,3.24249267578125e-05
10,29,4.8160552978515625e-05
13,61,8.7738037109375e-05
16,125,0.00016617774963378906
19,253,0.0003478527069091797
22,509,0.0005488395690917969
25,1021,0.0013327598571777344
28,2045,0.002663135528564453
31,4093,0.006145954132080078
34,8189,0.015703916549682617
37,16381,0.03756833076477051
40,32765,0.08895421028137207
43,65533,0.301516056060791
46,100000,0.8489089012145996

n,total_paths,time
1,1,0
4,5,3.1948089599609375e-05
7,13,3.337860107421875e-05
10,29,4.8160552978515625e-05
13,61,8.7738037109375e-05
16,125,0.00017690658569335938
19,253,0.00033736228942871094
22,509,0.000553131103515625
25,1021,0.001260995864868164
28,2045,0.0028100013732910156
31,4093,0.00655055046081543
34,8189,0.016375064849853516
37,16381,0.03917860984802246
40,32765,0.09401965141296387
43,65533,0.31699132919311523
46,100000,0.893218994140625

n,total_paths,time
...
'''
import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

def main():
    # get all the csv files in the directory
    csv_files = []
    for file in os.listdir("../../test_diamond_results/"):
        if file.endswith(".csv"):
            csv_files.append(file)

    # plot the results
    for csv_file in csv_files:
        print(csv_file)
        plot(csv_file)

def plot(csv_file):
    # read the csv file
    with open("../../test_diamond_results/" + csv_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # get the number of nodes and the time
    y = {}
    z = {}
    for i in range(1, len(data)):
        # if data[i] is empty, or header, skip
        if len(data[i]) == 0 or data[i][0] == "n":
            continue
        if data[i][0] not in y:
            y[data[i][0]] = []
            z[data[i][0]] = []

        y[data[i][0]].append(float(data[i][1]))
        z[data[i][0]].append(float(data[i][2]))

    # plot the data as x axis (label 'n') to be y.keys() and y axis on right side to be
    # y.values() (label 'ukupno puteva'), and on the left side to be
    # z.values(), which is labelled with 'vrijeme'
    # note that values are lists, so we need to get the average and standard
    # deviation of each list and plot that nicely

    # get the average and standard deviation of each list
    y_avg = []
    y_std = []
    z_avg = []
    z_std = []
    for key in y.keys():
        y_avg.append(np.average(y[key]))
        y_std.append(np.std(y[key]))
        z_avg.append(np.average(z[key]))
        z_std.append(np.std(z[key]))

    # plot the data
    fig, ax1 = plt.subplots()

    # plot the data
    ax1.set_xlabel('n')
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
    plt.title(csv_file)

    # save the plot to image file
    plt.savefig("../diamond_results/plots/" + csv_file + ".png")

    # close the plot
    plt.close()

if __name__ == "__main__":
    main()
