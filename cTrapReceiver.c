#include "stdio.h"
#include "winsock2.h"
#pragma comment(lib, "ws2_32.lib")
#define SNMP_TRAP_PORT 162
#define MAX_MSG 400

static void init(void)
{

  WSADATA wsa;
    int err = WSAStartup(MAKEWORD(2, 2), &wsa);
    if(err < 0)
    {
        puts("WSAStartup failed !");
        exit(EXIT_FAILURE);
    }

}

static void end(void)
{

    WSACleanup();

}

int main(int argc, char *argv[]) {


  int sd, rc, n, cliLen;
  struct sockaddr_in cliAddr, servAddr;
  char msg[MAX_MSG];



  /* socket creation */
  init();
  sd= socket(AF_INET, SOCK_DGRAM, 0);
  if(sd<0) {
    printf("can't open socket \n");
    exit(1);
  }

  /* bind local server port */
  servAddr.sin_family = AF_INET;
  servAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  servAddr.sin_port = htons(SNMP_TRAP_PORT);
  rc = bind (sd, (struct sockaddr *) &servAddr,sizeof(servAddr));
  if(rc<0) {
    printf("can't bind port number %d \n", SNMP_TRAP_PORT);
    exit(1);
  }

  printf("waiting for SNMP Traps on UDP port %d\n", SNMP_TRAP_PORT);

  /* server infinite loop */
  while(1) {

    /* init buffer */
    memset(msg,0x0,MAX_MSG);


    /* receive message */
    cliLen = sizeof(cliAddr);
    n = recvfrom(sd, msg, MAX_MSG, 0, (struct sockaddr *) &cliAddr, &cliLen);

    if(n<0) {
      printf("%s: cannot receive data \n",argv[0]);
      continue;
    }
    /*message is encoded with ASN1 and should be decoded*/
    /* print received message */
    printf("SNMP Trap received from %s : %o\n", inet_ntoa(cliAddr.sin_addr),msg);


  }/* end of server infinite loop */
end();
return 0;

}

/*
//The printf format specifier %o interprets the next bytes in the argument data as an integer and prints it in octal.
//Passing an array as an argument to a function is converted into passing a pointer to the first element. So these statements are equivalent:
printf("%p\n", msg);
printf("%p\n", &msg[0]);

To actually print the data you received, add the following:
for (int i = 0; i < n; ++i) {
    printf("%02x ", (unsigned char)msg[i]);
}
printf("\n");
*/