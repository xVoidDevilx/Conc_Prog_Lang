import argparse
from decryptLetter import decryptLetter
import re

"""
    @author: Silas Rodriguez
    @brief: uses regex to justify valid seeds
    @return: boolean for valid seed
    @param: seed - string to be regex compared
"""
def justifySeed(seed:str):
    assert type(seed) == str, 'Seed is not a string'
    pattern = re.compile('^[abc]+$')
    return bool(pattern.match(seed))

"""
    @author: Silas Rodriguez
    @brief: one time function to generate a nxn matrix using the input seed as a repeater
    @return: nxn matrix with repeated seed
    @param: n - integer, size of encrpyted string to be decrypted
    @param: seed - string to be regex compared
"""
def generateMatrix(n: int, seed: str):
    #Phase 1.2 : Generate the matrix
    matrix = [[seed[char % len(seed)] for char in range(row, row + n)] for row in range(0, n * n, n)]   # loop comprehension is very fast
    return matrix

"""
    @author: Silas Rodriguez
    @brief: computes a timestep of the matrix
    @return: generator object, itterate to get the timesteps
    @param: matrix - nxn matrix to compute time steps for in this cipher. Is overwritten
    @param hashgrid - dictionary mapping of seed: (value , function pairs)
"""
def timeStep(matrix:[[]], hashgrid:dict):
    # Phase 1.3: Matrix Processing
    possibleSums = {num for num in range(17)}
    primes = {2, 3, 5, 7, 11, 13}
    odds = {num for num in possibleSums if num % 2 == 1 and num not in primes}
    evens = possibleSums ^ primes ^ odds

    dimension = len(matrix)    # matrix must be square, so this will serve as the border position
    # Calculate the sum of neighboring cells
    neighbors_offsets = {(x,y) for x in range(-1,2) for y in range(-1,2) if (x,y) != (0,0)} # precompute vector table of all offsets from a cell
    while True:
        currentStep = [row[:] for row in matrix]   # creating a copy of the current matrix
        for i, row in enumerate(currentStep):
            for j, cell in enumerate(row):
                neighbors_sum = sum(hashgrid[currentStep[i + x][j + y]][0] for x, y in neighbors_offsets if 0 <= i + x < dimension and 0 <= j + y < dimension)
                matrix[i][j] = hashgrid[cell][1](prime=neighbors_sum in primes,even=neighbors_sum in evens)
        yield(matrix)

"""
    @author: Silas Rodriguez
    @brief: Pulls all the files, organizes data, writes to the screen
    @param: argv - argument vector from argparse. Used for parameters that control the program
"""
def main(argv:argparse.Namespace, *args, **kwargs):

    # Phase 1.1: Data Retrieval
    with open(argv.input, 'r') as inputFile:
        encrytped_str = inputFile.read()
    
    # try to open a file, otherwise, just set the string, then execute the matrix operations
    try:
        with open(argv.seed, 'r') as inputFile:
            seed = inputFile.read()
    except FileNotFoundError:
        seed = argv.seed
    finally:
        seed = seed.strip()     # do not lower case the seed, a!=A
        if not justifySeed(seed) or not len(seed) >= 1:
            raise ValueError('Seed can only contain [abc]+ !')
        if not argv.processes > 0:
            raise ValueError('processes must be greater than 0')
        process_count = argv.processes

        # Phase 1.2 - Matrix Generation
        matrix = generateMatrix(len(encrytped_str), seed)        

        # Phase 1.3: Matrix Processing
        hashGrid = {'a': (0, lambda prime,even: 'a' if prime else 'b' if even else 'c'),
                    'b': (1, lambda prime,even: 'b' if prime else 'c' if even else 'a'),
                    'c': (2, lambda prime,even: 'c' if prime else 'a' if even else 'b')}
        
        # use the generator to itterate through all the time steps, using enummerate, we can track the itterations since this is an infinite generator
        for step, matrix_step in enumerate(timeStep(matrix=matrix, hashgrid=hashGrid)):
            if step >= 99:
                break
                    
        # Phase 1.4 Decryption:
        col_sums = [sum(hashGrid[row[i]][0] for row in matrix) for i in range(len(matrix))]
        decryptedString = ''
        for i, col_sum in enumerate(col_sums):
            decryptedString += decryptLetter(encrytped_str[i], col_sum) # String concatenation

        # Write to Output File:
        with open(argv.output, 'w') as outFile:
            outFile.write(decryptedString)

if __name__ == '__main__':
    # Phase 1.1: Data Retrieval
    print('Project :: R11679913')

    parser = argparse.ArgumentParser(
        prog='main.py',
        description='Large Matrix Math',
        epilog='Silas Rodriguez, R11679913, TTU Computer Engineer, 2023'
                                     )
    parser.add_argument('-i', '--input',  required=True, help='input file containing encrypted string', type=str)
    parser.add_argument('-o', '--output', required=True, help='output file path to an existing directory', type=str)
    parser.add_argument('-s', '--seed',   required=True, help='retrieves a string that sets seed when starting matrix', type=str)
    parser.add_argument('-p', '--processes', required=False, default=1, help='how many processes to spawn to solve', type=int)
    
    argv = parser.parse_args()
    main(argv)