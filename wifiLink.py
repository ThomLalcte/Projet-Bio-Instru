import socket
import csv
import numpy
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from datetime import datetime as dt

HOST = '192.168.0.16'    # The remote host
HOST = '192.168.4.1'    # The remote host
PORT = 12345              # The same port as used by the server
esp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
esp.connect((HOST, PORT))

formatedData:list[int] = list(range(32))

file = open("{}.csv".format(dt.now().strftime("%Y-%m-%d-%H:%M")),"w",newline="")
csvFile = csv.writer(file)

# We create the X dataset where the first column is the time reaction in seconds and 
# the second is the intensity of the EMG in mV
X = numpy.random.rand(4000,2)

# We build the y classification
y = []
for x in X:
    if 0.625 <= x[1]:
        if x[0] <= 0.1:
            y.append(1)
        else:
            y.append(2)
    else:
        y.append(0)
y = numpy.array(y)

# We split the dataset matrices into random train and test subsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.18, random_state=42)

# We train the Perceptron model
clf = QuadraticDiscriminantAnalysis()
clf = clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))

# # Create a grid here to display the decision regions for each classifier
# h = 0.02 # not too small step size
# minimum = numpy.argmin(X, axis=0)
# x_min = X[minimum[0]][0]
# y_min = X[minimum[1]][1]
# maximum = numpy.argmax(X, axis=0)
# x_max = X[maximum[0]][0]
# y_max = X[maximum[1]][1]
# xxgrid, yygrid = numpy.meshgrid(numpy.arange(x_min - h, x_max + h, h), numpy.arange(y_min - h, y_max + h, h))

# # We initialize the plt figure
# fig = plt.figure()
# ax = fig.add_subplot(111)

# # We will analyze the entire grid and draw it according to its classification
# Z = clf.predict(numpy.c_[xxgrid.ravel(), yygrid.ravel()])
# Z = Z.reshape(xxgrid.shape)
# ax.contourf(xxgrid, yygrid, Z, cmap='Paired_r', alpha=0.75)
# ax.contour(xxgrid, yygrid, Z, colors='k', linewidths=0.1)
# ax.scatter(X[:,0], X[:,1], c=y, cmap='Paired_r', edgecolors='k')

# # We show the final result
# plt.xlabel("Time (sec)")
# plt.ylabel("Amplitude (V)")
# plt.show()

SinglePrintFlag = False
formatedData = []

try:
    while True:
        data = esp.recv(64)
        startFlag = (data[-1]&128)>0
        if(startFlag):
            if (SinglePrintFlag==False):
                print("reading")
                SinglePrintFlag = True
            for i in range(0,len(data),2):
                currentData = data[i]|(data[i+1]&0b00001111)<<8
                formatedData.append(currentData)
        if(len(formatedData) > 900):
            print("enough data")
            break
    esp.close()

    csvFile.writerow(formatedData)
    file.close()
    formatedData_normalized = numpy.array(formatedData) / 2**12
    # formatedData_normalized = numpy.array(formatedData) / numpy.max(numpy.abs(formatedData),axis=0)
    rms = []
    plage = 100//2
    for offset in range(plage*2,len(formatedData_normalized)-plage):
        rms.append(numpy.sqrt(numpy.mean(formatedData_normalized[offset-plage*2:offset])))
        # rms.append(numpy.sqrt(numpy.mean(formatedData_normalized[offset-plage:offset+plage])))
    rms = [[0.001 * index+plage//1000, rms_i] for index, rms_i in enumerate(rms)]
    plt.plot(numpy.array(formatedData_normalized))
    plt.plot(numpy.append(numpy.zeros([50]),numpy.array(rms).transpose()[1]))
    predictions:numpy.ndarray = clf.predict(rms)
    
    for index, predictions_i in enumerate(predictions.tolist()):
        if(predictions_i == 1):
            print("Il y a faux départ, la personne est partie en ", index , " millisecondes.")
            break
        elif(predictions_i == 2):
            print("Il y a bon départ, la personne est partie en ", index , " millisecondes.")
            break
        elif(index == len(y) - 1):
            print("Aucun faux départ détecté")
            break
        
    plt.show()
except KeyboardInterrupt:
    file.close()
