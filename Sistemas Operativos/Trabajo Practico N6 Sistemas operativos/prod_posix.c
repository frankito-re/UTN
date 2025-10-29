// TP6 - POSIX Message Queue - Producer
// Compile: gcc -O2 -Wall -o prod_posix prod_posix.c -lrt
#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#define QNAME "/tp6_posix_queue"
#define MAX_MSG 10
#define MAX_SIZE 128

int main(void){
    mqd_t mq;
    struct mq_attr attr;
    attr.mq_flags = 0;            // blocking
    attr.mq_maxmsg = MAX_MSG;     // max number of messages in queue
    attr.mq_msgsize = MAX_SIZE;   // max size of each message
    attr.mq_curmsgs = 0;

    mq = mq_open(QNAME, O_CREAT | O_WRONLY, 0666, &attr);
    if(mq == (mqd_t)-1){
        perror("mq_open");
        return 1;
    }

    for(int i=1;i<=5;i++){
        char buf[MAX_SIZE];
        snprintf(buf, sizeof(buf), "Mensaje %d", i);
        unsigned prio = (unsigned)(10 - i); // prioridad más alta para el 1
        if(mq_send(mq, buf, strlen(buf)+1, prio) == -1){
            perror("mq_send");
            mq_close(mq);
            return 1;
        }
        printf("[PROD] Enviado: \"%s\" (prio=%u)\n", buf, prio);
        usleep(150000);
    }

    mq_close(mq);
    // Nota: no hacemos mq_unlink aquí para que el consumidor pueda abrirla.
    return 0;
}
