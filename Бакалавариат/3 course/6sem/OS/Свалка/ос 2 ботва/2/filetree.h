#pragma once

#include <dirent.h>
#include <limits.h>
#include <sys/stat.h>

enum filetype { FileCommon, FileDir, FileDirNR, FileUnknown };
//файл, не являющийся каталогом; каталог; не доступный для чтения каталог; информацию невозможно получить с помощью stat


//тип функции, которая будет вызываться для каждого встреченного файла
typedef int (*t_parseFunc)(const char*, const struct stat*, enum filetype);


void get_ftw_results(long *r_nreg, long *r_ndir, long *r_nblk, long *r_nchr, long *r_nfifo, long *r_nslink, long *r_nsock);

int myftw(char *pathname);