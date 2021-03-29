#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "keygen.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_bttn_checkLicanse_clicked();

    void on_bttn_delete_clicked();

    void on_bttn_register_clicked();

private:
    Ui::MainWindow *ui;
    keygen *keygen;

};
#endif // MAINWINDOW_H
