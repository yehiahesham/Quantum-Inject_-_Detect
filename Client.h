#ifndef CLIENT_H
#define CLIENT_H


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include <iostream>

//using namespace std;

#define maxBytes 1024


class Client
{

  struct sockaddr_in serverAddr;
  socklen_t sin_size;

public:
  int sock;
  char  bytes[maxBytes];

  Client(const char * Server_IP,int Server_Socket)
  {
     socklen_t sin_size =sizeof(struct sockaddr_in);
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("Error Creating Socket");
        exit(-1);
    }
    memset((char *) &serverAddr, 0,sizeof(serverAddr));
          serverAddr.sin_family = AF_INET;
          serverAddr.sin_port = htons(Server_Socket);//9990
          struct hostent *server = gethostbyname(Server_IP);
    if ( server == NULL ) terminate_with_error(sock);
    memcpy((char *)&serverAddr.sin_addr.s_addr,(char *)server->h_addr, server->h_length);
          memset(&(serverAddr.sin_zero), 0, 8);
    if (connect(sock,(sockaddr *)&serverAddr,sizeof(serverAddr)) == -1 ) terminate_with_error(sock);

  }

void Send(char * buffer1  ) {  /*usleep(1000);*/ send(sock, buffer1, strlen(buffer1), 0); }

void Terminate_Connection() { /*usleep(1000); send (sock,"q\n",sizeof("q\n"),0); */   close(sock); }

void terminate_with_error (int sock)
{
    close (sock);
    perror("Error Binding Socket:");
    exit(1);
}


};

#endif
