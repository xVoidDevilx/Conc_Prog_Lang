from time import sleep
def funcStep(matrix: [[]]):
    while True:
        currentStep = [row[:] for row in matrix]   # copy the current time step
        for i, row in enumerate(currentStep):
            for j, cell in enumerate(row):
                matrix[i][j] = currentStep[i][j] + 1
        
        yield matrix

matrix = [[1, 2, 3], [4,5,6], [7,8,9]]

for i in funcStep(matrix):

    for row in matrix:
        print(matrix)
    
    sleep(1)