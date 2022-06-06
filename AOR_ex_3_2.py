import gurobipy as gp
from gurobipy import GRB
import numpy as np
import datetime
import scipy.stats
start = datetime.datetime.now()

M = 7
K = 5
a = 0.1
sol = []
z_k = []
for i in (range(M)):
    qO = 1.2                            # qO is deterministic, the same for each scenario
    qB = np.random.uniform(1.5,2.2,K)   # Draw K iid RVs with Uniform distribution
    d = np.random.uniform(80,120,K)     # Draw K iid RVs with Uniform distribution
    m = gp.Model("Exercise 3.2")
    m.Params.LogToConsole = 0
    xSH = m.addVar(vtype = GRB.CONTINUOUS, name = "the amount shipped from the factory")
    yB = m.addVars([i for i in range(0,K)], vtype = GRB.CONTINUOUS, name = "the amount bought in the local market")
    yO = m.addVars([i for i in range(0,K)], vtype = GRB.CONTINUOUS, name = "the oversupply")
    m.setObjective(xSH + 1/K * sum(qB[i]*yB[i]+qO*yO[i] for i in range(K)), GRB.MINIMIZE)
    m.addConstr(xSH <= 100)                                     # Limit of shipment from factory
    m.addConstr(xSH >= 0)                                       # Must ship a positive amount from the factory
    m.addConstrs(xSH+yB[i]-yO[i] == d[i] for i in range(K))     # Scenario constraints, ensure that demand is met
    m.optimize()
    sol.append(xSH.x)
    z_k.append(m.getObjective().getValue())
    print('Iteration', i+1, 'complete')
end = datetime.datetime.now()


print('Time taken to run the calculations: ', end-start)
L_KM = 1/M * sum(z_k)
zeta = scipy.stats.norm.ppf(1-a)
print('L_KM: ', L_KM)
sigma_est = (1/(M-1) * sum((z_k[x]-L_KM)**2 for x in range(M)))**(1/2)
print('sigma: ', sigma_est)
print('CI, lower bound: (',round(L_KM-zeta*sigma_est/np.sqrt(M),2),',',round(L_KM+zeta*sigma_est/np.sqrt(M),2),')')

