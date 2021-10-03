
import localSearch.localSearch as ls
import localSearch.nearestNeighbourAlgorithm as nearestNeighbourAlgorithm
import functions
import random
import time
import matplotlib.pyplot as plt

#2-opt Local Search Heuristic 
#iteratedLocalSearch: pertubation + local search
def iteratedLocalSearch(points, nodeCount, timeout):
    bestl = None
    bestSolution = None
    timeout = time.time() + timeout
    progress = []

    #greedy solution
    solution = nearestNeighbourAlgorithm.nearestNeighbourAlgorithm(points, nodeCount)

    #run local search
    ls.local_search_first_improvement(solution, points, nodeCount)
    l = functions.tourLength(solution, points, nodeCount)
    bestl = l
    bestSolution = solution.copy()
    progress.append(l)

    while True:
        #pertubation
        pertubation(solution, points, nodeCount)

        #run local search
        ls.local_search_first_improvement(solution, points, nodeCount)
        l = functions.tourLength(solution, points, nodeCount)
        progress.append(l)

        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = solution.copy()
        
        if time.time() > timeout: break

    plotProgress(progress)
    return bestSolution

#swap 2 random points
def pertubation(solution, points, nodeCount):
    start = random.randint(0, nodeCount-1)
    end = random.randint(start, nodeCount)
    solution[start+1:end+1] = reversed(solution[start+1:end+1])

def plotProgress(progress):
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show()