// Client to interact with server:
// Current function is "getfile" and "exit" commands from server.


#include <arpa/inet.h> // for inet_ntoa
#include <stdio.h>  // for printf
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

#define PORT 5000

void GetFile(int sock);

int main()
{
	int sock = 0; 
	int connect_status = 0;
	char function_name[10];
	struct sockaddr_in serv_addr;
    

	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
		{
		printf("\n Socket creation error \n");
		return -1;
		}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	// Convert IPv4 and IPv6 addresses from text to binary
	if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) 
	{
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}

	if ((connect_status = connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) 
	{
		printf("\nConnection Failed \n");
		return -1;
	}
		
	printf("\nConnection Established \n");
	while(1)
	{
		read(sock, function_name, sizeof(function_name)); // Get requested function from server
		if (strcmp(function_name, "getfile") == 0)
		{
        	GetFile(sock);
    	}
		else if (strcmp(function_name, "exit") == 0)
		{
            break;
        }
		bzero(function_name, sizeof(function_name)); 

	}
	
	return 0;

}

void GetFile(int sock)
{
	
	char filename[100];
	char  buffer[1024] = { 0 };
	char * input = "inputfilename";
	char * found = "FOUND";

	send(sock, input, strlen(input), 0); // Send 'inputfilename'

	bzero(filename, sizeof(filename));
	read(sock, filename, sizeof(filename)); // Get the filename
	printf("\nFile Name : %s \n", filename);

	if (access(filename, F_OK) == 0) 
	{
		//printf("File exists\n");
		send(sock, found, strlen(found), 0); // send confirmation of file existence

		//bzero(buffer, sizeof(buffer));
		read(sock, buffer, sizeof(buffer)); // receive ok from server
		printf("buffer: %s\n", buffer);
		//printf("%i buffer: ", buffer);

		if (strcmp(buffer, "ok") == 0) 
		{
			FILE * fp = fopen(filename, "rb");
			printf("filename = %s\n", filename);

			if (fp == NULL) 
				{ 
					printf("File does not exist");
				}

			int bytes_read = fread(buffer, 1, sizeof(buffer), fp);
			int bytes_written = write(sock, buffer, bytes_read);

			fclose(fp);
		}

	}
		
   	else 
    {
    	printf("File does not exist\n");
    }
	return;

}
