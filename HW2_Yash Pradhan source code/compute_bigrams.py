# @author: yash pradhan
# net-id: ypp170130
# Homework 2 - Bigram Probabilities
# Corpus: dataset/HW2_S18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt
#
# Models:
# 1. No Smoothing
# 2. Add One Smoothing
# 3. Good Turing Discounting based Smoothing

# imports
from collections import Counter

# constants
corpus_abs_path = "dataset/HW2_S18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt"

# helper methods

# reads file specified in the argument path and returns list of words as they appear in the file
def getListOfWords(path):
    # line.split() splits the sentence on white spaces like: space, tab and newline
    return [word for line in open(path, 'r') for word in line.split()]

######## No Smoothing ###############################################

def getUnigramCounts(list_of_words):
    unigramCounts = Counter({})

    for word in list_of_words:
        unigramCounts[word] += 1

    return unigramCounts

def getUnigramProbabilities(unigramCounts, corpusSize):
    unigramProbabilities = Counter({})
    
    for key in unigramCounts:
        unigramProbabilities[key] = unigramCounts[key]/corpusSize

    return unigramProbabilities

def getBigramCounts(list_of_words):
    bigramCounts = Counter({})
    i = 0
    for i in range(len(list_of_words)-1):
        bigramCounts[(list_of_words[i], list_of_words[i+1])] += 1
        
    return bigramCounts

def getBigramProbabilities(unigramCounts, bigramCounts):
    bigramProbabilities = Counter({})
    
    for word1, word2 in bigramCounts.keys():
        bigramProbabilities[(word2, word1)] = bigramCounts[(word1,word2)]/unigramCounts[word1]
        
    return bigramProbabilities


######## Add One Smoothing ###############################################

def getAddOneSmoothedBigramCount(bigramCounts, word1, word2):
    return bigramCounts[(word1, word2)] + 1

def getAddOneSmoothedReconstitutedBigramCount(unigramCounts, bigramCounts, word1, word2, vocabSize): 
    return getAddOneSmoothedBigramCount(bigramCounts, word1, word2)*unigramCounts[word1]/(unigramCounts[word1]+vocabSize)

def getAddOneSmoothedBigramProbability(unigramCounts, bigramCounts, word1, word2, vocabSize):    
    return (getAddOneSmoothedBigramCount(bigramCounts, word1, word2)/(unigramCounts[word1]+vocabSize))


######## Good Turing Discounting Smoothing ###############################################

def computeNc(bigramCounts, vocabSize):
    Nc = Counter({})
    other = 0
    
    for key in bigramCounts:
        Nc[bigramCounts[key]] += 1
        
    for key in Nc:
        other += Nc[key]
    Nc[0] = vocabSize*vocabSize - other
        
    return Nc

def computeCstar(word1, word2, N, bigramCounts):
    c = bigramCounts[(word1, word2)]
    return (c+1)*N[c+1]/N[c]

def computePstar(word1, word2, N, bigramCounts, corpus_size):
    if(bigramCounts[(word1, word2)] == 0):
        return N[1]/corpus_size
    return computeCstar(word1, word2, N, bigramCounts)/corpus_size


# driver

list_of_words = getListOfWords(corpus_abs_path)
corpus_size = len(list_of_words)
totalNonZeroBigramCounts = corpus_size - 1

print("\nTotal Words in Corpus: ", corpus_size)

unigramCounts = getUnigramCounts(list_of_words)
vocabSize = len(unigramCounts)

print("Unique Tokens:", vocabSize)

unigramProbabilities = getUnigramProbabilities(unigramCounts, corpus_size)

bigramCounts = getBigramCounts(list_of_words)
print("Total non-zero unique bigrams: ", len(bigramCounts))
print("Non zero bigram counts:", totalNonZeroBigramCounts)

# computing bigram probabilities
bigramProbabilities = getBigramProbabilities(unigramCounts, bigramCounts)

################## TEST CODE #############################
# given word1 and word2 find correspoding values based on the unigrams and bigrams of corpus

print("\nDemo code, testing\nNo Smoothing:")
word1 = "to"
word2 = "control"
print("C("+word1+","+word2+"):", bigramCounts[(word1, word2)])
print("P("+word2+"|"+word1+"):", bigramProbabilities[(word2, word1)])

