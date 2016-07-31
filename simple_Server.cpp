#include <termios.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>


#define maxBytes 1024


void terminate_with_error (const char * error_msg,int sock)
{
	perror("Error Binding Socket:");
	if (sock != -1)
	{
		close (sock);
		exit(1);
	}
}


int main(void)
{
 //Simple Server

int sock;
struct sockaddr_in serverAddr;
struct sockaddr_in clientAddr;
socklen_t sin_size = sizeof(struct sockaddr_in);

if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) terminate_with_error("Error Creating Socket",sock);
int sock_opt = 1;
setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,(void *)&sock_opt,sizeof (sock_opt));
      serverAddr.sin_family = AF_INET;
      serverAddr.sin_port = htons(9992);
      serverAddr.sin_addr.s_addr = INADDR_ANY;
      bzero(&(serverAddr.sin_zero), 8);
if (bind(sock, (struct sockaddr *)&serverAddr, sizeof(struct sockaddr)) == -1) terminate_with_error("Error Binding",sock);

if (listen(sock, 10) == -1) terminate_with_error("Error Listening: ",sock);
int newsock = accept(sock, (struct sockaddr *)&clientAddr,&sin_size);

char buffer[maxBytes];

if ( newsock < 1 ) terminate_with_error("Error Accepting Socket",0);
  else
{
		//loop for Receiving multiple packets
    do
  {
      memset(buffer,0, maxBytes);
      int bytes_read = recv (newsock,buffer,maxBytes,0);
      if(bytes_read <= 0) { printf("bytes_read = %d\n",bytes_read ); perror("Error Receiving Message:"); return -2;}
     else
			printf ("Received Message from %s:%d\n%s\n",(char *)inet_ntoa(clientAddr.sin_addr),clientAddr.sin_port,buffer);
	}while(true);
}
close(newsock);
close(sock);
}
