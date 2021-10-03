import functions
import localSearch.nearestNeighbourAlgorithm as nearestNeighbourAlgorithm

def local_search(points, nodeCount):
    solution = nearestNeighbourAlgorithm.nearestNeighbourAlgorithm(points, nodeCount)
    local_search_first_improvement(solution, points, nodeCount)
    return solution

def local_search_first_improvement(solution, points, nodeCount):
    improvement = True
    while (improvement):
        improvement = False
        for i in range(nodeCount-1):
            for j in range(nodeCount-1):
                if is_improvement(i, j, points, solution):
                    swap(solution, i, j)
                    improvement = True

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