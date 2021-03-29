#ifndef KEYGEN_H
#define KEYGEN_H

#include <QMessageBox>

#include <string>
#include <iostream>
#include <stdio.h>
#include <fileapi.h>
#include <fstream>

using namespace std;


#define OK 0
#define UNDEFIEND_ERROR 1

class keygen
{
public:
    keygen();
    bool checkRegister();
    int deactivateProg();
    int registerProg();

private:
    char *pathName;
    DWORD getSerialNumber();

};

#endif // KEYGEN_H
