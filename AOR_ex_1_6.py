import gurobipy as gp
from gurobipy import GRB
import datetime
start = datetime.datetime.now()
m = gp.Model("Problem 6")
#self.m.Params.Timelimit = 300
#self.m.Params.MIPGap = 0.0
x_SH = m.addVar(vtype = GRB.INTEGER, name = "the amount shipped from the factory")
y_B = m.addVars([i for i in range(1,4)], vtype = GRB.INTEGER, name = "the amount bought in the local market")
y_O = m.addVars([i for i in range(1,4)], vtype = GRB.INTEGER, name = "the oversupply")
m.setObjective(x_SH + 0.3*(1.5*y_B[1] + 1.2*y_O[1]) + 0.3*(1.7*y_B[2] + 1.2*y_O[2]) + 0.4*(2.0*y_B[3] + 1.2*y_O[3]),
               GRB.MINIMIZE)
m.addConstr(x_SH <= 100)                # Limit of shipment from factory
m.addConstr(x_SH >= 0)                  # Must ship a positive amount from the factory
m.addConstr(y_B[1]-y_O[1]+x_SH == 85)   # Scenario 1 constraint, ensure that demand is met
m.addConstr(y_B[2]-y_O[2]+x_SH == 105)  # Scenario 2 constraint, ensure that demand is met
m.addConstr(y_B[3]-y_O[3]+x_SH == 120)  # Scenario 3 constraint, ensure that demand is met

m.optimize()

end = datetime.datetime.now()
print('Time taken to run the calculations: ', end-start)

print('x_SH: ', x_SH.x)
print('y_B:', y_B[1].x, y_B[2].x, y_B[3].x)
print('y_O:', y_O[1].x, y_O[2].x, y_O[3].x)
