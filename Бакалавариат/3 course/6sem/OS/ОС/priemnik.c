#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	int sock = socket( AF_INET, SOCK_DGRAM, IPPROTO_UDP );
	struct sockaddr_in addr;
	addr.sin_addr.s_addr = INADDR_ANY;
	addr.sin_port = htons(7777);
	addr.sin_family = AF_INET;
	
	printf( "waiting on port %d\n", ntohs(addr.sin_port) );
	
	int result = bind( sock, (struct sockaddr*) &addr, sizeof(addr) );
	printf( "bind result = %d\n", result );
	
	struct sockaddr_in from;
		int fromSize = sizeof(from);
	char buffer[256];
	
	printf( "waiting for data ...\n" );
	while( 1 ) {
		int recvLen = recvfrom( sock, buffer, sizeof(buffer), 0, (struct sockaddr*) &from, &fromSize );
		if( recvLen > 0 ) {
			buffer[recvLen] = '\0';
			printf( "[%s] %s\n", inet_ntoa(from.sin_addr), buffer );
		}
	}

	return 0;
}