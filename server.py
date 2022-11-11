"""
Server
===================

.. Summary::
Server listens for connections from a client, connects and then function ListCMD sanitised inputs and calls over functions / commands"""


"""Connection and global variables for the server"""
import socket
s_host = "0.0.0.0"
s_port = 5000
buffer = 1024
fbuffer = 4096

print("Awaiting a connection from client")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 #Create a socket
s.bind((s_host, s_port))                                              #Bind the socket to the port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)               #Set the socket options
s.listen(5)                                                           #Listen for clients connection (5) - multi thread and client supported
s, addr = s.accept() 
print("Connected to client at ", addr)                                #Connection established 

"""Function for server"""

def server():                           #Server function using ListCMD 
    from sFunctions import ListCMD      #global variables used.
    global buffer
    global s
    global fbuffer
    ListCMD(s, buffer, fbuffer)
if __name__ == '__main__':
    server()