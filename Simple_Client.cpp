#include <iostream>
#include "Client.h"
using namespace std;

#define H  "Hello\n"

int main ()
{

Client Simple_Client( "localhost",9992);//connect on that IP with this sockt
for(int i=0;i<4;i++)
  {
    Simple_Client.Send(H); //send to this entity a string
    sleep(2); //sleep 2 sec
  }
Simple_Client.Terminate_Connection();
return 0;
}
