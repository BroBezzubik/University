#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "keygen.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    keygen = new class::keygen;
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_bttn_checkLicanse_clicked()
{
    QMessageBox msgBox;
    int answer = this->keygen->checkRegister();
    switch (answer) {
    case OK:
        msgBox.setText(QString("Activated"));
        break;
    case UNDEFIEND_ERROR:
        msgBox.setText(QString("Nonactivated"));
        break;

    }

    msgBox.exec();
}

void MainWindow::on_bttn_delete_clicked()
{
    int anser = this->keygen->deactivateProg();
    QMessageBox msgBox;
    msgBox.setText(QString("Key deleted!"));
    msgBox.exec();
}

void MainWindow::on_bttn_register_clicked()
{
    QMessageBox msgBox;
    int answer = this->keygen->registerProg();
    switch (answer) {
        case OK:
            msgBox.setText(QString("Registered"));
            break;
        case UNDEFIEND_ERROR:
            msgBox.setText(QString("Error"));
            break;
    }
    msgBox.exec();
}
