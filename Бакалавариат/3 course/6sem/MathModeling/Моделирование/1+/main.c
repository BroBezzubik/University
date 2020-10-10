#include <stdio.h>
#include <math.h>
#define h 0.01
///
/// \brief function
/// \param x
/// \param u
/// \return
///
double function(double x, double u)
{
    return pow(x,2)+pow(u,2);
}
///
/// \brief Picar3
/// \param x
/// \return
double Picar3(double x)
{
    double y = pow(x, 3) / 3;
    double tmp = 1 + pow(x, 4) / 21;
    tmp += 2 * pow(x, 3) / (693);
    tmp += pow(x, 12) / (19845);
    return y*tmp;
}
///
/// \brief Picar4
/// \param x
/// \return
///
double Picar4(double x)
{
     double y = pow(x, 31)/109876902975;
     y += 2 * pow(x, 23) / 86266215;
     y += 2 * pow(x, 22) / 1361505915;
     y += 2 * pow(x, 19) / 3393495;
     y += pow(x, 15) / 59535;
     y += 2 * pow(x, 14) / 916839;
     y += pow(x, 13) / 56189133;
     y += 2 * pow(x, 11)/2079;
     y += 2 * pow(x, 10)/31185;
     y += 2 * pow(x, 7)/63;
     y += pow(x, 3) / 3;
     return y;
}
//Численный метод (Метод ломанных)
///
/// \brief polyline
/// \param x
/// \param y
/// \return
///
double polyline(double x, double y)
{
    return (y + h * function(x, y));
}
double Runge2(double x, double y)
{
    return y + h * function(x + h / 2, y + h / 2 * function(x, y));
}
double Runge4(double x, double y)
{

    double K1 = function(x, y);
    double K2 = function(x + h / 2, y + h * K1 / 2);
    double K3 = function(x + h / 2, y + h * K2 / 2);
    double K4 = function(x + h, y + h * K3);
    return y + h / 6 * (K1 + 2 * K2 + 2 * K3 + K4);
}



int main()
{
            // Границы
            double x = 0.0;
            double maxX = 1.0;

            double poly = 0.0;

            double run2 = 0.0;
            double run4 = 0.0;

            puts("X\t\t|Picar3 \t|Picar4 \t|Polyline\t|Runge\t\t|Runge\t\t");//|function\t|");
            puts("\t\t| \t\t| \t\t|yavnyi \t|2d step \t|4th step\t");//\t\t|");
            puts("-------------------------------------------------------------------------------------------");

            while(x <= maxX)
            {
                printf("%.2f\t\t|%.7f\t|%.7f\t|%.7f\t|%.7f\t|%.7f\t\n", x, Picar3(x), Picar4(x), polyline(x, poly), run2, run4);
                poly = polyline(x, poly);
                run2 = Runge2(x, run2);
                run4 = Runge4(x, run4);
                x += h;
            }
            return 0;
}
