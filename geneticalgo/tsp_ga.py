import random, operator, matplotlib.pyplot as plt
import math
import functions

class Individual:
    def __init__(self, route, points):
        self.route = route
        self.points = points
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            self.distance = functions.length(self.points[self.route[-1]], self.points[self.route[0]])
            for index in range(0, len(self.points)-1):
                self.distance += functions.length(self.points[self.route[index]], self.points[self.route[index+1]])
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

def geneticAlgorithm(points, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, points)
    progress = []
    result = rankRoutes(pop, points)
    len = 1 / result[0][1]
    progress.append(len)
    bestRoute = {"list":pop[result[0][0]].copy(), "len": len}
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, points)
        result = rankRoutes(pop, points)
        len = 1 / result[0][1]
        progress.append(len)
        if(len < bestRoute["len"]):
            bestRoute = {"list":pop[result[0][0]].copy(), "len": len}
            print(len)
    print(bestRoute)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
    
    return bestRoute["list"]

def nextGeneration(currentGen, eliteSize, mutationRate, points):
    popRanked = rankRoutes(currentGen, points)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize, points)
    nextGeneration = mutatePopulation(children, mutationRate, points)
    return nextGeneration

#create Greedy Randomized route
def createRoute(points):
    nodeCount = len(points)
    
    #nextNode = random.randint(0, nodeCount-1)
    nextNode = 0
    solution = []
    solution.append(nextNode)
    selected = [0] * nodeCount
    selected[0] = 1
    alfa = random.random()
    size = math.ceil(alfa*nodeCount)
    while(len(solution) < nodeCount):
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

#Initial population
def initialPopulation(popSize, pointList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(pointList))
    return population

#Rank population
def rankRoutes(population, points):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Individual(population[i], points).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Selection
#Elitism: select best routes
def selection(popRanked, eliteSize):
    selectionResults = []
    for i in range(0, len(popRanked)):
        selectionResults.append(popRanked[i][0])
    return selectionResults

#create a ordered array of individuals (population)
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# breed Population and create a children population modified
def breedPopulation(matingpool, eliteSize, points):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    # the elite bests (elite) individuals (routes) in matingpool don't suffer crossover modification
    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    # the remaining worst: breed with random individuals (routes) in matingpool and create modified children
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1], points)
        children.append(child)
    return children

# Crossover
def breed(parent1, parent2, points):
    node_count = len(parent1)
    child = []
    selected = [0]*node_count
    child.append(parent1[0])
    selected[0]=1
    for n in range(0, node_count-1):
        candidates = [parent1[n], parent2[n], parent1[n+1], parent2[n+1]]
        best = None
        bestLen = None
        for c in range(len(candidates)):
            if(selected[candidates[c]] != 1):
                if(bestLen == None or bestLen > functions.length(points[child[n]], points[candidates[c]])):
                    best = candidates[c]
                    bestLen = functions.length(points[child[n]], points[candidates[c]])
        if(best != None): 
            child.append(best)
            selected[best]=1
        else: 
            nearest = nearestNode(n, selected, points)
            child.append(nearest)
            selected[nearest]=1
    return child

def nearestNode(node, selected, points):
    nearestNode = 0
    minlength = 0
    for j in range(len(points)):
        if(selected[j] == 0):
            l = functions.length(points[node], points[j])
            if(minlength == 0 or minlength > l): 
                minlength = l
                nearestNode = j
    if nearestNode!=0: return nearestNode
    else: return None

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutatePopulation(population, mutationRate, points):
    mutatedPop = []
    
    #keep the best
    mutatedPop.append(population[0])
    
    #mutate the remaining
    for ind in range(1, len(population)):
        mutatedInd = mutate(population[ind], mutationRate, points)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#mutate -> local search best improvement swaps
def mutate(individual, mutationRate, points):
    nodeCount = len(points)
    for i in range(nodeCount-1):
        if random.random() < mutationRate :
            for j in range(nodeCount-1):
                if is_improvement(i, j, points, individual):
                    swap(individual, i, j)
    return individual

def is_improvement(i, j, points, route):
    if i < j:
        actual = functions.length(points[route[i-1]], points[route[i]]) +  functions.length(points[route[j]], points[route[j+1]])
        new = functions.length(points[route[i-1]], points[route[j]]) +  functions.length(points[route[i]], points[route[j+1]])
        return new < actual
    elif i > j:
        actual = functions.length(points[route[j-1]], points[route[j]]) +  functions.length(points[route[i]], points[route[i+1]])
        new = functions.length(points[route[j-1]], points[route[i]]) +  functions.length(points[route[j]], points[route[i+1]])
        return new < actual

# swap (B,E)
# A->B->C->D->E->F
# A->E->D->C->B->F (A-> reverve(B->C->D->E) ->F)
def swap(route, i, j):
    if i < j : route[i:j+1] = reversed(route[i:j+1])
    elif j > i: route[j:i+1] = reversed(route[j:i+1])
