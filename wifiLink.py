import socket
import csv

HOST = '192.168.0.16'    # The remote host
HOST = '192.168.4.1'    # The remote host
PORT = 12345              # The same port as used by the server
esp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
esp.connect((HOST, PORT))

formatedData:list[int] = list(range(32))

file = open("data.csv","w",newline="")
csvFile = csv.writer(file)

try:
    while True:
        formatedData = []
        data = esp.recv(64)
        for i in range(0,len(data),2):
            formatedData.append(data[i]|(data[i+1]&15)<<8)
        startFlag = (data[-1]&128)>0
        csvFile.writerow(formatedData)
except KeyboardInterrupt:
    file.close()
