###########################
# 6.00.2x Problem Set 1: Space Cows 

#from ps1_partition import get_partitions
import time
import operator

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.
    Parameters:
    filename - the name of the data file as a string
    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = dict()
    f = open(filename, 'r')
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:
    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows
    Does not mutate the given dictionary of cows.
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cowsCopy = sorted(cows.items(), key=operator.itemgetter(1), reverse=True)
    tempResult = []
    finalResult = []
    totalWeight = 0
    i = 0
    
    while len(cowsCopy) != 0:
        if i == len(cowsCopy):
            finalResult.append(tempResult)
            tempResult = []
            totalWeight = 0
            i = 0
        elif totalWeight + cowsCopy[i][1] <= limit:    
            tempResult.append(cowsCopy[i][0])
            totalWeight += cowsCopy[i][1]
            del cowsCopy[i]
        else:
            i += 1
    
    if tempResult != []:
        finalResult.append(tempResult)
            
    return finalResult


# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:
    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
    Does not mutate the given dictionary of cows.
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    result = []
    # for a given transport scheme
    for transport in get_partitions(cows):
        transApproved = True
        # for every load in transport scheme
        for i in range(len(transport)):
            totalWeight = 0
            # for every element of load
            for j in range(len(transport[i])):
                # sum weight
                totalWeight += cows.get(transport[i][j])
            #if the weight is above limit
            if totalWeight > limit:
                # reject the whole transport scheme
                transApproved = False
                break
        if transApproved: 
            result.append(transport)
    
    #choose the scheme with min number of loads
    min = len(cows)+1
    finalResult = []
    
    for i in range(len(result)):
        if len(result[i]) < min:
            min = len(result[i])
            finalResult = result[i]
    return finalResult

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.
    Returns:
    Does not return anything.
    """

    print('The greedy_cow_transport takes ' + str(len(greedy_cow_transport(cows,limit=10))) + ' transports')
    print('The brute_force_cow_transport takes ' + str(len(brute_force_cow_transport(cows,limit=10))) + ' transports')
    print()
    start = time.time()
    greedy_cow_transport(cows, limit=10)
    end = time.time()
    timeGreedy = end - start 
    print('The greedy_cow_transport takes ' + str(timeGreedy) + ' seconds')
    
    start = time.time()
    brute_force_cow_transport(cows, limit=10)
    end = time.time()
    timeBrute = end - start
    print('The brute_force_cow_transport takes ' + str(timeBrute) + ' seconds')


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit = 100
#print(cows)

print(greedy_cow_transport(cows))
print()
print(brute_force_cow_transport(cows))
print()
compare_cow_transport_algorithms()


#TESTING
#greedy_cow_transport({'Polaris': 20, 'Louis': 45, 'Clover': 5, 'Patches': 60, 'Lotus': 10, 'Milkshake': 75, 'Horns': 50, 'Muscles': 65, 'Miss Bella': 15, 'MooMoo': 85}, 100)
#[['MooMoo', 'Miss Bella'], ['Milkshake', 'Polaris', 'Clover'], ['Muscles', 'Lotus'], ['Patches'], ['Horns', 'Louis']]

#greedy_cow_transport({'Buttercup': 72, 'Coco': 10, 'Willow': 35, 'Daisy': 50, 'Dottie': 85, 'Rose': 50, 'Lilly': 24, 'Patches': 12, 'Abby': 38, 'Betsy': 65}, 100)
#[['Dottie', 'Patches'], ['Buttercup', 'Lilly'], ['Betsy', 'Willow'], ['Daisy', 'Rose'], ['Abby', 'Coco']]

#greedy_cow_transport({'Buttercup': 11, 'Starlight': 54, 'Willow': 59, 'Luna': 41, 'Rose': 42, 'Abby': 28, 'Betsy': 39, 'Coco': 59}, 120)
#[['Coco', 'Willow'], ['Starlight', 'Rose', 'Buttercup'], ['Luna', 'Betsy', 'Abby']]

#brute_force_cow_transport({'Lotus': 40, 'Horns': 25, 'Milkshake': 40, 'Boo': 20, 'Miss Bella': 25, 'MooMoo': 50}, 100)
#[['MooMoo', 'Horns', 'Miss Bella'], ['Lotus', 'Milkshake', 'Boo']]

#brute_force_cow_transport({'Daisy': 50, 'Buttercup': 72, 'Betsy': 65}, 75)
#[['Buttercup'], ['Daisy'], ['Betsy']]

#brute_force_cow_transport({'Starlight': 54, 'Buttercup': 11, 'Luna': 41, 'Betsy': 39}, 145)
#[['Betsy', 'Buttercup', 'Starlight', 'Luna']]

