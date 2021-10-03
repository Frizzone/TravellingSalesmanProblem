
import localSearch.localSearch as ls
import localSearch.nearestNeighbourAlgorithm as nearestNeighbourAlgorithm
import functions
import random
import time
import matplotlib.pyplot as plt

#Local Search Heuristic using Multi Start Metaheurisct: starting from different starting configuration (random)
def multiStartMH(points, nodeCount, timeout):
    bestl = None
    bestSolution = None
    timeout = time.time() + timeout
    progress = []
    while True:
        solution = generateRandomSolution(nodeCount)
        ls.local_search_first_improvement(solution, points, nodeCount)
        l = functions.tourLength(solution, points, nodeCount)
        progress.append(l)
        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = solution.copy()

        if time.time() > timeout: break

    plotProgress(progress)
    return bestSolution

def generateRandomSolution(nodeCount):
    solution = []
    finish = False
    selected = [0]*nodeCount
    nodes = list(range(0, nodeCount))
    while(not finish):
        minlength = 0
        j = 0
        if(len(solution) < nodeCount):
            nextNode = random.choice(nodes)
            solution.append(nextNode)
            selected[nextNode] = 1
            nodes.remove(nextNode)            
        else: finish = True
    return solution


def plotProgress(progress):
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show()