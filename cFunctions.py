def cGetFile(c, buffer):
    import os                       #Get file function recived from the server, this will be used to send files to the server from this client.
    c.send("inputfilename".encode())  ##2
    filename = c.recv(buffer).decode() ##3
    print(filename)
    if os.path.isfile(filename):                            #Checks filenpath and name to see if it exists
        found = 'FOUND' + str(os.path.getsize(filename))
        print(found) 
        c.send(found.encode())    ##4
        response = c.recv(buffer).decode()  ##5
        print(response)                                  #Checking reponse from server
        if response == 'ok':
            with open(filename) as f:
                contents = f.read(buffer)
                c.send(contents.encode())
                f.close() ##6
                print(filename + " sent")

def cPutFile(c, buffer):
    c.send('SEND'.encode()) ##
    filename = c.recv(buffer).decode() #2            #waits from input from server filename
    filename2 = filename.split("/")
    filename3 = filename2[-1]
    print(filename3)
    c.send('SENDC'.encode()) ##
    contents = c.recv(buffer).decode() #4
    with open('put_' + filename3,'wb') as f:
        f.write(contents.encode())  ##
        print("Upload of " + filename3 + " is complete")
        f.close()

def cArgs(c, buffer):
    while True:
        from cFunctions import cGetFile, cPutFile
        data = c.recv(buffer).decode()
        if data == "getfile":    
            cGetFile(c, buffer)
        if data == "putfile":  
            cPutFile(c, buffer)
        if data == "exit":
            c.close()
            break