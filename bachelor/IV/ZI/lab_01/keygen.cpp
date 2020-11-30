#include "keygen.h"


using namespace std;

keygen::keygen()
{
}

bool keygen::checkRegister(){
    DWORD serialNumberHD = this->getSerialNumber();
    FILE *keyFile = fopen("debug/key.txt", "r");
    bool result = UNDEFIEND_ERROR;
    if (keyFile) {
        DWORD serialKey = 0;
        fscanf(keyFile, "%u", &serialKey);
        result = (serialKey == serialNumberHD) ? OK : UNDEFIEND_ERROR;
        fclose(keyFile);
    }
    return result;
}

int keygen::deactivateProg(){
    int result = OK;
    FILE *keyFile = fopen("debug/key.txt", "w");
    if (keyFile){
        fclose(keyFile);
        result = OK;
    } else {
        result = UNDEFIEND_ERROR;
    }

    return result;
}

int keygen::registerProg(){
    int result = OK;
    DWORD serialNumberHD = this->getSerialNumber();
    FILE *keyFile = fopen("debug/key.txt", "w");
    if (keyFile){
        fprintf(keyFile, "%u", serialNumberHD);
        result = OK;
        fclose(keyFile);

    } else { result = UNDEFIEND_ERROR; }

    return result;
}

DWORD keygen::getSerialNumber(){
    LPCUWSTR path = L"C:\\";
    DWORD volumeSerialNumber;
    GetVolumeInformationW(path, NULL, NULL, &volumeSerialNumber, NULL, NULL, NULL, NULL);

    return volumeSerialNumber;
}
