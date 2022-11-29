from matplotlib import pyplot as plt
import csv
import numpy as np

with open("force faible.csv","r") as file:
    csvreader = csv.reader(file)
    data = []
    for row in csvreader:
        roww = []
        for sample in row:
            # roww.append(int(sample))
            data.append(int(sample))
        # data.append(roww)
    file.close()
    data = np.array(data)
    tempdata = np.square(data-data.mean())
    rms = []
    for offset in range(10,len(tempdata)-10):
        rms.append(np.sqrt(np.mean(tempdata[offset-10:offset+10])))
    plt.plot(data)
    plt.plot(rms)
    plt.show()