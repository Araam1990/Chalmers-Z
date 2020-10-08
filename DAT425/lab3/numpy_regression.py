import sys
import matplotlib.pyplot as plt
from numpy import *

def powers(matrix, a, b):
    output = []
    for row in matrix:
        row_output = []
        for n in range(a, b+1):
            row_output.append(row**n)
        output.append(row_output)
    return array(output)

def poly(a, x):
    value  = 0
    for n in range(len(a)):
        value += a[n] * x**n
    return value

data = loadtxt(sys.argv[1])

X = data[:,0]
Y = data[:,1]

n = int(sys.argv[2])

Xp  = powers(X,0,n)
Yp  = powers(Y,1,1)
Xpt = Xp.transpose()

a = matmul(linalg.inv(matmul(Xpt,Xp)),matmul(Xpt,Yp))
a = a[:,0]

min, max = [X[0], X[-1]]
pointCount = int((max-min)/0.2)
X2 = linspace(min, max, pointCount).tolist()
Y2 = list(map(lambda x: poly(a, x), X2))

plt.plot(X,Y, 'ro')
plt.plot(X2,Y2)

plt.show()