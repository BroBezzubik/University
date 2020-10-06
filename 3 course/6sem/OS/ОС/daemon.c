#include <syslog.h>
#include <fcntl.h>
#include <sys/resource.h>

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <arpa/inet.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>


//FILE *mylog;
//const char mylogname[128] = "/home/artalus/err.txt";
const char demonname[64] = "MyDemon";
#define LOCKFILE "/var/run/MyDemon.pid"

int sock;				//файловый дескриптор сокета, в который
						//пишем репорты
struct sockaddr_in addr;	//адрес, св€занный с этим сокетом

//печать информации путем посылани€ еЄ через сокет
void MyPrint(const char* format, ...)
{
	char message[512];
	va_list ap;
	va_start( ap, format );
	vsnprintf( message, 512, format, ap );
	va_end( ap );
	
	//открываем сокет
	sock = socket( AF_INET, SOCK_DGRAM, IPPROTO_UDP );
	
	//посылаем через сокет, сообщение, длиной, без флагов,
	//по адресу, определенного размера
	sendto( sock, message, strlen(message), 0,
		(struct sockaddr*) &addr, sizeof(addr) );
	
	close( sock ); //закрываем сокет
	
	//fprintf( mylog, "%s: %s\n", demonname, message );
	//fflush( mylog );
}

//возвращает в основную функцию:
//сигнал завершитьс€ предку (1),
//ошибку демонизации(-1),
//успешную демонизацию (0)
int demonize(const char *process_name)
{
	int i;
		
	MyPrint( "fork" );
	//выводим демона в отдельный процесс - не будет €вл€тьс€
	//лидером группы, что позвол€ет вызвать setsid
	int pid = fork();
	if ( pid < 0 )
	{
		MyPrint( "ERROR: fork" );
		return -1;
	}
	if ( pid != 0 ) //parent
		return 1;
	
	//запускаем его в новой сессии - становитс€ лидером сессии,
	//лидером группы и лишаетс€ управл€ющего терминала
	setsid();
	
	//игнорируем сигнал потери терминала
	struct sigaction sa; //будем выполн€ть действие над сигналом:
	sa.sa_handler = SIG_IGN; //игнорировать сигнал
	sigemptyset( &sa.sa_mask ); //сбрасываем маску
	sa.sa_flags = 0;
	
	MyPrint( "sigaction" );
	if ( sigaction(SIGHUP, &sa, NULL) < 0 )
	{
		MyPrint( "ERROR: can't ignore SIGHUP" );
		return -1;
	}
	
	//второй форк - нужен только в систем5
	/*pid = fork();
	if ( pid < 0 )
	{
		fprintf( mylog, "%s: second fork error", process_name );
		fflush( mylog );
		exit(1);
	}
	if ( pid != 0 )
		exit(0); //second parent*/
	
	MyPrint( "changing dir" );
	//мен€ем директорию на / чтобы при необходимости можно было
	//отмонтировать файловую систему, из которой запустилс€ демон
	if ( chdir("/") < 0 )
	{
		MyPrint( "ERROR: can't change directory" );
		return -1;
	}
	

	MyPrint( "umask and getrlimit\n" );
	umask(0); //обнул€ем старую маску доступа к файлам, чтобы она
	//не привела к неопределенному поведению
	
	//получаем максимальное количество дескрипторов
	struct rlimit rl;
	if ( getrlimit(RLIMIT_NOFILE, &rl) < 0 ) 
	{
		MyPrint( "ERROR: couldn't get max number of fd" );
		return -1;
	}
	if ( rl.rlim_max == RLIM_INFINITY )
		rl.rlim_max = 1024;
	
	//проходим по всем дескрипторам и закрываем их - демон не должен
	//взаимодействовать с дескрипторами предка
	for (i = 0; i < rl.rlim_max; ++i)
	{
		if ( i != sock ) //кроме лог-сокета, чтобы было куда писать
			close(i);
	}
	MyPrint( "\n" );
	
	//открываем первые три файловых дескриптора, чтобы библиотечные
	//функции чтени€\записи на стандартный ввод\вывод не оказывали
	//вли€ни€
	int fd0, fd1, fd2;
	fd0 = open( "/dev/null", O_RDWR );
	fd1 = dup(0); //дублируем дескрипторы
	fd2 = dup(0);
	
	//получаем доступ к записи в /var/log/syslog
	openlog( process_name, LOG_CONS, LOG_DAEMON );
	if ( fd0 != 0 || fd1 != 1 || fd2 != 2)
	{
		MyPrint( "ERROR: Incorrect file descriptors 0,1,2" );
		syslog( LOG_ERR, "incorrect fd: %d %d %d", fd0, fd1, fd2 );
		return -1;
	}
	MyPrint( "Demonizing finished." );
	return 0;
}

//обеспечивает запуск демона в единственном экземпл€ре
//завершает выполнение, если не может открыть файл,
//возвращает 1, если файл уже "зан€т",
//0, если запуск возможен
int already_running(void)
{
#define BUFLEN 8
	int fd;
	char buf[BUFLEN];
	
	fd = open( LOCKFILE, O_RDWR|O_CREAT, S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH );
	if (fd < 0)
	{
		MyPrint( "ERROR: unable to open %s: %s", LOCKFILE, strerror(errno) );
		syslog( LOG_ERR, "unable to open %s: %s", LOCKFILE, strerror(errno) );
		exit(1);
	}
	
	flock( fd, LOCK_EX|LOCK_NB );
	if ( errno == EWOULDBLOCK )
	{
		MyPrint( ">>> Can't lock file %s: %s\n>>> Is demon already launched?", LOCKFILE, strerror(errno) );
		syslog(LOG_ERR, "unable to lock %s: %s", LOCKFILE, strerror(errno));
		close(fd);
		return 1;
	}
	
	MyPrint( "%d - Successfully locked the file.", getpid() );
	snprintf( buf, BUFLEN, "%d", getpid() );
	write( fd, buf, strlen(buf) );
	return 0;
}

void demonFunc()
{
	MyPrint( "(%d) timestamp...", getpid() );
	syslog( LOG_INFO, "(%d) timestamp...\n", getpid() );
	sleep(3);
}

int main(void)
{
	addr.sin_addr.s_addr = 0x0100007f;
	addr.sin_port = htons(7777);
	addr.sin_family = AF_INET;
	
	
	printf( "demonizing...\n" );
	int d = demonize( demonname );
	if ( d > 0 )
	{
		MyPrint( "Parent: finished successfully" );
		return 0;
	}
	else if ( d < 0 )
	{
		MyPrint( "Parent: something went wrong!" );
		return 1;
	}
	
	if ( already_running() )
	{
		return 1;
	}
	MyPrint( "Successfully demonized." );
	
	while ( 1 )
	{
		demonFunc();
	}
}