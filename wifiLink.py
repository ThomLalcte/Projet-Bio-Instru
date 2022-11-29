import socket
import csv
import numpy
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

HOST = '192.168.0.16'    # The remote host
HOST = '192.168.4.1'    # The remote host
PORT = 12345              # The same port as used by the server
esp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
esp.connect((HOST, PORT))

formatedData:list[int] = list(range(32))

file = open("data.csv","w",newline="")
csvFile = csv.writer(file)

# We create the X dataset where the first column is the time reaction in seconds and 
# the second is the intensity of the EMG in mV
X = numpy.random.rand(1250,2)

# We build the y classification
y = []
for x in X:
    if x[0] <= 0.1 and 0.33 <= x[1]:
        y.append(1)
    else:
        y.append(0)
y = numpy.array(y)

# We split the dataset matrices into random train and test subsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.18, random_state=42)

# We train the Perceptron model
clf = QuadraticDiscriminantAnalysis()
clf = clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))

try:
    while True:
        numberOfFormatedData = 0
        formatedData = []
        data = esp.recv(64)
        startFlag = (data[-1]&128)>0
        for i in range(0,len(data),2):
            currentData = data[i]|data[i+1]<<8
            if(startFlag):
                formatedData.append(currentData)
                numberOfFormatedData = len(formatedData)
        if(numberOfFormatedData > 900):
            break

    rms = formatedData / numpy.max(numpy.abs(formatedData),axis=0)
    rms = [[0.001 * index, rms_i] for index, rms_i in enumerate(rms)]
    predictions = clf.predict(rms)
    index_first_movement = predictions.index(1)
    if(index_first_movement < 100):
        print("Aucun faux départ.")
    else:
        print("Il y a faux départ, la personne est partie en ", index_first_movement, " millisecondes.")

    csvFile.writerow(formatedData)
except KeyboardInterrupt:
    file.close()
