#include <iostream>
#include <cctype>

#include "front.h"
#include "parser.h"

/* Global Variable */
int nextToken;

/* Local Variables */
static int charClass;
static char lexeme[100];
static char nextChar;
static int lexLen;
static FILE *in_fp;

/* Local Function declarations */
static void addChar();
static void getChar();
static void getNonBlank();

using std::cerr;
using std::cout;
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
        nextToken = LEFT_BRACK;
        break;
    case '}':
        addChar();
        nextToken = RIGHT_BRACK;
        break;
    case '+':
        addChar();
        nextToken = ADD_OP;
        break;
    case '-':
        addChar();
        nextToken = SUB_OP;
        break;
    case '=':
        addChar();
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
        nextToken = SEMICOL;
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
    {
        cerr << "Error - lexeme is too long" << endl;
    }
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
    {
        charClass = EOF;
    }
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

    cout << "Next token is: " << nextToken << ", Next lexeme is " << lexeme << endl;
    return nextToken;
} /* End of function lex */

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }

    if ((in_fp = fopen(argv[1], "r")) == nullptr)
    { // Open the file specified as a command-line argument
        std::cerr << "ERROR - cannot open " << argv[1] << std::endl;
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
