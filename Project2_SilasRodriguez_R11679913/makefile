CC = g++
CFLAGS = -Wall

all: dcooke_parser

dcooke_parser: main.o parser.o
	$(CC) $(CFLAGS) -o $@ main.o parser.o
	
.cpp.o:
	$(CC) -std=c++11 $(CFLAGS) -c $<

clean:
ifeq ($(OS),Windows_NT)
	del /Q *.o dcooke_parser*
else
	rm -f *.o dcooke_parser*
endif