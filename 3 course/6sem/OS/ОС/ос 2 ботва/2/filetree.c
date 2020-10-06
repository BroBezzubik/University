#include "filetree.h"
#include "error.h"

#include <stdio.h>
#include <string.h>


//static char *fullpath; // полный путь к обрабатываемому файлу
static long	nreg = 0,
			ndir = 0,
			nblk = 0,
			nchr = 0,
			nfifo = 0,
			nslink = 0,
			nsock = 0;

			
void printTabs(int n)
{
	int i;
	for (i = 0; i < n; ++i)
		printf( "  " );
}


static void dopath(const char* filename, int depth)
{
	struct dirent *dir_entry;
	struct stat statbuf;
	DIR *dir_stream;
	
	//игнорируем при рекурсии
	if (strcmp(filename, ".") == 0 || strcmp(filename, "..") == 0)
		return;
	
	lstat( filename, &statbuf );
	
	printTabs(depth);

	//если файл не является каталогом, то просто отображаем его в дереве
    if ( !S_ISDIR(statbuf.st_mode) )
	{
		printf( "%s\n", filename );
		return;
	}
	
	//если же файл является каталогом, то отображаем его и повторяем процедуру для его содержимого
	printf( "%s/\n", filename );
	if ((dir_stream = opendir(filename)) == NULL)
	{
		err_ret("dopath: couldn't open directory '%s'", filename);
		return;
	}
	
	chdir(filename);
	while ( (dir_entry =  (dir_stream)) != NULL ) 
		dopath(dir_entry->d_name, depth+1);
	chdir("..");
	
	closedir(dir_stream);
}



int myftw(char *path)
{
	dopath(path, 0);
	printf( "--------------------\n" );
	return 0;
}