
from collections import namedtuple
Point = namedtuple("Point", ['x', 'y'])
import math
import random
import matplotlib.pyplot as plt


__ALFA = 1
__BETA = 1
__EVAPORATIONRATE = 0.01
__INITIALPHEROMONE = 0.1
__UPDATEPHEROMONECONSTANT = 10

class AntSolution:
    def __init__(self, ant, nodeCount):
        self.ant = ant
        self.routeList = []
        self.routeMatrix = [[0 for i in range(nodeCount)] for j in range(nodeCount)]
        self.distance=0
        self.complete = False
        self.remaningList = set(range(nodeCount))
        self.nodeCount = nodeCount
    
    def appendNode(self, node, points):
        if(len(self.routeList)>0):
            lastNode = self.routeList[-1]
            self.routeMatrix[lastNode][node] = 1
            self.distance += length(points[lastNode], points[node])
        self.routeList.append(node)
        self.complete = (len(self.routeList) >= self.nodeCount)
        self.remaningList.discard(node)
        

def antColony(points, n_iterations):   
    node_count = len(points)
    pheromone_matrix = [[__INITIALPHEROMONE**__BETA for i in range(node_count)] for j in range(node_count)]
    distance_matrix = createDistanceMatrix(points, node_count)
    probability_matrix = [[0 for i in range(node_count)] for j in range(node_count)]
    updateProbabilityMatrix(probability_matrix, node_count, distance_matrix, pheromone_matrix)
    progress = []   
    
    betterSolution = None
    for i in range(n_iterations):
        solutions = []
        for ant in range(node_count):            
            antSolution = AntSolution(ant, node_count)
            antSolution.appendNode(ant, points)
            solutions.append(antSolution)
            lastNode = ant
            
            while (antSolution.complete == False):
                nextNode = rouletteWheel(probability_matrix[lastNode], antSolution.remaningList)
                antSolution.appendNode(nextNode, points)
                lastNode = nextNode
                
        updatePheromoneMatrix(pheromone_matrix, solutions, node_count)
        updateProbabilityMatrix(probability_matrix, node_count, distance_matrix, pheromone_matrix)
        solution = getBetterSolution(solutions)
        if(betterSolution == None or  solution.distance < betterSolution.distance):
            betterSolution = solution
        progress.append(solution.distance) 
       
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show()
    
    return getBetterSolution(solutions).routeList

def getBetterSolution(solutions):
    betterS = solutions[0]
    for s in solutions:
        if (s.distance < betterS.distance): betterS = s
    return betterS

def createDistanceMatrix(points, node_count):
    distance_matrix = [[0 for i in range(node_count)] for j in range(node_count)]
    for p1 in range(node_count):
        for p2 in range(node_count):
            if(p1!=p2): distance_matrix[p1][p2] = (1/length(points[p1],points[p2]))**__ALFA
    return distance_matrix                         
                                                   
def updateProbabilityMatrix(probability_matrix, node_count, distance_matrix, pheromone_matrix):
    for p1 in range(node_count):
        for p2 in range(node_count):
            if(p1!=p2): probability_matrix[p1][p2] = ((distance_matrix[p1][p2]) * (pheromone_matrix[p1][p2])) / sum(x * y for x, y in zip(distance_matrix[p1], pheromone_matrix[p1]))
    return probability_matrix

def updatePheromoneMatrix(pheromone_matrix, solutions, node_count):
    for p1 in range(node_count):
        for p2 in range(node_count):
            pheromone_matrix[p1][p2] = getNewPheromoneValue(solutions, pheromone_matrix[p1][p2], node_count, p1, p2)
            
    return pheromone_matrix
    
def getNewPheromoneValue(solutions, initial_value, node_count, p1, p2):
    value = (1-__EVAPORATIONRATE)*initial_value
    for ant in range(node_count):
        if(solutions[ant].routeMatrix[p1][p2] == 1 or solutions[ant].routeMatrix[p2][p1]== 1): value += (__UPDATEPHEROMONECONSTANT) / (solutions[ant].distance)
    return value    

def rouletteWheel(probability_array, remaningNodes):
    total = 0
    for i in remaningNodes: total += probability_array[i]
    
    probability_array_new = [0]*len(probability_array)
    for i in remaningNodes: probability_array_new[i] = probability_array[i] / total

    randNum = random.random()
    r = 0
    choice = 0
    for i in probability_array_new:
        r += i
        if randNum < r: return choice
        choice += 1

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)