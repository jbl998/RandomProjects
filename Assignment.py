from inspect import _void
import numpy as np
from gurobipy import GRB, Model
print("Kristian Kofoed Mortensen (JBL998)\n"
      "Advanced Operations Research \n"
      "Practical assignment June 8th")
# Setting seed to ensure replicability
np.random.seed(10)

##### TASK 2 #####

def TaskTwoUpperBound(M,K)->(_void):
    objV=np.zeros(M)    # Object value vector
    c1 = 2; c2 = 4; c3 = 5.2  # Cost of procurement
    q1 = 60; q2 = 40; q3 = 10 # Selling price
    for m in range(M):
        # Creating the model
        Prod = Model("Production")
        Prod.Params.LogToConsole = 0
        # Assigning the variables
        x1 = Prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x1')     # Procurement of resource 1
        x2 = Prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x2')     # Procurement of resource 2
        x3 = Prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x3')     # Procurement of resource 3

        y1 = Prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y1')     # Produced of product 1
        y2 = Prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y2')     # Produced of product 2
        y3 = Prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y3')     # Produced of product 3

        # Drawing random samples
        d1 = np.random.uniform(50, 250, K)  # Demand ~ U(50,250)
        d2 = np.random.uniform(20, 250, K)  # Demand ~ U(50,250)
        d3 = np.random.uniform(200, 500, K) # Demand ~ U(50,250)

        # Setting objective function
        Prod.setObjective(sum([q1*y1[k] + q2*y2[k] + q3*y3[k] for k in range(K)]) / K - c1*x1 - c2*x2 - c3*x3,
                          sense=GRB.MAXIMIZE)

        # Adding constraints
        Prod.addConstrs(x1 >= 8 * y1[k] + 6 * y2[k] + 1 * y3[k] for k in range(K))      # Use less than procured, resource 1
        Prod.addConstrs(x2 >= 4 * y1[k] + 2 * y2[k] + 1.5 * y3[k] for k in range(K))    # Use less than procured, resource 2
        Prod.addConstrs(x3 >= 2 * y1[k] + 1.5 * y2[k] + 0.5 * y3[k] for k in range(K))  # Use less than procured, resource 3
        Prod.addConstrs(y1[k] <= d1[k] for k in range(K))   # Produce less than demand, product 1
        Prod.addConstrs(y2[k] <= d2[k] for k in range(K))   # Produce less than demand, product 2
        Prod.addConstrs(y3[k] <= d3[k] for k in range(K))   # Produce less than demand, product 3

        # Optimizing
        Prod.optimize(callback=None)
        objV[m] = Prod.ObjVal

    U_KM = np.mean(objV)
    sigma_U = np.sqrt(sum([np.power(objV[m]-U_KM,2) for m in range(M)])/(M-1))
    print('M =', M ,', K =', K ,'Upper bound with 95% confidence bands:',
          U_KM+(sigma_U*1.96/np.sqrt(M))*np.array([-1,0,1]))
    # Print for latex copy
    # print('$',round(U_KM,2),'\pm',round(sigma_U*1.96/np.sqrt(M),2),'$\n')

# Getting upper bounds for different values of M and K
TaskTwoUpperBound(5, 5)
# TaskTwoUpperBound(5, 50)
# TaskTwoUpperBound(5, 500)
# TaskTwoUpperBound(50, 5)
# TaskTwoUpperBound(50, 50)
# TaskTwoUpperBound(50, 500)
# TaskTwoUpperBound(500, 5)
# TaskTwoUpperBound(500, 50)
# TaskTwoUpperBound(500, 500)

##### TASK 3 #####

def TaskThreeApproximation(K)->(_void):
    c1=2; c2=4; c3=5.2  # Cost of procurement
    q1=60; q2=40; q3=10 # Selling price
    # Creating the model
    prod = Model("Production")
    prod.Params.LogToConsole = 0
    # Assigning the variables
    x1 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x1')     # Procurement of resource 1
    x2 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x2')     # Procurement of resource 2
    x3 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x3')     # Procurement of resource 3

    y1 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y1')     # Produced of product 1
    y2 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y2')     # Produced of product 2
    y3 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y3')     # Produced of product 3

    # Drawing random samples
    d1 = np.random.uniform(50, 250, K)  # Demand ~ U(50,250)
    d2 = np.random.uniform(20, 250, K)  # Demand ~ U(50,250)
    d3 = np.random.uniform(200, 500, K) # Demand ~ U(50,250)

    # Setting objective function
    prod.setObjective(sum([q1 * y1[k] + q2 * y2[k] + q3 * y3[k] for k in range(K)]) / K - c1 * x1 - c2 * x2 - c3 * x3,
                      sense=GRB.MAXIMIZE)

    # Adding constraints
    prod.addConstrs(x1 >= 8 * y1[k] + 6 * y2[k] + 1 * y3[k] for k in range(K))      # Use less than procured, resource 1
    prod.addConstrs(x2 >= 4 * y1[k] + 2 * y2[k] + 1.5 * y3[k] for k in range(K))    # Use less than procured, resource 2
    prod.addConstrs(x3 >= 2 * y1[k] + 1.5 * y2[k] + 0.5 * y3[k] for k in range(K))  # Use less than procured, resource 3
    prod.addConstrs(y1[k] <= d1[k] for k in range(K))   # Produce less than demand, product 1
    prod.addConstrs(y2[k] <= d2[k] for k in range(K))   # Produce less than demand, product 2
    prod.addConstrs(y3[k] <= d3[k] for k in range(K))   # Produce less than demand, product 3

    # Optimizing
    prod.optimize(callback=None)
    print('K =', K,' Optimum: x1 =', round(x1.x,2),'x2 =', round(x2.x,2),'x3 =', round(x3.x,2),
          'Objective:', round(prod.objVal, 2))

