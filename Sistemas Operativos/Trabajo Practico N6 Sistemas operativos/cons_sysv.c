// TP6 - System V Message Queue - Consumer
// Compile: gcc -O2 -Wall -o cons_sysv cons_sysv.c
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define KEY 0x12345

struct msg {
    long mtype;
    char mtext[128];
};

int main(void){
    int qid = msgget(KEY, 0666);
    if(qid == -1){
        perror("msgget");
        return 1;
    }

    for(int i=0;i<5;i++){
        struct msg m;
        ssize_t n = msgrcv(qid, &m, sizeof(m.mtext), 0, 0); // 0: cualquier tipo, FIFO
        if(n == -1){
            perror("msgrcv");
            return 1;
        }
        printf("[CONS] Recibido: \"%s\"\n", m.mtext);
    }

    // Eliminar la cola
    if(msgctl(qid, IPC_RMID, NULL) == -1){
        perror("msgctl IPC_RMID");
        return 1;
    }
    return 0;
}
