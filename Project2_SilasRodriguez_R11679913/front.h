/*
=============================================================================
Title : front.h
Description : This is a header for the lexical analyzer program.
Author : silrodri (R#11679913)
Date : 10/19/2023
Version : 1.0
Usage : Imported into main.cpp and parser.cpp
Notes : This example program has no requirements.
C++ Version : cpp (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)
=============================================================================
*/
#ifndef FRONT_H
#define FRONT_H

/* Character classes */
#define LETTER 0
#define DIGIT 1
#define UNKNOWN 99

/* Token codes */
#define ASSIGN_OP 10
#define LESSER_OP 11
#define GREATER_OP 12
#define EQUAL_OP 13
#define NEQUAL_OP 14
#define LEQUAL_OP 15
#define GEQUAL_OP 16
#define SEMICOLON 17

#define ADD_OP 18
#define SUB_OP 19
#define MULT_OP 20
#define DIV_OP 21
#define INC_OP 22
#define DEC_OP 23
#define LEFT_PAREN 24
#define RIGHT_PAREN 25

#define LEFT_CBRACE 26
#define RIGHT_CBRACE 27
#define KEY_READ 28
#define KEY_WRITE 29
#define KEY_WHILE 30
#define KEY_DO 31
#define IDENT 32
#define INT_LIT 33

int lex();

#endif
