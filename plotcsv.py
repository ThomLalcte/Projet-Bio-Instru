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
    data = np.array(data[:2000])
    tempdata = np.square(data-data.mean())
    rms = []
    plage = 100//2
    for offset in range(plage,len(tempdata)-plage):
        rms.append(np.sqrt(np.mean(tempdata[offset-plage*2:offset])))
    plt.plot(data)
    plt.plot(rms)
    plt.show()