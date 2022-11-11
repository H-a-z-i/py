"""Server Functions
====================

.. Summary::

These functions were designed to allow files to be transferred from and to,(get and put). 
The server is interacted with on the command line after running the server.py script.
Commands have the input sanitised, and will accept only required inputs.

These functions are broken down into:
GetFile - This request the filename and contents from the client. Creates a document under new +filename, linked function cFunctions: cGetFile function
PutFile - This collects the file from input, reads the contents and sends the input to the server.
"""

def GetFile(s, buffer,fbuffer):                                                     #GetFile function
    s.send("getfile".encode())                                                      #getfile string send to client to be processed in cArgs
    filename = s.recv(buffer).decode()                                              
    if filename == "inputfilename":                                                 #Response from client ready to receive filename
        filename = input("Enter the file name with correct extension: ")
        s.send(filename.encode())                     
        found = s.recv(buffer).decode()  ##4
        if found[:5] == 'FOUND':                                                    #Else statement for file verification to be completed, does check and confirm file exists
            filesize = int(found[5:])                                               # If check fails currently hangs needs to be implemented
            get = input("File exists, " + str(filesize) + "Bytes, download (Y/N)? -> ")
            #User asked for download confirmation
            if get == 'Y' or get == 'y':
                s.send('ok'.encode())   ##5
                contents = s.recv(fbuffer).decode() ##6
                #totalRecv = len(contents)                                           #Total length and adjustable buffer TBC
                with open('new__' + filename,'wb') as f:                             #Write content received with new file name to file contents
                    f.write(contents.encode())
                    f.close()
                    print("Download of " + filename + " is complete")
        else:
            print("File does not exist!")

def PutFile(s, buffer):                                                              #Putfile functions
    import os                                                                        #OS import for filename checks
    filename = input("Enter the file name with correct extension: ")
    if os.path.isfile(filename):                                                     #Checks filepath and name to see if it exists
        data = 'FOUND' + str(os.path.getsize(filename))                              #Data check statement to be implemented for this check, this is 
        if data[:5] == 'FOUND':                                                      #Grabs first 5 char from response checks if added to string for file sanitation                       
            #filesize = int(data[5:])
            #print(filesize)
            data = input(str(filename) + " found upload (Y/N)? -> ")                 #Accepts input from Y to accept a upload else command to be done to exit.
            if data == 'Y' or data == 'y':
                s.send("putfile".encode()) #1
                data = s.recv(buffer).decode()
                if data == 'SEND':
                    s.send(filename.encode()) #2
                    data = s.recv(buffer).decode()
                    if data == 'SENDC':
                        with open(filename) as f:                                    #Opens a file and and reads the contents then send to client.
                            contents = f.read(buffer)
                            s.sendall(contents.encode()) #3
                            f.close()
                            print("File uploaded successfully")
        else:
            print("File not recognised, try running from from correct directory, or using full a file path") 

def ListCMD(s, buffer, fbuffer):                                        #ListCMD functions
    from sFunctions import GetFile , PutFile                            #Imports correct functions
    my_list = ['-g', '-p', '-h','exit']
    print ("For list of supported commands and help enter -h ")
    while True:
        commands = input("-> ")                                         #Inputs commands and checks against a list for validated commands
        if commands not in my_list:
            print("Invalid command")
        elif commands == "-g":
            GetFile(s, buffer, fbuffer)
        elif commands == "-p":
            PutFile(s, buffer)
        elif commands == "-h":
            help()
        elif commands == "exit":                                        #Shuts down client and server
            s.send("exit".encode())
            print("Shuttting down any live clients and server")
            s.close()
            break

def help():    #help function that displays current accepted commands
    print(""" The following list of commands are available, all commmands must be run from the server, passing multiple arguments is not supported at this time:
Command list:

    -g   -   Get / download file from client.

    -p   -   Put / upload file to client.

    -h   -   Show the help message.

    exit -  Stops the server, alternatively ctrl + c to exit the server
    """)
