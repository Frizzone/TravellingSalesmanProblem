
import localSearch.localSearch as ls
import localSearch.nearestNeighbourAlgorithm as nearestNeighbourAlgorithm
import functions
import random
import time
import math
import matplotlib.pyplot as plt

#2-opt Local Search Heuristic using GRAPS Metaheurisct
def graspMH(points, nodeCount, timeout):
    bestl = None
    bestSolution = None
    timeout = time.time() + timeout
    progress = []
    while True:
        #alfa 0%-20%
        alfa = random.random()/5
        solution = buildSolution(points, nodeCount, alfa)        
        ls.local_search_first_improvement(solution, points, nodeCount)
        l = functions.tourLength(solution, points, nodeCount)
        progress.append(l)
        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = solution.copy()
        if time.time() > timeout: break
    plotProgress(progress)
    return bestSolution

def buildSolution(points, nodeCount, alfa):
    nextNode = firstNode(points, nodeCount)
    solution = []
    solution.append(nextNode)
    
    selected = [0] * nodeCount
    size = math.ceil(alfa*nodeCount)
    while(len(solution) <= nodeCount):
        bestCandidatesList = selectBestCandidates(nextNode, points, size, selected)
        nextNode = random.choice(bestCandidatesList)
        solution.append(nextNode)
        selected[nextNode] = 1
    
    return solution


def selectBestCandidates(nextNode, points, size, selected):
    bestCandidatesOrdered = []
    for i in range(len(points)):
        l = functions.length(points[nextNode], points[i])
        if(i!= nextNode and selected[i]==0): bestCandidatesOrdered.append((i, l))
    
    bestCandidatesOrdered.sort(key=lambda x:x[1], reverse=False)
    
    s = 0
    bestCandidatesList = []
    for i in bestCandidatesOrdered:
        bestCandidatesList.append(i[0])
        s+=1
        if(s>=size): return bestCandidatesList
    return bestCandidatesList

def firstNode(points, nodeCount):
    init = random.randint(0, nodeCount-1)
    return init

def plotProgress(progress):
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show()