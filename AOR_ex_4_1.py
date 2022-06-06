import numpy as np
import gurobipy as gp
from gurobipy import GRB



D1= [1,3,4]
D2 = [2,3,7]

# input

x1 = 0
x2 = 5

# Exercise 1
def Dual1():

    m1 = gp.Model("Dual1")
    k1 = m1.addVar(vtype = GRB.CONTINUOUS, ub = 1, lb = 0,name = "dual variable 1")
    k2 = m1.addVar(vtype = GRB.CONTINUOUS, ub = 1, lb = 0,name = "dual variable 2")
    k3 = m1.addVar(vtype = GRB.CONTINUOUS, ub = 0, lb = -1, name = "dual variable 3")
    k4 = m1.addVar(vtype = GRB.CONTINUOUS, ub = 0, lb = -1, name = "dual variable 4")

    m1.setObjective((d1-x1)*k1+(d2-x1-x2)*k2+k3+k4, GRB.MAXIMIZE)

    m1.addConstr(k1+k2+k3<=0)
    m1.addConstr(2*k1+k2+k4<=0)


    m1.optimize()

    print('k1:', k1.x)
    print('k2:', k2.x)
    print('k3:', k3.x)
    print('k4:', k4.x)

    print('obj:', m1.getObjective().getValue())
    return k1.x,k2.x,k3.x,k4.x,m1.getObjective().getValue()

FD = []
K = {}

for i in range(3):
    d1 = D1[i]
    d2 = D2[i]
    k1,k2,k3,k4,obj = Dual1()
    FD.append(obj)
    K[i] = [k1,k2,k3,k4]



m = gp.Model("MP")
x = m.addVars([i for i in range(1,3)], vtype = GRB.INTEGER, name = "Xs")
y = m.addVars([i for i in range(1,3)], vtype = GRB.INTEGER, name = "Ys")

m.setObjective(3*x[1] + 2*x[2] + 3*y[1] + y[2], GRB.MINIMIZE)
m.addConstr(x[1] + x[2] >= 5)


m.optimize()

print('x: ', x[1].x, x[2].x)
print('y: ', y[1].x, y[2].x)
