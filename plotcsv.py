from matplotlib import pyplot as plt
import csv

with open("first flex.csv","r") as file:
    csvreader = csv.reader(file)
    data:list[int] = []
    for row in csvreader:
        for sample in row:
            data.append(int(sample))
    file.close()
    plt.plot(data)
    plt.show()