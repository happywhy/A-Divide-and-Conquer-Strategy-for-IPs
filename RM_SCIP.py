import os
import time
import random
import pickle
import numpy as np
from pyscipopt import Model as SModel

class pair: 
    def __init__(self): 
        self.site = 0
        self.money = 0

def cmp(a, b): 
    if a[1] < b[1]: 
        return -1 
    else:
        return 1 

def partition(n, m, k, site, value, constraint, constraint_type, nowX, city_num):
    village = []
    for i in range(m):
        village.append(i)
    
    
    random.shuffle(village)

    
    city_partition = []
    now_city = np.zeros(n)
    now_num = 0
    visit = {}
    for i in range(m):
        if(now_num >= n / city_num):
            city_partition.append(now_city)
            now_city = np.zeros(n)
            now_num = 0
        for j in range(k[village[i]]):
            if(site[village[i]][j] not in visit):
                visit[site[village[i]][j]] = 1
                now_city[site[village[i]][j]] = 1
                now_num += 1
    city_partition.append(now_city)

    #print(len(city_partition))
    return(city_partition)

def search(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, now_sol, city_partition, time_limit):

    begin_time = time.time()
    
    #Define model
    #print("====", obj_type, "====")
    model = SModel("SCIP")
    # Decision variable definition
    x = []
    for i in range(n):
        x.append(0)
        x[i] = model.addVar(vtype="B", name="x(%s)"%i)  
    # objective
    coeff = 0
    for i in range(n):
        if(city_partition[i] == 1):
            coeff += x[i] * coefficient[i]
        else:
            coeff += now_sol[i] * coefficient[i]
    model.setObjective(coeff, sense = obj_type)
    #add constraits
    for i in range(m):
        constr = 0
        flag = 0
        for j in range(k[i]):
            if(city_partition[site[i][j]] == 1):
                constr += x[site[i][j]] * value[i][j]
                flag = 1
            else:
                constr += now_sol[site[i][j]] * value[i][j]

        if(flag == 1):
            if(constraint_type[i] == 1):
                model.addCons(constr <= constraint[i])
            else:
                model.addCons(constr >= constraint[i])
    # maximum time for solving
    model.setRealParam('limits/time', max(time_limit - (time.time() - begin_time), 0))
    
    model.optimize()

    try:
        if(model.getDualbound() <= 0):
            return -1, -1
        new_sol = []
        for i in range(n):
            new_sol.append(model.getVal(x[i]))
        for i in range(n):
            if(city_partition[i] == 0):
                new_sol[i] = now_sol[i]
        return new_sol, model.getObjVal()
    except:
        return -1, -1

def cross(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, solA, blockA, solB, blockB, set_time):
    crossX = np.zeros(n)
    
    for i in range(n):
        if(blockA[i] == 1):
            crossX[i] = solA[i]
        else:
            crossX[i] = solB[i]
    
    color = np.zeros(n)
    add_num = 0
    for j in range(m):
        constr = 0
        flag = 0
        for l in range(k[j]):
            if(color[site[j][l]] == 1):
                flag = 1
            else:
                constr += crossX[site[j][l]] * value[j][l]

        if(flag == 0):
            if(constraint_type[j] == 1):
                if(constr > constraint[j]):
                    for l in range(k[j]):
                        if(color[site[j][l]] == 0):
                            color[site[j][l]] = 1
                            add_num += 1
            else:
                if(constr < constraint[j]):
                    for l in range(k[j]):
                        if(color[site[j][l]] == 0):
                            color[site[j][l]] = 1
                            add_num += 1
    
    newcrossX, newVal = search(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, crossX, color, set_time)
    return newcrossX, newVal

def merge(n, blockA, blockB):
    new_block = np.zeros(n)
    for i in range(n):
        if(blockA[i] or blockB[i]):
            new_block[i] = 1
    return(new_block)

#begin time
begin_time = time.time()

#parameter definition
now_num = 4
set_time = 3000
layer = 2
city_num = 2 ** layer

# problem reading
if(os.path.exists('/home/sharing/disk1/username/GAT3/example-IS-m/data' + str(now_num) + '.pickle') == False):
    print("No problem file!")

with open('/home/sharing/disk1/username/GAT3/example-IS-m/data' + str(now_num) + '.pickle', "rb") as f:
    problem = pickle.load(f)

obj_type = problem[0]
print(obj_type)
n = problem[1]
m = problem[2]
k = problem[3]
site = problem[4]
value = problem[5]
constraint = problem[6]
constraint_type = problem[7]
coefficient = problem[8]


nowX = np.zeros(n)
for i in range(n):
    nowX[i] = 0
nowVal = 0
for i in range(n):
    nowVal += nowX[i] * coefficient[i]

# current solution
ValList = [nowVal]
TimeList = [time.time() - begin_time]



while(time.time() -  begin_time < set_time):
    # best solution for this iteration
    bestVal = nowVal
    bestSol = nowX

    
    city_partition = partition(n, m, k, site, value, constraint, constraint_type, nowX, city_num)
    # local optimum
    now_city_num = city_num
    now_Sols = []
    for i in range(now_city_num):
        nowSol, nowVal = search(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, nowX, city_partition[i], 0.1 * set_time)
        if(nowVal == -1):
            continue
        now_Sols.append(nowSol)
        print("Search")
        #update
        ValList.append(nowVal)
        TimeList.append(time.time() - begin_time)
        if(obj_type == 'maximize' and nowVal > bestVal):
            bestVal = nowVal
            bestSol = nowSol
        if(obj_type == 'minimize' and nowVal < bestVal):
            bestVal = nowVal
            bestSol = nowSol
    
    # global optimum
    while(len(now_Sols) == now_city_num and now_city_num > 1):
        now_city_num //= 2
        new_Sols = []
        new_Citys = []
        for i in range(now_city_num):
            nowSol, nowVal = cross(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, now_Sols[i * 2], city_partition[i * 2], now_Sols[i * 2 + 1], city_partition[i * 2 + 1], 0.1 * set_time)
            if(nowVal == -1):
                continue
            new_Sols.append(nowSol)
            new_Citys.append(merge(n, city_partition[i * 2], city_partition[i * 2 + 1]))
            
            ValList.append(nowVal)
            TimeList.append(time.time() - begin_time)
            if(obj_type == 'maximize' and nowVal > bestVal):
                bestVal = nowVal
                bestSol = nowSol
            if(obj_type == 'minimize' and nowVal < bestVal):
                bestVal = nowVal
                bestSol = nowSol
        now_Sols = new_Sols
        city_partition = new_Citys
    nowVal = bestVal
    nowX = bestSol

print(TimeList)
print(ValList)        