# TaskThreeApproximation(5)
# TaskThreeApproximation(50)
# TaskThreeApproximation(500)
# TaskThreeApproximation(5000)
# TaskThreeApproximation(50000)
# TaskThreeApproximation(500000)

##### TASK 4 #####

def EV()->(_void):
    c1=2; c2=4; c3=5.2  # Cost of procurement
    q1=60; q2=40; q3=10 # Selling price
    # Creating the model
    prod = Model("Production")
    prod.Params.LogToConsole = 0
    # Assigning the variables
    x1 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x1')     # Procurement of resource 1
    x2 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x2')     # Procurement of resource 2
    x3 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x3')     # Procurement of resource 3

    y1 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='y1')     # Produced of product 1
    y2 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='y2')     # Produced of product 2
    y3 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='y3')     # Produced of product 3

    # Drawing random samples
    d1 = 150 # np.random.uniform(50,250, K)
    d2 = 150 # np.random.uniform(20,250, K)
    d3 = 350 # np.random.uniform(200,500, K)

    # Setting objective function
    prod.setObjective(q1 * y1 + q2 * y2 + q3 * y3 - c1 * x1 - c2 * x2 - c3 * x3, sense=GRB.MAXIMIZE)

    #Adding constraints
    prod.addConstr(x1 >= 8 * y1 + 6 * y2 + 1 * y3)
    prod.addConstr(x2 >= 4 * y1 + 2 * y2 + 1.5 * y3)
    prod.addConstr(x3 >= 2 * y1 + 1.5 * y2 + 0.5 * y3)
    prod.addConstr(y1 <= d1)
    prod.addConstr(y2 <= d2)
    prod.addConstr(y3 <= d3)

    #Optimizing
    prod.optimize()
    print('EV: Optimum: x1 =', round(x1.x,2),'x2 =', round(x2.x,2),'x3 =', round(x3.x,2),
          'Objective:', round(prod.objVal, 2))

# EV()

def EEV(K)->(_void):
    c1=2; c2=4; c3=5.2  # Cost of procurement
    q1=60; q2=40; q3=10 # Selling price
    # Creating the model
    prod = Model("Production")
    prod.Params.LogToConsole = 0
    # Assigning the variables
    x1 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x1')     # Procurement of resource 1
    x2 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x2')     # Procurement of resource 2
    x3 = prod.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x3')     # Procurement of resource 3

    y1 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y1')     # Produced of product 1
    y2 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y2')     # Produced of product 2
    y3 = prod.addVars([i for i in range(K)], lb=0, vtype=GRB.CONTINUOUS, name='y3')     # Produced of product 3

    # Drawing random samples
    d1 = np.random.uniform(50, 250, K)  # Demand ~ U(50,250)
    d2 = np.random.uniform(20, 250, K)  # Demand ~ U(50,250)
    d3 = np.random.uniform(200, 500, K) # Demand ~ U(50,250)

    # Setting objective function
    prod.setObjective(sum([q1 * y1[k] + q2 * y2[k] + q3 * y3[k] for k in range(K)]) / K - c1 * x1 - c2 * x2 - c3 * x3,
                      sense=GRB.MAXIMIZE)

    # Adding constraints
    prod.addConstrs(x1 >= 8 * y1[k] + 6 * y2[k] + 1 * y3[k] for k in range(K))      # Use less than procured, resource 1
    prod.addConstrs(x2 >= 4 * y1[k] + 2 * y2[k] + 1.5 * y3[k] for k in range(K))    # Use less than procured, resource 2
    prod.addConstrs(x3 >= 2 * y1[k] + 1.5 * y2[k] + 0.5 * y3[k] for k in range(K))  # Use less than procured, resource 3
    prod.addConstrs(y1[k] <= d1[k] for k in range(K))   # Produce less than demand, product 1
    prod.addConstrs(y2[k] <= d2[k] for k in range(K))   # Produce less than demand, product 2
    prod.addConstrs(y3[k] <= d3[k] for k in range(K))   # Produce less than demand, product 3
    prod.addConstr(x1 == 2100)
    prod.addConstr(x2 == 900)
    prod.addConstr(x3 == 525)

    # Optimizing
    prod.optimize()
    print('EEV: K =', K, round(prod.objVal, 2))

# EEV(5)
# EEV(50)
# EEV(500)
# EEV(5000)
# EEV(50000)
# EEV(500000)
