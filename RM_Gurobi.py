import os
import time
import random
import pickle
import numpy as np
from gurobipy import *

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

    model = Model("Gurobi")

    site_to_new = {}
    new_to_site = {}
    new_num = 0
    for i in range(n):
        if(city_partition[i] == 1):
            site_to_new[i] = new_num
            new_to_site[new_num] = i
            new_num += 1

    x = model.addMVar((new_num), lb = 0, ub = 1, vtype = GRB.BINARY) 
    
    coeff = 0
    for i in range(n):
        if(city_partition[i] == 1):
            coeff += x[site_to_new[i]] * coefficient[i]
        else:
            coeff += now_sol[i] * coefficient[i]
    if(obj_type == 'maximize'):
        model.setObjective(coeff, GRB.MAXIMIZE)
    else:
        model.setObjective(coeff, GRB.MINIMIZE)

    for i in range(m):
        constr = 0
        flag = 0
        for j in range(k[i]):
            if(city_partition[site[i][j]] == 1):
                constr += x[site_to_new[site[i][j]]] * value[i][j]
                flag = 1
            else:
                constr += now_sol[site[i][j]] * value[i][j]

        if(flag == 1):
            if(constraint_type[i] == 1):
                model.addConstr(constr <= constraint[i])
            else:
                model.addConstr(constr >= constraint[i])
        else:
            if(constraint_type[i] == 1):
                if(constr > constraint[i]):
                    print("QwQ")
                    print(constr,  constraint[i])
                    print(city_partition)
            else:
                if(constr < constraint[i]):
                    print("QwQ")
                    print(constr,  constraint[i])
                    print(city_partition)

    model.setParam('TimeLimit', max(time_limit - (time.time() - begin_time), 0))

    model.optimize()
    try:
        sol = (list)((x.X).astype(int))
        new_sol = []
        for i in range(n):
            if(city_partition[i] == 0):
                new_sol.append(now_sol[i])
            else:
                new_sol.append(sol[site_to_new[i]])
        return new_sol, model.ObjVal
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


begin_time = time.time()


now_num = 4
set_time = 3000
layer = 2
city_num = 2 ** layer


if(os.path.exists('/home/username/RM/example-SC-h/data' + str(now_num) + '.pickle') == False):
    print("No problem file!")

with open('/home/uername/RM/example-SC-h/data' + str(now_num) + '.pickle', "rb") as f:
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


ValList = [nowVal]
TimeList = [time.time() - begin_time]



while(time.time() -  begin_time < set_time):
   
    bestVal = nowVal
    bestSol = nowX

   
    city_partition = partition(n, m, k, site, value, constraint, constraint_type, nowX, city_num)
    
    now_city_num = city_num
    now_Sols = []
    for i in range(now_city_num):
        nowSol, nowVal = search(obj_type, n, m, k, site, value, constraint, constraint_type, coefficient, nowX, city_partition[i], 0.1 * set_time)
        if(nowVal == -1):
            continue
        now_Sols.append(nowSol)
        print("Search")
       
        ValList.append(nowVal)
        TimeList.append(time.time() - begin_time)
        if(obj_type == 'maximize' and nowVal > bestVal):
            bestVal = nowVal
            bestSol = nowSol
        if(obj_type == 'minimize' and nowVal < bestVal):
            bestVal = nowVal
            bestSol = nowSol
    

    while(len(nowSol) == now_city_num and now_city_num > 1):
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


            
        
