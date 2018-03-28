/*
Original code by: https://github.com/Snootlab/lora_chisterapi
Edited by: Ramin Sangesari
*/

/*-----------------------------------------*/
#include <dirent.h>
#include <string.h>
#include <fcntl.h>
/*-----------------------------------------*/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <RH_RF95.h>
#include <Python.h>

RH_RF95 rf95;

/* The address of the node which is 10 by default */
uint8_t node_number = 1;
uint8_t msg[4] = {0,0,0,0};
int run = 1;
uint8_t int_part = 0;
uint8_t rem = 0;
uint8_t dec_part = 0;
/*-----------------------------------------*/
ssize_t numRead;
/*-----------------------------------------*/
void run_py_script();
void read_file();
/* Send a message every 3 seconds */
void sigalarm_handler(int signal)
{
    run_py_script();
    read_file();
    msg[0] = node_number;
    msg[1] = int_part;
    msg[2] = rem;
    msg[3] = dec_part;

    rf95.send(msg, sizeof(msg));
    rf95.waitPacketSent();
    printf("Send: From Sensor %d 	Measurement: %d.%d\n",msg[0],msg[1]*256 + msg[2],msg[3]);
    alarm(3);
}

/* Signal the end of the software */
void sigint_handler(int signal)
{
    run = 0;
}

void setup()
{ 

    wiringPiSetupGpio();

    if (!rf95.init()) 
    {
        fprintf(stderr, "Init failed\n");
        exit(1);
    }

    /* Tx power is from +5 to +23 dBm */
    rf95.setTxPower(23);
    /* There are different configurations
     * you can find in lib/radiohead/RH_RF95.h 
     * at line 437 
     */
    rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
    rf95.setFrequency(902.3); /* Mhz */
}

void loop()
{
	sleep(1000);
}

void run_py_script()
{
	Py_Initialize();
	PyRun_SimpleString("execfile(\"/home/pi/Desktop/RTFL_Sensor/Sensor.py\")");
	Py_Finalize();
}

void read_file()
{
	FILE *myfile;
  	double myvariable;
	double times;
	uint8_t int_remainder;
	myfile=fopen("/home/pi/Desktop/Scripts/myapp.txt", "r");
	fscanf(myfile,"%lf",&myvariable);
	myvariable = roundf(100*myvariable)/100;

	times = myvariable / 256;
	int_remainder = (uint8_t)myvariable % 256;
	int_part = (uint8_t)times;
	rem = int_remainder;
  	double decpart = myvariable - (uint8_t)myvariable;
	dec_part = (uint8_t)(decpart*100);
}

int main(int argc, char **argv)
{
    signal(SIGINT, sigint_handler);
    signal(SIGALRM, sigalarm_handler);

    alarm(3);

    setup();

    while( run )
    {
        loop();
        usleep(5);
	run = 0;
    }

    return EXIT_SUCCESS;
}
