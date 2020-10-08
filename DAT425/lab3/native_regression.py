import matplotlib.pyplot as plt

from matrix import *

data = loadtxt("chirps.txt")

X, Y = [], []

for row in data:
    X.append(float(row[0]))
    Y.append(float(row[1]))


Xp  = powers(X,0,1)
Yp  = powers(Y,1,1)
Xpt = transpose(Xp)

[[b],[m]] = matmul(invert(matmul(Xpt,Xp)),matmul(Xpt,Yp))

Y2 = list(map(lambda x: b + m * x, X))

plt.plot(X,Y, 'ro')
plt.plot(X,Y2)

plt.show()