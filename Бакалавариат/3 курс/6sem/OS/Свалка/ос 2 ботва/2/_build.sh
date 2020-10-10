gcc -c error.c
gcc -c main.c
gcc -c filetree.c
gcc -c pathalloc.c
gcc -o filetree main.o error.o filetree.o pathalloc.o
