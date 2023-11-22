#!/usr/bin/env python3
"""
=============================================================================
Title : Silas_Rodriguez_R11679913_final_project.py
Description : This script utilizes multiprocessing to perform vector calculations on a large matrix, decrypting an encrypted string.
Author : Silas Rodriguez (R#1167913)
Date : 11/22/2023
Version : 1.0
Usage : python Silas_Rodriguez_R11679913_final_project.py -i INPUT_FILE -s SEED -o OUTPUT_FILE -p NUM_PROCESSES
Notes : This example script has no requirements - written in base python.
Python Version: 3.9.12 +
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
    @brief: one time function to generate a n^2 vector using the input seed as a repeater
    @return: n^2 vector with repeated seed
    @param: 
        -n (integer): size of encrpyted string to be decrypted
        -seed (str) : string to be regex validated
"""
def generateVector(n: int, seed: str):
    # Generate the vector directly
    vector = [seed[char % len(seed)] for char in range(n * n)]
    return vector
    flattened_vector = [char for row in matrix for char in row]
    return flattened_vector

"""
    @author: Silas Rodriguez
    @brief: computes a timestep of the matrix
    @return: None
    @param:
        - vector (list): The input vector.
        - dim (int): The dimension of the square array.
        - chunk (tuple): The range of indices to process.
        - hashgrid (dict): A dictionary representing the hashgrid for vector processing.
    @post: vector_w is updated with the chunk section assigned to process
"""
def timeStepScatter(args:tuple):
    vector, dim, chunk, hashgrid= args
    start, stop = chunk # unpack the range
    totalCells = len(vector)    # get the total elements

    dim_p1 = dim+1
    dim_m1 = dim-1
    """
        This needs explaining:
        right, left, bottom, top, bottom-right corner, top-left corner, top-right corner, and bottom-left corner neighbors.
        Pre computing these 8 values based on the properties of a square matrix, one can QUICKLY access the possible neighbors of the 3 (corner), 5 (edge), or 8 (center) neighbors
        any one cell can have by setting booleans when checking in order
    """
    changes = []
    for i in range(start, stop):
        # compass[key][0] = index of offset
        # compass[key][1] = bool to bother adding
        compass_base = { 
        'right':  (i+1, i % dim != dim-1),
        'left':   (i-1, i % dim != 0),
        'bottom': (i+dim, i + dim < totalCells),
        'top':    (i-dim, i - dim >= 0)}
        compass_corners = {
        'brc':    (i + (dim_p1), compass_base['right'][1] and compass_base['bottom'][1]),
        'blc':    (i + (dim_m1), compass_base ['left'][1] and compass_base['bottom'][1]),
        'tlc':    (i + -(dim_p1), compass_base['left'][1] and compass_base['top'][1]),
        'trc':    (i + -(dim_m1), compass_base['right'][1] and compass_base['top'][1])}
        compass_base.update(compass_corners)

        # compute the sum of the neighbors + write to the output vector
        sum_neighbors = 0
        for offset, compute in compass_base.values():
            if compute:
                sum_neighbors += hashgrid[vector[offset]][0]
        # append to the changes to be made
        changes.append(hashgrid[vector[i]][1](sum_neighbors in hashgrid['primes'], sum_neighbors in hashgrid['evens']))

    # return a tuple for chunk edited, and changes to be cast
    return (start, stop, changes)

"""
    @author: Silas Rodriguez
    @brief: handles processes
    @return: final cipher matrix
"""
def run_vector_processing(args: tuple):
    vector, dim, ranges, hashGrid, process_count = args
    with Pool(process_count) as pool:
        for _ in range(100):
            # Only necessary information to the worker processes - each worker knows their chunk, so order will not matter
            results = tuple(pool.imap_unordered(timeStepScatter, [(vector, dim, chunk, hashGrid) for chunk in ranges]))    # Trick I learned: tuple (imap) forces the computations instead of being lazy

            for result in results:
                start, stop, changes = result
                vector[start:stop] = changes
    return tuple(vector)

"""
    @brief: computes the chunks for each process
    @return: set of tuples for each process to itterate over {(start, stop)}
    @param: 
        - dim (int): the dimension of the square array
        - process_count (int): amount of processes that the program will run
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
    @brief: Pulls all the files, organizes data, writes to the screen
    @post: file to output with cipher decrypted
    @param: argv - argument vector from argparse. Used for parameters that control the program
"""
def main(argv: argparse.Namespace, *args, **kwargs):

    # Phase 1.1: Data Retrieval
    with open(argv.input, encoding='ascii') as inputFile:
        encrypted_str = inputFile.read().strip()  # cleans whitespace trailing and leading

    # try to open a file, otherwise, just set the string, then execute the matrix operations
    try:
        with open(argv.seed, 'r', encoding='ascii') as seedFile:
            seed = seedFile.read().strip()
    except FileNotFoundError:
        seed = argv.seed
    finally:
        seed = seed.strip()
        if not justifySeed(seed) or not len(seed) >= 1:
            raise ValueError('Seed can only contain [abc]+!')

        # Phase 1.2 - Matrix Generation
        dim = len(encrypted_str)
        if not argv.processes > 0:
            raise ValueError('Processes must be greater than 0')
        process_count = argv.processes

        ranges = generateChunkPairs(dim=dim, process_count=process_count)
        vector = generateVector(dim, seed)

        # Phase 1.3: Matrix Processing
        possible_sums = {num for num in range(17)}   # 16 is the max of 8 c neighbors * 2 = 16.
        primes = {2, 3, 5, 7, 11, 13}
        odds = {num for num in possible_sums if num % 2 == 1 and num not in primes}
        evens = possible_sums ^ primes ^ odds
        # generate a hashgrid to make processing matrix way easier
        hashGrid = {'a': (0, hashgrid_function_a),
                    'b': (1, hashgrid_function_b),
                    'c': (2, hashgrid_function_c),
                    'primes': primes,
                    'evens': evens}
        del possible_sums
        del primes
        del odds
        del evens

        vector = run_vector_processing((vector, dim, ranges, hashGrid, process_count))

        # reassemble the matrix
        matrix_re = [vector[i:i + dim] for i in range(0, len(vector), dim)]

        # # Phase 1.4 Decryption:
        col_sums = [sum(hashGrid[row[i]][0] for row in matrix_re) for i in range(len(matrix_re))]
        decrypted_string = ''
        for letter in decryptLetter(encrypted_str, col_sums):
            decrypted_string += letter

        # Write to Output File:
        with open(argv.output, 'w', encoding='ascii') as outFile:
            decrypted_string = decrypted_string.strip() # remove leading and trailing whitespace
            outFile.write(decrypted_string)

"""
    @brief: starts the program with processes in mind
    @return: None
"""
if __name__ == '__main__':
    # Phase 1.1: Data Retrieval
    print('Project :: R11679913')

    parser = argparse.ArgumentParser(
        prog='Silas_Rodriguez_R11679913_final_project.py',
        description='Vector Decrypter Tool',
        epilog='Silas Rodriguez, R11679913, TTU Computer Engineer, 2023'
                                     )
    parser.add_argument('-i', '--input',  required=True, help='input file containing encrypted string', type=str)
    parser.add_argument('-o', '--output', required=True, help='output file path to an existing directory', type=str)
    parser.add_argument('-s', '--seed',   required=True, help='retrieves a string that sets seed when starting matrix', type=str)
    parser.add_argument('-p', '--processes', required=False, default=1, help='how many processes to spawn', type=int)
    
    argv = parser.parse_args()
    
    main(argv)