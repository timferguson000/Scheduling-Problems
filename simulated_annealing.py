# Implements the simulated annealing algorithm to solve the job shop problem for the benchmark 6 x 6 example by Fisher and Thompson (ft06)
# The optimal makespan (time until the final job is completed) for this problem is 55
# ith row represents the ith machinee
# jth colunm represents the jth job
# ijth entry represents the time it takes the ith machine to process the jth job

job_order = [
             [2, 0, 1, 3, 5, 4],
             [1, 2, 4, 5, 0, 3],
             [2, 3, 5, 0, 1, 4], 
             [1, 0, 2, 3, 4, 5],
             [2, 1, 4, 5, 0, 3],
             [1, 3, 5, 0, 4, 2]
            ]

process_cost = [
                [1, 3, 6, 7, 3, 6],
                [8, 5, 10, 10, 10, 4],
                [5, 4, 8, 9, 1, 7],
                [5, 5, 5, 3, 8, 9],
                [9, 3, 5, 4, 3, 1],
                [3, 3, 9, 10, 4, 1]
               ]

# solution is an array of length 36 with entries 0 , 1, 2, 3, 4, 5 each appearing six times
# This records when a job will be processed by the next machine that it needs to be processed by
# Ex. solution = [0, 1, 0, ...]
# This means that job 0 will be processed on machine 2 (job_order entry 0, 0)
# When job 1 is not being processed elsewhere and machine 1 is not processing another job, machine 1 will start to process job 1 (job_order entry 1, 0)
# When job 0 is not being processed elsewhere and machine 0 is not processing another job, machine 0 will start to process job 0 (job_order entry 0, 1)
# ...
# Every possible solution is a permutation of the array
# solution = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, ..., 5, 5, 5, 5, 5, 5]
# which represents job 0 being processed on all machines, then job 1 being processed on all machines, ..., and finally job 5 being processed on all machines



# Imports libraries

import numpy as np
import random



# Defines the makespan function
# Input: the finish times of each job
# Output: the makespan (max of the finish times) of the solution

def makespan(times):
    return max(times)



# Defines function finish_times
# Input: a solution (array of length 36 describing the order in which each job is processed on each machine)
# Output: the finish times of each job

def finish_times(solution):
    time = 0
    available = [0,0,0,0,0,0]
    indices = [0,0,0,0,0,0]

    for job in solution:
        index = indices[job]
        machine = job_order[job][index]
        if time < available[machine]:
            time = available[machine]
        available[machine] = time + process_cost[job][index]
        indices[job] += 1

    return available
    
    
    
# Defines the funciton random_neighbor
def random_neighbor(solution):
    i = 0
    j = 0
    while i == j:
        swap = random.sample(solution.tolist(), 2)
        i = swap[0]
        j = swap[1]
    solution[i], solution[j] = solution[j], solution[i] # Swaps values in ith and jth positions
    return solution


# Main Program
n_tests = 50 # Number of times a random initial solution is probabilistically evolved to a good local solution
n_iterations = 500 # Number of iterations for probabilistically evolving random initial solution to a good local solution
beta = 0.9 # Cooling parameter. Determines how quickly the probability of a random move decrease as the iteration number increases.
           # This allows the algorithm to explore more in the beginning iterations and exploit more in later iterations.

best_score = 100 # High value that will be updated with first decent iteration

for test in range(n_tests):
    solution = np.random.permutation([i%6 for i in range(36)])
    score = makespan(finish_times(solution))
    for iteration in range(n_iterations):
        neighbor_solution = random_neighbor(solution)
        neighbor_score = makespan(finish_times(neighbor_solution))
        if neighbor_score < score: # Update solution if the neighbor solution is better
            solution = neighbor_solution
            score = neighbor_score
        else: # If the neighbor solution isn't better, only update with given probability. Probability decreases with gap between scores and with later iterations
            threshold = np.exp((score - neighbor_score)*pow(beta, -iteration))
            x = random.uniform(0.0,1.0)
            if x < threshold:
                solution = neighbor_solution
                score = neighbor_score
    if score < best_score:
        best_solution = solution
        best_score = score

# Displays the final values
# Optimal solution has makespan of 55
print(best_solution)
print(best_score)

# I obtained this output which represents an optimal solution
# [0 5 3 5 0 4 3 5 1 3 1 1 5 2 3 1 2 3 1 4 2 4 2 2 1 0 2 4 0 0 5 3 4 0 5 4]
# 55
