#include "filetree.h"

#include <stdio.h>


int main(int argc, char *argv[])
{
	int ret;
	long nreg, ndir, nblk, nchr, nfifo, nslink, nsock, ntot;
	
	if (argc != 2)
		err_quit("Использование: ftw <начальный_каталог>");
		
	ret = myftw(argv[1]); /* выполняет всю работу */
	/*get_ftw_results(&nreg, &ndir, &nblk, &nchr, &nfifo, &nslink, &nsock);
	
	ntot = nreg + ndir + nblk + nchr + nfifo + nslink + nsock;
	if (ntot == 0)
		ntot = 1; //во избежание деления на 0; вывести 0 для всех счетчиков
	
	printf("summary:\n");
	printf("common files:\t%7ld, %5.2f%%\n", nreg, nreg*100.0/ntot);
	printf("catalogs:\t%7ld, %5.2f %%\n", ndir, ndir*100.0/ntot);
	printf("block-devices:\t%7ld, %5.2f %%\n", nblk, nblk*100.0/ntot);
	printf("char-devices:\t%7ld, %5.2f %%\n", nchr, nchr*100.0/ntot);
	printf("FIFOs:\t\t%7ld, %5.2f %%\n", nfifo, nfifo*100.0/ntot);
	printf("sym-links:\t%7ld, %5.2f %%\n", nslink, nslink*100.0/ntot);
	printf("sockets:\t%7ld, %5.2f %%\n", nsock, nsock*100.0/ntot);*/
	return ret;
}