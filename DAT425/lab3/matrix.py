def transpose(matrix):
    rows = len(matrix)
    if len(matrix) == 0:
        return []

    cols = len(matrix[0])

    output = []

    for col in range(cols):
        r = []

        for row in range(rows):
            r.append(matrix[row][col])
        output.append(r)

    return output

def powers(matrix, a, b):
    output = []
    for row in matrix:
        row_output = []
        for n in range(a, b+1):
            row_output.append(row**n)
        output.append(row_output)
    return output

def matmul(matrix1, matrix2):
    if len(matrix1) == 0 or len(matrix2) == 0:
        return []
    if len(matrix1[0]) == 0 or len(matrix2[0]) == 0:
        return []

    output = []

    n, k_1 = [len(matrix1), len(matrix1[0])]
    k_2, m = [len(matrix2), len(matrix2[0])]

    for row in range(n):
        output_row = []
        for col in range(m):

            l1 = len(matrix1[row])
            l2 = len(matrix2)

            sum = 0

            for x in range(0, min(l1, l2)):
                sum += matrix1[row][x] * matrix2[x][col]

            output_row.append(sum)

        output.append(output_row)
    return output

def invert(matrix):
    [ [a, b], [c, d] ] = matrix
    det = a * d - b * c

    return [
        [d/det, -b/det],
        [-c/det, a/det]
    ]

def loadtxt(name):
    file = open(name)
    rows = []

    for line in file:
        rows.append(line.split())

    return rows