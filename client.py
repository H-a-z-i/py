"""
Client
====================

.. Summary::
Client connects to the sever and confirms connection all information arguments and commands are defined for this client in cFunctions

"""
import socket
from sys import platform
host = "127.0.0.1"                          
port = 5000                         #port number
buffer = 1024                       #buffer size for command inputs and strings
fbuffer = 4096                      #buffer size for files

def client():                                                 #client function
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #connected to server      
    c.connect((host, port))
    print("Connected on:")                                          
    print(host, port)
    from cFunctions import cArgs                              #Uses client functions (cFunctions) to assign cArgs, this then calls available functions.
    cArgs(c, buffer, fbuffer)
if __name__ == '__main__':
    client()