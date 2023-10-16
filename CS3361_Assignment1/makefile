assignment_1: main.o calculator.o
        gcc main.o calculator.o -o assignment_1
main.o: main.c
        gcc -c main.c
calculator.o: calculator.c calculator.h
        gcc -c calculator.c
clean:
        rm *.o