#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions
import localSearch.localSearch as ls
import localSearch.multiStartMH as multiStartMH
import localSearch.graspMH as graspMH
import localSearch.iteratedLocalSearch as iteratedLocalSearch
import antColony.antColony as antColony
import geneticalgo.tsp_ga as geneticalgo
import visualization

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(functions.Point(float(parts[0]), float(parts[1])))


    option = input ("(1) Local Search\n(2) MultiStart MH\n(3) Grasp MH\n(4) ILS MH\n(5) Ant Colony\n(6) Genetic Algo\n>>")
    
    solution = []
    if(option =="1"):
        solution = ls.local_search(points, nodeCount)
    elif(option =="2"):
        timeout = int(input("Timeout in seconds:"))
        solution = multiStartMH.multiStartMH(points, nodeCount, timeout)
    elif(option =="3"):
        timeout = int(input("Timeout in seconds:"))
        solution = graspMH.graspMH(points, nodeCount, timeout)
    elif(option == "4"):
        timeout = int(input("Timeout in seconds:"))
        solution = iteratedLocalSearch.iteratedLocalSearch(points, nodeCount, timeout)
    elif(option == "5"):
        iterations = int(input("Number of iterations:"))
        solution = antColony.antColony(points, iterations)
    elif(option == "6"):
        solution = geneticalgo.geneticAlgorithm(points=points, popSize=100, eliteSize=20, mutationRate=0.005, generations=500)
    
    if(visualization.__PLOT): visualization.plot(solution, points, nodeCount)

    # calculate the length of the tour
    obj = functions.tourLength(solution, points, nodeCount)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')