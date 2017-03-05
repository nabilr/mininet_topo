#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>



#define DATA "Hello World"

int main(int argc, char *argv[]){

	/* Variables */

	int sock; 
	int ret;
	struct sockaddr_in server;
	struct hostent *hp; 
	//struct sockaddr_in myaddr, client_addr;
	char buffer[80000];

	/* Create Socket */
	
	sock = socket(AF_INET, SOCK_STREAM, 0);
	
	if (sock < 0 ){
		perror("Socket creation error");
		exit(1);
	}

	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY; // what does this do? 
	server.sin_port = htons(5000); 

	hp = gethostbyname (argv[1]);
	if (hp == 0){
		perror("gethostbyname error");
		close (sock);
		exit(1);
	}

	memcpy(&server.sin_addr, hp -> h_addr, hp -> h_length); 

	server.sin_port = htons(5000);
	
	/* Connect */ 
	
	if (connect(sock, (struct sockaddr*) &server, sizeof(server)) < 0 ){
		perror("connect error");	
		//printf("connect error\n");
		close (sock);
		exit(1);
	}

	/* Check message sent */

	if ((ret = write(sock, buffer, sizeof(buffer))) < 0) {
		perror("send error");
		close (sock);
		exit(1);
	}

	printf("Sent %d\n", ret);

	/* Close Socket */

	close (sock);

	return 0;

}	
