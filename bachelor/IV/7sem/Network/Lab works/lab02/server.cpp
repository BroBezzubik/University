#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#define MSG_LEN 512
#define SOCK_PORT 9100

#define symbols "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

void num_base(int num, int base);
void print_result(int num);

int main(void){
    char buf[MSG_LEN];

    printf("Server started\n");

    int sock;
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1){
        perror("Socket error");
        exit(1);
    }

    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SOCK_PORT);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1){
        close(sock);
        perror("bind error");
        exit(EXIT_FAILURE);
    }

    printf("Server is ready\n");

    while (true){
        struct  sockaddr_in clientAddr;
        socklen_t clientAddrLen = sizeof(clientAddr);
        if (recvfrom(sock, buf, MSG_LEN, 0, (struct sockaddr *)&clientAddr, &clientAddrLen) == -1){
            perror("recvfrom()");
            exit(1);
        }
        printf("Received packet from %s:%d\nData:%s\n\n",
               inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port), buf);

        print_result(atoi(buf));
    }

    close(sock);
    return 0;
}

void num_base(int num, int base){
    if (base == 1){
        while (num > 0){
            printf("1");
            num = num - 1;
        }
    } else {
        if (num){
            int tmp = num % base;
            num = num / base;
            num_base(num, base);
            printf("%c", symbols[tmp]);
        }
    }
}

void print_result(int num){
    printf ("#### RESULT #### \n");
    printf("Result: \n");
    printf("binary: ");
    num_base(num, 2);
    printf("\noct: ");
    num_base(num, 8);
    printf("\nhex: ");
    num_base(num, 16);
    printf("\nBy variant 1nd: ");
    num_base(num, 1);
    printf("\n#### END ####\n\n");
}
