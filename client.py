""" This client will run on a given host and port number, from there commands are run from the server and all output is returned"""
import socket
from sys import platform
host = "127.0.0.1"                          
port = 5000           
buffer = 4096

def client():                                                 
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           
    c.connect((host, port))
    print(host, port)
    from cFunctions import cArgs                                  
    cArgs(c, buffer)
if __name__ == '__main__':
    client()