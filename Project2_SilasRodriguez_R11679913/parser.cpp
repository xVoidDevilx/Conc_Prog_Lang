/*
=============================================================================
Title : parser.cpp
Description : This is part of a syntax analyzer program.
Author : silrodri (R#11679913)
Date : 10/19/2023
Version : 1.0
Usage : Compile and run this program using 'make' and ./dcooke_parser [file]
Notes : This program is dependent on the lexical analyzer program (main.cpp / dcooke_analyzer).
C++ Version : cpp (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)
=============================================================================
*/
#include <iostream>
#include "parser.h"
#include "front.h"

using std::cerr;
using std::cout;
using std::endl;

static void error(std::string details);
static exitCode shadowCode = NoError;

/**
 * @brief Handle statement call
 */
void statement()
{
    // Check which statement was entered:
    switch (nextToken)
    {
    // V = E
    case IDENT:
        lex(); // update lexeme
        if (nextToken == ASSIGN_OP)
        {
            lex();
            expr();
        }
        break;
    // read(IDENT) or write(IDENT) can be handled the same
    case KEY_READ:
    case KEY_WRITE:
        lex(); // update lexeme
        if (nextToken == LEFT_PAREN)
        {
            lex();
            // Must be an ident (V)
            if (nextToken == IDENT)
            {
                lex();
                // Missing close paren ?
                if (nextToken == RIGHT_PAREN)
                    lex();
                else
                    error("Expected ')'");
            }
        }
        // Missing left paren
        else if (shadowCode == NoError)
            error("Expected '('");
        break;
    // do {statements} while(conditional)
    case KEY_DO:
        lex();
        if (nextToken == LEFT_CBRACE)
        {
            lex();       // update lexeme
            statement(); // resolve statements
            if (nextToken == RIGHT_CBRACE)
                lex(); // move on
            else if (shadowCode == NoError)
                error("Expected '}'");
            // following c brace, need to see a while
            if (nextToken == KEY_WHILE)
            {
                lex(); // move on to next lexeme
                if (nextToken == LEFT_PAREN)
                {
                    lex();         // move into while
                    conditional(); // resolve conditional
                    if (nextToken == RIGHT_PAREN)
                        lex();
                    // missing close paren
                    else if (shadowCode == NoError)
                        error("Expected ')'");
                }
                // missing left paren
                else if (shadowCode == NoError)
                    error("Expected '('");
            }
            // missing while(conditional)
            else if (shadowCode == NoError)
                error("Expected 'while(conditional)'");
        }
        // Missing left cbrace
        else if (shadowCode == NoError)
            error("Expected '{'");
        break;
    // error last line statement entrance
    case EOF:
        error("Last line does not support semicolon ';'");
        break;
    // unsupported entrance - expected last statement no semicolon
    default:
        error("Expected a semicolon ';'");
        break;
    }
    // statement handled, check for semicolon
    if (nextToken == SEMICOLON)
    {
        lex();                // move on to next statement
        shadowCode = NoError; // Reset this so that next statement can track errors again
        statement();          // move s;s -> s
    }                         // Last statement doesn't need to reset shadowCode
}

/**
 * @brief Conditional: Return the checks for a conditional statment
 *  expr (op) expr
 */
void conditional()
{
    // enter expression
    expr();
    // check for correct comparator
    if (nextToken == EQUAL_OP || nextToken == NEQUAL_OP ||
        nextToken == GEQUAL_OP || nextToken == LEQUAL_OP ||
        nextToken == LESSER_OP || nextToken == GREATER_OP)
    {
        lex();
        expr();
    }
    // invalid comparator operator
    else if (shadowCode == NoError)
        error("Invalid Comparitor Operator");
}

/* expr
 * Parses strings in the language generated by the rule:
 * <expr> -> <term> {(+ | -) <term>}
 */
void expr()
{
    // call term
    term();
    // check for operations with other term; if any
    while (nextToken == ADD_OP || nextToken == SUB_OP)
    {
        lex();
        term();
    }
} /* End of function expr */

/* term
 * Parses strings in the language generated by the rule:
 * <term> -> <factor> {(* | /) <factor>)
 */
void term()
{
    // call factor
    factor();
    // check for operations with another factor; if any
    while (nextToken == MULT_OP || nextToken == DIV_OP)
    {
        lex();
        factor();
    }
    if (nextToken == UNKNOWN && shadowCode == NoError)
        error("Invalid Operation");
} /* End of function term */

/* factor
 * Parses strings in the language generated by the rule:
 * <factor> -> ( <expr> ) | IDENT(INC/DEC) | INT_LIT | IDENT
 */
void factor()
{
    // Determine which subtree to enter:
    switch (nextToken)
    {
    case LEFT_PAREN:
        lex();
        expr(); // resolve expression
        if (nextToken == RIGHT_PAREN)
            lex();
        // missing closing paren
        else if (shadowCode == NoError)
            error("Expected ')'");
        break;
    // V++, V--, or just V?
    case IDENT:
        lex();
        if (nextToken == INC_OP || nextToken == DEC_OP)
            lex();
        break;
    // Number
    case INT_LIT:
        lex(); // update lexeme
        break;
    // unsupported call to factor
    default:
        error("Unsupported call to factor");
        break;
    }
} /* End of function factor */

/**
 * @brief Error handler routine
 * @param details: String describing the problem for call
 */
static void error(std::string details)
{
    exit_code = shadowCode = SyntaxError;
    cout << "error detected: " << details << endl
         << lexeme << " was the next lexeme "
         << strNextToken << " was the next token" << endl;
}