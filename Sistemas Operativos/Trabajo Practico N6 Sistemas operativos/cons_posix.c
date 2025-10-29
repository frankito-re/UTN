// TP6 - POSIX Message Queue - Consumer
// Compile: gcc -O2 -Wall -o cons_posix cons_posix.c -lrt
#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define QNAME "/tp6_posix_queue"
#define MAX_SIZE 128

int main(void){
    mqd_t mq = mq_open(QNAME, O_RDONLY);
    if(mq == (mqd_t)-1){
        perror("mq_open");
        return 1;
    }

    struct mq_attr attr;
    if(mq_getattr(mq, &attr) == -1){
        perror("mq_getattr");
        mq_close(mq);
        return 1;
    }

    for(int i=0;i<5;i++){
        unsigned prio;
        char buf[MAX_SIZE];
        ssize_t n = mq_receive(mq, buf, sizeof(buf), &prio);
        if(n == -1){
            perror("mq_receive");
            mq_close(mq);
            return 1;
        }
        printf("[CONS] Recibido: \"%s\" (prio=%u)\n", buf, prio);
    }

    mq_close(mq);
    // Eliminar la cola del sistema
    if(mq_unlink(QNAME) == -1){
        perror("mq_unlink");
        return 1;
    }
    return 0;
}
