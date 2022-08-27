import numpy as np
NUM_ARRAYS = 10000
np.random.seed(10023432)
myString = input("Enter a word (all lowercase letters) > ")
counter = 1
candidates = {}
genes = np.random.randint( ord('a'), ord('z')+1, size=(NUM_ARRAYS, len(myString)), dtype=np.uint8)

#convert input into array
actual = np.zeros(len(myString), dtype=np.uint8)
for i in range(len(myString)):
    actual[i] = ord(myString[i])

#find fitness
def fitness(candidate, theactual):
    diffAlready1 = (np.bitwise_and(candidate, theactual))
    diffGet0s = (np.bitwise_and(np.invert(candidate), np.invert(theactual)))
    unpacked1s = np.unpackbits(diffAlready1)
    unpacked0s = np.unpackbits(diffGet0s)
    return unpacked1s.sum() + unpacked0s.sum()

#convert array into string
def getChrs(array):
    x = ""
    for i in array:
        x += chr(i)
    return x

#wipe out everything below average
#state the best gene, if we've seen this guy too much, add a bunch of mutationns
def runGeneration(geneArray, theactual):
    theFitnesses = []
    for i in geneArray:
        indexFitness = fitness(i, actual)
        theFitnesses.append(indexFitness)
    theFitnessesArray = np.array(theFitnesses)
    bests = (  theFitnessesArray[theFitnessesArray == np.amax(theFitnessesArray)]  )
    bestLocation = theFitnessesArray == bests[0]
    best = getChrs(geneArray[bestLocation][0])
    
    if best not in candidates:
        candidates[best] = 1
    else:
        candidates[best] +=1
    if candidates[best] > 1:
        for _ in range(NUM_ARRAYS // 2):
            mutation(geneArray)
    
    print("Iteration number {}. The best match is {} with a fitness of {}\n".format(counter, best, bests[0]))
    average = theFitnessesArray.mean()
    keepers = theFitnessesArray > average
    return geneArray[keepers]

#check to see if we've done it
#if so, return the answer
def checkMatch(geneArray, theactual):
    didItWork = False
    theMatch = ""
    for i in geneArray:
        if list(i) == list(theactual) and didItWork == False:
            theMatch = getChrs(i)
            didItWork = True
    return [didItWork, theMatch]

#input two genes, output two hybrid genes
def breedTwo(a,b):
    cutAt = np.random.randint(0,len(myString))
    tempa = a.copy()
    tempb = b.copy()
    a[cutAt:] = tempb[cutAt:]
    b[cutAt:] = tempa[cutAt:]
    return np.array([a,b])

#generate NUM_ARRYS new genes using breedTwo
def crossGen(geneArray):
    children = []
    for i in range(NUM_ARRAYS//2):
        first = np.random.randint(0,len(geneArray))
        second = np.random.randint(0,len(geneArray))
        newBorns = breedTwo(geneArray[first],geneArray[second])
        children.append(newBorns[0])
        children.append(newBorns[1])
    return np.array(children)

#convert one gene to something random
def mutation(geneArray):
    mutant = np.random.randint(0, len(geneArray)-1)
    geneArray[mutant] = np.random.randint( ord('a'), ord('z')+1, len(myString))

found = False
while not found:
    survivors = runGeneration(genes,actual)
    offspring = crossGen(survivors)    
    for _ in range(10):
        mutation(offspring)
    results = checkMatch(offspring, actual)
    if results[0] == True:
        found = True
        print("After cross breeding/mutating iteration {}, your word, {}, was found".format(counter, results[1]))
    else:
        genes = offspring
        counter += 1