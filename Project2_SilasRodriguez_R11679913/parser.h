/*
=============================================================================
Title : parser.cpp
Description : This is a header file for the syntax analyzer program.
Author : silrodri (R#11679913)
Date : 10/19/2023
Version : 1.0
Usage : For project 2, this is imported into the lexical and syntax analyzer
Notes : This program is dependent on the lexical analyzer program (main.cpp / dcooke_analyzer).
C++ Version : cpp (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)
=============================================================================
*/
#ifndef PARSER_H
#define PARSER_H

void expr();
void term();
void factor();
void statement();
void conditional();

extern int nextToken;
extern std::string strNextToken;
extern char lexeme[100];

/**
 * @brief : Exit codes the program execution will see upon exit
 */
typedef enum exitCodes
{
    NoError,
    SyntaxError,
    MissingFile,
    FileNotFound
} exitCode;

extern exitCode exit_code;

#endif
