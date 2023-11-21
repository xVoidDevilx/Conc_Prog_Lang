#!/usr/bin/env python3
"""
=============================================================================
Title : pool.py
Description : This will spawn a pool of processes to use the worker function to perform vector calculations.
Author : Silas Rodriguez (R#1167913)
Date : 11/20/2023
Version : 1.0
Usage : [python3, py, python] -i (input_file) -s (seed) -o (output_file) -p [# of processes]
Notes : This example script has no requirements - written in base python.
Python Version: 3.4.8 +
=============================================================================
"""
from multiprocessing import Pool
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
    @brief: flatten the matrix into a vector
    @return: n**2 len vector
    @param: matrix - nxn matrix to be flattened
"""
def flattenMatrix(matrix: [[]]):
    flattened_vector = [char for row in matrix for char in row]
    return flattened_vector

"""
    @author: Silas Rodriguez
    @brief: computes a timestep of the matrix
    @return: generator object, itterate to get the timesteps
    @param: matrix - nxn matrix to compute time steps for in this cipher. Is overwritten
    @param: hashgrid - dictionary mapping of seed: (value , function pairs)
    @param: chunk: value range the process will compute over
"""
def timeStepScatter(args:tuple):
    vector, dim, chunk, hashgrid = args  # unpack the arguments
    start, stop = chunk # unpack the range
    totalCells = len(vector)    # get the total elements
    currentStep = vector[start:stop]    # create a copy

    """
        This needs explaining:
        right, left, bottom, top, bottom-right corner, top-left corner, top-right corner, and bottom-left corner neighbors.
        Pre computing these 8 values based on the properties of a square matrix, one can QUICKLY access the possible neighbors of the 3 (corner), 5 (edge), or 8 (center) neighbors
        any one cell can have by setting booleans when checking in order ... buckle up bukaroo
    """
    for i in range(start, stop):
        # compass[key][0] = index of offset
        # compass[key][1] = bool to bother adding
        compass_base = { 
        'right':  (i+1, i % dim != dim-1),
        'left':   (i-1, i % dim != 0),
        'bottom': (i+dim, i + dim < totalCells),
        'top':    (i-dim, i - dim >= 0)}
        compass_corners = {
        'brc':    (i + (dim+1), compass_base['right'][1] and compass_base['bottom'][1]),
        'blc':    (i + (dim-1), compass_base ['left'][1] and compass_base['bottom'][1]),
        'tlc':    (i + -(dim+1), compass_base['left'][1] and compass_base['top'][1]),
        'trc':    (i + -(dim-1), compass_base['right'][1] and compass_base['top'][1])}
        compass_base.update(compass_corners)

        sum_neighbors = 0
        for key, (offset, compute) in compass_base.items():
            if compute:
                sum_neighbors+=hashgrid[vector[offset]][0]
            currentStep[i-start] = hashgrid[vector[i]][1](sum_neighbors in hashgrid['primes'],
                                                           sum_neighbors in hashgrid['evens'])
    
    post = {
        'start': start,
        'stop':stop,
        'vector':currentStep
    }
    return post
"""
    @author: Silas Rodriguez
    @brief: handles processes
    @return: final cipher matrix
"""
def run_vector_processing(args: tuple):
    vector, dim, ranges, hashGrid, process_count = args
    with Pool(process_count) as pool:
        for _ in range(100):
            # Only pass the necessary information to the worker processes
            results = pool.imap(timeStepScatter, [(vector[:], dim, chunk, hashGrid) for chunk in ranges])
            # reassemble the vector being scattered
            for result in results:
                start, stop, sliced = result['start'], result['stop'], result['vector']
                vector[start:stop] = sliced
    return vector

"""
    @author: Silas Rodriguez
    @brief: computes the chunks for each process
    @return: ranges for each process to itterate over (startRow, startCol, stopRow, StopCol)
    @param: dim - the dimension of the square array
    @param: process_count: amount of processes that the program will run
"""
def generateChunkPairs(dim: int, process_count: int):
    assert process_count <= dim**2, 'More Processes than work to do...'
    # Calculate the cells per chunk & return the steps
    cells_per_process = dim**2 // process_count
    remaining_cells = dim**2 % process_count

    chunks = []
    start_index = 0
    for process in range(process_count):
        end_index = start_index + cells_per_process + (1 if process < remaining_cells else 0)
        chunks.append((start_index, end_index))
        start_index = end_index

    return set(chunks)

"""
    This needed to be defined because lambda functions cannot be pickled
"""
def hashgrid_function_a(prime:set, even:set):
    return 'a' if prime else 'b' if even else 'c'
def hashgrid_function_b(prime:set, even:set):
    return 'b' if prime else 'c' if even else 'a'
def hashgrid_function_c(prime:set, even:set):
    return 'c' if prime else 'a' if even else 'b'

"""
    @author: Silas Rodriguez
    @brief: Pulls all the files, organizes data, writes to the screen
    @return: file to output with cipher decrypted
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

        # Phase 1.2 - Matrix Generation
        dim = len(encrytped_str)
        matrix = generateMatrix(dim, seed)        

        # Phase 1.3: Matrix Processing
        if not argv.processes > 0:
            raise ValueError('processes must be greater than 0')
        process_count = argv.processes
        
        ranges = generateChunkPairs(dim=dim, process_count=process_count)
        vector = flattenMatrix(matrix)

        possibleSums = {num for num in range(17)}   # 16 is the max of 8 c neighbors * 2 = 16.
        primes = {2, 3, 5, 7, 11, 13}
        odds = {num for num in possibleSums if num % 2 == 1 and num not in primes}
        evens = possibleSums ^ primes ^ odds
        # generate a hashgrid to make processing matrix way easier
        hashGrid = {'a': (0, hashgrid_function_a),
                    'b': (1, hashgrid_function_b),
                    'c': (2, hashgrid_function_c),
                    'primes': primes,
                    'evens': evens}
        del possibleSums; del primes; del odds; del evens

        vector = run_vector_processing((vector, dim, ranges, hashGrid, process_count))

        # reassemble the matrix
        matrix_re = [vector[i:i+dim] for i in range(0, len(vector), dim)]

        # # Phase 1.4 Decryption:
        col_sums = [sum(hashGrid[row[i]][0] for row in matrix_re) for i in range(len(matrix_re))]
        decryptedString = ''
        for i, col_sum in enumerate(col_sums):
            decryptedString += decryptLetter(encrytped_str[i], col_sum) # String concatenation

        # Write to Output File:
        with open(argv.output, 'w') as outFile:
            outFile.write(decryptedString)

"""
    @author: Silas Rodriguez
    @brief: starts the program smoothly with processes in mind
    @return: None
"""
if __name__ == '__main__':
    # Phase 1.1: Data Retrieval
    print('Project :: R11679913')

    parser = argparse.ArgumentParser(
        prog='Silas_Rodriguez_R11679913_final_project.py',
        description='Large Matrix Math',
        epilog='Silas Rodriguez, R11679913, TTU Computer Engineer, 2023'
                                     )
    parser.add_argument('-i', '--input',  required=True, help='input file containing encrypted string', type=str)
    parser.add_argument('-o', '--output', required=True, help='output file path to an existing directory', type=str)
    parser.add_argument('-s', '--seed',   required=True, help='retrieves a string that sets seed when starting matrix', type=str)
    parser.add_argument('-p', '--processes', required=False, default=1, help='how many processes to spawn', type=int)
    
    argv = parser.parse_args()
    
    main(argv)