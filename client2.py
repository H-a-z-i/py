""" This client will run on a given host and port number, from there commands are run from the server and all output is returned"""
import socket
import os
from sys import platform
host = "127.0.0.1"                          #host IP current set to localhost
port = 5001                                 #port number
c_buffer = 1024

def client():                                                       #function to create client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #create socket
    s.connect((host, port))                                         #connect to host and port
    os_name = platform.lower()                                      #created for future compatibility in command such as shell commands and os commands
    if "linux" in os_name:                                          #OS determined by platform
        s.send("The OS is: Linux".encode())
    elif "win32" in os_name:
        s.send("The OS is: Windows ".encode())
    while True:
        data = s.recv(1024).decode()
        if data == "GetFile":                                       #Get file function recived from the server, this will be used to send files to the server from this client.
            s.send("filename".encode())
            filename = s.recv(1024).decode()
            if os.path.isfile(filename):                            #Checks filenpath and name to see if it exists
                data = 'EXISTS' + str(os.path.getsize(filename))    #Adds EXSITS to the filename, this then check if the file exists on return
                s.send(data.encode())
                userAnswer = s.recv(1024).decode()
                #print(userAnswer)                                  #Checking reponse from server
                if userAnswer == 'ok':
                    with open(filename) as f:
                        confile = f.read(1024)
                        s.sendall(confile.encode())
            else:
                s.send("File not found, use full file paths or run client from dir destination ".encode()) #If name doesn match error message is returned
if __name__ == '__main__':
    client()