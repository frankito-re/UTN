// TP6 - System V Message Queue - Producer
// Compile: gcc -O2 -Wall -o prod_sysv prod_sysv.c
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#define KEY 0x12345

struct msg {
    long mtype;
    char mtext[128];
};

int main(void){
    int qid = msgget(KEY, IPC_CREAT | 0666);
    if(qid == -1){
        perror("msgget");
        return 1;
    }

    for(int i=1;i<=5;i++){
        struct msg m;
        m.mtype = 1; // tipo único (FIFO)
        snprintf(m.mtext, sizeof(m.mtext), "Mensaje %d", i);
        if(msgsnd(qid, &m, strlen(m.mtext)+1, 0) == -1){
            perror("msgsnd");
            return 1;
        }
        printf("[PROD] Enviado: \"%s\"\n", m.mtext);
        usleep(150000);
    }
    return 0;
}