print("\n\nAdd one smoothed count:", getAddOneSmoothedBigramCount(bigramCounts,word1, word2))
print("C*("+word1+","+word2+"):", getAddOneSmoothedReconstitutedBigramCount(unigramCounts, bigramCounts, word1, word2, vocabSize))
print("P*("+word2+"|"+word1+"):", getAddOneSmoothedBigramProbability(unigramCounts, bigramCounts, word1, word2, vocabSize))

Nc = computeNc(bigramCounts, vocabSize)

print("\n\nGood Turing")

print("C*("+word1+","+word2+"):", computeCstar(word1, word2, Nc, bigramCounts)) 
print("P*("+word2+"|"+word1+"):",computePstar(word1, word2, Nc, bigramCounts, totalNonZeroBigramCounts))



# printing models to file
# no smoothing

print("\n\nStart of writing models to the file")

outputfile = open("output/no-smoothing.txt", "w")
corpus_size = len(list_of_words)

i = 0
for i in range(corpus_size-1):
    word1 = list_of_words[i]
    word2 = list_of_words[i+1]    
    outputfile.write("Count("+word1+", "+word2+"):"+ str(bigramCounts[(word1, word2)]))
    outputfile.write("\tProbability("+word2+"|"+word1+"):"+ str(bigramProbabilities[(word2, word1)])+"\n")
outputfile.close()



# add one smoothing
outputfile = open("output/add-one-smoothing.txt", "w")
# vocabSize = len(unigramCounts)
# vocabSize = 10
i = 0
for i in range(corpus_size-1):
    word1 = list_of_words[i]
    word2 = list_of_words[i+1]
    outputfile.write("Count*("+word1+", "+word2+"):" + str(getAddOneSmoothedReconstitutedBigramCount(unigramCounts, bigramCounts, word1, word2, vocabSize)))
    outputfile.write("\tProbability*("+word2+"|"+word1+"):"+str(getAddOneSmoothedBigramProbability(unigramCounts, bigramCounts, word1, word2, vocabSize))+"\n")
outputfile.close()




# good turing discounting based smoothing
outputfile = open("output/good-turing-discounting-smoothing.txt", "w")

i = 0
for i in range(corpus_size-1):
    word1 = list_of_words[i]
    word2 = list_of_words[i+1]
    outputfile.write("c*("+word1+", "+word2+"):"+str(computeCstar(word1, word2, Nc, bigramCounts)))
    outputfile.write("\tp*("+word2+"|"+word1+"):"+str(computePstar(word1, word2, Nc, bigramCounts, totalNonZeroBigramCounts))+"\n")
outputfile.close()


print("End of writing models to the file")



######################################################
# Uncomment the following code for viewing calcution of the given sentence 


# compute probability of: The president wants to control the board 's control

print("\n\n\nComputing probability of given sentence:\n")

sentence = ["The", "president", "wants", "to", "control", "the", "board", "'s", "control"]

print("Sentence:")
print(sentence)

print("\n\nNo Smoothing:")
# no smoothing
i = 1
probabilityNoSmoothing = 1
for i in range(1, len(sentence)):
    word1 = sentence[i-1]
    word2 = sentence[i]
    print("P("+word2+"|"+word1+") =", bigramProbabilities[(word2, word1)])
    probabilityNoSmoothing = probabilityNoSmoothing * bigramProbabilities[(word2, word1)]
    
print("No Smoothing:", probabilityNoSmoothing)



# add one
print("\n\nAdd One:")
i = 1
probabilityAddSmoothing = 1
for i in range(1, len(sentence)):
    word1 = sentence[i-1]
    word2 = sentence[i]
    print("P("+word2+"|"+word1+") =", getAddOneSmoothedBigramProbability(unigramCounts, bigramCounts, word1, word2, vocabSize))
    probabilityAddSmoothing = probabilityAddSmoothing * getAddOneSmoothedBigramProbability(unigramCounts, bigramCounts, word1, word2, vocabSize)
    
print("Add One:", probabilityAddSmoothing)





# good turing
print("\n\nGood Turing Discounting:")
i = 1
probabilityGoodTuringSmoothing = 1
for i in range(1, len(sentence)):
    word1 = sentence[i-1]
    word2 = sentence[i]
    print("P("+word2+"|"+word1+") =", computePstar(word1, word2, Nc, bigramCounts, totalNonZeroBigramCounts))
    probabilityGoodTuringSmoothing = probabilityGoodTuringSmoothing * computePstar(word1, word2, Nc, bigramCounts, totalNonZeroBigramCounts)
print("Good Turing:", probabilityGoodTuringSmoothing)