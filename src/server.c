#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main(){

	/* Variables */

	int sock, client_fd; 
	struct sockaddr_in server; 
	//struct sockaddr_in myaddr, client_addr;
	char buffer[80000];
	int rval;

	/* Create Socket */
	
	sock = socket(AF_INET, SOCK_STREAM, 0);
	
	if (sock < 0 ){
		perror("Failed to print socket");
		exit(1);
	}

	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY; // what does this do? 
	server.sin_port = htons(5000); 

	printf("created socket\n");

	/* Call Bind */ 

	if ( bind(sock, (struct sockaddr *)&server, sizeof(server))){
		perror("bind error");
		exit(1);
	}

	printf("binded socket\n");

	/* Listen */ 

	listen(sock, 5);
	printf("listening\n");

	/* Accept */
	do {
		client_fd = accept(sock, (struct sockaddr *) 0, 0); 
		sleep(1);
		if (client_fd == 1) 
			perror("accept error\n"); 
		else {

			do {
			memset(buffer, 0, sizeof(buffer));
			if ((rval = read(client_fd, buffer, sizeof(buffer))) < 0)
				perror("reading message error\n");
			else if (rval == 0) {
				printf("The End\n");
				break;
			}

				
			printf("Message recieved (rval = %d)\n", rval);
			sleep(1);
			} while(1);
			/* Close Socket */ 
			close(client_fd);
		}
	} while (1);

	return 0;

}	
