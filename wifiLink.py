import socket


HOST = '192.168.0.16'    # The remote host
PORT = 12345              # The same port as used by the server
esp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
esp.connect((HOST, PORT))

formatedData:list[int] = list(range(32))

while True:
    formatedData = []
    data = esp.recv(64)
    for i in range(0,len(data),2):
        formatedData.append(data[i]|data[i+1]<<8)
