"""
Client Functions
====================

.. Summary::

These functions were designed to allow files to be transferred from and to,(get and put). 
The client does not print any statements or is interacted with in the command line,
all interactions are controlled by the server. The server sends commands, 
the client will execute this commands and respond back to the server.

These functions are broken down into:
cGetFile - This retrieves the file name and contents, send the contents to the server, sFunctions: GetFile function
cPutFile - This collects the filename and strips and directories (Linux  dir name only supported at this time), 
after sends command to confirm ready to receive the file and contents"""


def cGetFile(c, buffer, fbuffer):                      #Getfile function
    import os                                          #os module for if statement to check filename exists
    c.send("inputfilename".encode())                   #This sections collects the filename, check are done to confirm the file exists
    filename = c.recv(buffer).decode() 
    if os.path.isfile(filename):                            
        found = 'FOUND' + str(os.path.getsize(filename))
        c.send(found.encode())    
        response = c.recv(buffer).decode()
        if response == 'ok': 
            with open(filename) as f:                   #File opened and contents read and send to server
                contents = f.read(fbuffer)
                c.send(contents.encode())
                f.close()

def cPutFile(c, buffer, fbuffer):                       #cPutfile function
    c.send('SEND'.encode())                             
    filename = c.recv(buffer).decode()                  #Filename stripped of directory contents
    filename2 = filename.split("/")
    filename3 = filename2[-1]
    c.send('SENDC'.encode()) 
    contents = c.recv(fbuffer).decode()                 #Contents received from server, 
    with open('new_' + filename3,'wb') as f:
        f.write(contents.encode())
        f.close()

def cArgs(c, buffer, fbuffer):                          #Hows to process client arguments, inputs from server pushed to other functions listed above.
    while True:
        from cFunctions import cGetFile, cPutFile
        data = c.recv(buffer).decode()
        if data == "getfile":    
            cGetFile(c, buffer, fbuffer)
        if data == "putfile":  
            cPutFile(c, buffer, fbuffer)
        if data == "exit":
            c.close()
            break