#include <iostream>
#include <cctype>
#include <cstring>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <iomanip>

#include "front.h"
#include "parser.h"

/* Global Variable */
int nextToken;

/* Local Variables */
static int charClass;
static char lexeme[100];
static std::string strNextToken;
static char nextChar;
static int lexLen;
static FILE *in_fp;

/* Local Function declarations */
static void addChar();
static void getChar();
static void getNonBlank();
static void retDirective(int Token);

using std::cerr;
using std::endl;

/******************************************************/
/* lookup - a function to lookup operators and parentheses and return the
 * token */
static int lookup(char ch)
{
    switch (ch)
    {
    case '(':
        addChar();
        nextToken = LEFT_PAREN;
        break;
    case ')':
        addChar();
        nextToken = RIGHT_PAREN;
        break;
    case '{':
        addChar();
        nextToken = LEFT_CBRACE;
        break;
    case '}':
        addChar();
        nextToken = RIGHT_CBRACE;
        break;
    // could be INC_OP or ADD_OP
    case '+':
        addChar(); // push into lexeme
        getChar(); // check next char
        if (nextChar == '+')
        {
            nextToken = INC_OP;
            addChar();
        }
        else
            nextToken = ADD_OP;
        break;
    // could be DEC_OP or ADD_OP
    case '-':
        addChar(); // push into lexeme
        getChar(); // check next char
        if (nextChar == '-')
        {
            nextToken = DEC_OP;
            addChar();
        }
        else
            nextToken = SUB_OP;
        break;
    // could be ASSIGN_OP or EQUAL_OP
    case '=':
        addChar(); // push into lexeme
        getChar(); // check next char
        if (nextChar == '=')
        {
            nextToken = EQUAL_OP;
            addChar();
        }
        // add a bool or back up a file pointer
        else
            nextToken = ASSIGN_OP;
        break;
    case '*':
        addChar();
        nextToken = MULT_OP;
        break;
    case '/':
        addChar();
        nextToken = DIV_OP;
        break;
    case ';':
        addChar();
        nextToken = SEMICOLON;
        break;
    default:
        addChar();
        nextToken = EOF;
        break;
    }
    return nextToken;
}

/*****************************************************/
/* addChar - a function to add nextChar to lexeme */
static void addChar()
{
    if (lexLen <= 98)
    {
        lexeme[lexLen++] = nextChar;
        lexeme[lexLen] = 0;
    }
    else
        cerr << "Error - lexeme is too long" << endl;
}

/*****************************************************/
/* getChar - a function to get the next character of input and determine its
 * character class */
static void getChar()
{
    if ((nextChar = getc(in_fp)) != EOF)
    {
        if (std::isalpha(nextChar))
            charClass = LETTER;
        else if (std::isdigit(nextChar))
            charClass = DIGIT;
        else
            charClass = UNKNOWN;
    }
    else
        charClass = EOF;
}

/*****************************************************/
/* getNonBlank - a function to call getChar until it returns a non-whitespace
 * character */
static void getNonBlank()
{
    while (std::isspace(nextChar))
        getChar();
}

/*****************************************************/
/* lex - a simple lexical analyzer for arithmetic expressions */
int lex()
{
    lexLen = 0;
    getNonBlank();

    switch (charClass)
    {
    /* Parse identifiers */
    case LETTER:
        addChar();
        getChar();
        while (charClass == LETTER || charClass == DIGIT)
        {
            addChar();
            getChar();
        }
        // read(V)
        if (strcmp(lexeme, "read") == 0)
            nextToken = KEY_READ;
        else if (strcmp(lexeme, "write") == 0)
            nextToken = KEY_WRITE;
        else if (strcmp(lexeme, "while") == 0)
            nextToken = KEY_WHILE;
        else if (strcmp(lexeme, "do") == 0)
            nextToken = KEY_DO;
        else
            nextToken = IDENT;
        break;

    /* Parse integer literals */
    case DIGIT:
        addChar();
        getChar();
        while (charClass == DIGIT)
        {
            addChar();
            getChar();
        }
        nextToken = INT_LIT;
        break;

    /* Parentheses and operators */
    case UNKNOWN:
        lookup(nextChar);
        getChar();
        break;

    /* EOF */
    case EOF:
        nextToken = EOF;
        lexeme[0] = 'E';
        lexeme[1] = 'O';
        lexeme[2] = 'F';
        lexeme[3] = 0;
        break;
    } /* End of switch */

    // if not the end of file, print the lexeme and token, but always return    -
    if (!strcmp(lexeme, "EOF") == 0)
    {
        retDirective(nextToken); // update strNext Token
        std::cout << std::left << std::setw(10) << lexeme << strNextToken << endl;
    }
    return nextToken;
} /* End of function lex */

int main(int argc, char **argv)
{
    std::cout << "DCooke Analyzer :: R11679913" << endl;

    if (argc != 2)
    {
        cerr << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }

    if ((in_fp = fopen(argv[1], "r")) == nullptr)
    { // Open the file specified as a command-line argument
        cerr << "ERROR - cannot open " << argv[1] << endl;
        return 1;
    }
    else
    {
        getChar();
        do
        {
            lex();
            // You can call other functions like expr() here if needed.
        } while (nextToken != EOF);
    }

    fclose(in_fp); // Close the file when done
    return 0;
}

// Add a function to map int to string to directive
static void retDirective(int Token)
{
    switch (Token)
    {
    case ASSIGN_OP:
        strNextToken = "ASSIGN_OP";
        break;
    case LESSER_OP:
        strNextToken = "LESSER_OP";
        break;
    case GREATER_OP:
        strNextToken = "GREATER_OP";
        break;
    case EQUAL_OP:
        strNextToken = "EQUAL_OP";
        break;
    case NEQUAL_OP:
        strNextToken = "NEQUAL_OP";
        break;
    case LEQUAL_OP:
        strNextToken = "LEQUAL_OP";
        break;
    case GEQUAL_OP:
        strNextToken = "GEQUAL_OP";
        break;
    case SEMICOLON:
        strNextToken = "SEMICOLON";
        break;

    case ADD_OP:
        strNextToken = "ADD_OP";
        break;
    case SUB_OP:
        strNextToken = "SUB_OP";
        break;
    case MULT_OP:
        strNextToken = "MULT_OP";
        break;
    case DIV_OP:
        strNextToken = "DIV_OP";
        break;
    case INC_OP:
        strNextToken = "INC_OP";
        break;
    case DEC_OP:
        strNextToken = "DEC_OP";
        break;
    case LEFT_PAREN:
        strNextToken = "LEFT_PAREN";
        break;
    case RIGHT_PAREN:
        strNextToken = "RIGHT_PAREN";
        break;

    case LEFT_CBRACE:
        strNextToken = "LEFT_CBRACE";
        break;
    case RIGHT_CBRACE:
        strNextToken = "RIGHT_CBRACE";
        break;
    case KEY_READ:
        strNextToken = "KEY_READ";
        break;
    case KEY_WRITE:
        strNextToken = "KEY_WRITE";
        break;
    case KEY_WHILE:
        strNextToken = "KEY_WHILE";
        break;
    case KEY_DO:
        strNextToken = "KEY_DO";
        break;
    case IDENT:
        strNextToken = "IDENT";
        break;
    case INT_LIT:
        strNextToken = "INT_LIT";
        break;
    default:
        strNextToken = "UNKNOWN";
        break;
    }
}