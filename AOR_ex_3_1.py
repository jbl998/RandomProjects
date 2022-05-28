import gurobipy as gp
from gurobipy import GRB
import numpy as np
import datetime
start = datetime.datetime.now()
K = 5
qO = 1.2
qB = np.random.uniform(1.5, 2.2, K)
d = np.random.uniform(80, 120, K)
m = gp.Model("Exercise 3.1")
xSH = m.addVar(vtype = GRB.CONTINUOUS, name = "the amount shipped from the factory")
yB = m.addVars([i for i in range(K)], vtype = GRB.CONTINUOUS, name = "the amount bought in the local market")
yO = m.addVars([i for i in range(K)], vtype = GRB.CONTINUOUS, name = "the oversupply")
m.setObjective(xSH + 1/K * sum(qB[i]*yB[i]+qO*yO[i] for i in range(K)), GRB.MINIMIZE)
m.addConstr(xSH <= 100)                # Limit of shipment from factory
m.addConstr(xSH >= 0)                  # Must ship a positive amount from the factory
m.addConstrs(xSH+yB[i]-yO[i] == d[i] for i in range(K))   # Scenario constraints, ensure that demand is met
m.optimize()
end = datetime.datetime.now()
print('Time taken to run the calculations: ', end-start)
print('Objective value: ', m.getObjective().getValue())
print('qO: ', qO)
print('qB: ', qB, np.mean(qB))
print('d: ', d, np.mean(d))
print('xSH: ', xSH.x)

yBlist = []
for i in range(K):
    yBlist.append(yB[i].x)
print('yB:', yBlist)

yOlist = []
for i in range(K):
    yOlist.append(yO[i].x)
print('yO:', yOlist)
