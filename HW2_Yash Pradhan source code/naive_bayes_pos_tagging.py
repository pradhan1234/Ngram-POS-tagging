# @author: yash pradhan
# net-id: ypp170130
# Homework 2 - Naive Bayes tagging
# Corpus: dataset/HW2_S18_NLP6320_POSTaggedTrainingSet-Windows.txt

# imports
from collections import Counter

# constants
corpus_abs_path = "dataset/HW2_S18_NLP6320_POSTaggedTrainingSet-Windows.txt"

# helper functions

def read_file(path):
    list_tokens_tags = []
    # this will contain each token with its corresponding tag as a tuple: (token_i, tag_j)
    
    file = open(path, "r")
    
    for line in file.read().split("\n"):
        for word_tag in line.split():
            list_tokens_tags.append((word_tag.split("_")[0], word_tag.split("_")[1]))
    return list_tokens_tags

def getTagCounts(list_tokens_tags):
    tagCounts = Counter({})
    
    for token, tag in list_tokens_tags:
        tagCounts[tag] += 1
    return tagCounts

def getTokenTagCounts(list_tokens_tags):
    tokenTagCounts = Counter({})
    
    for token, tag in list_tokens_tags:
        tokenTagCounts[(token, tag)] += 1
        
    return tokenTagCounts

def getTagPrevTagCounts(list_tokens_tags):
    tagPrevTagCounts = Counter({})
    
    for i in range(1, len(list_tokens_tags)):
        tagPrevTagCounts[(list_tokens_tags[i-1][1], list_tokens_tags[i][1])] += 1
        
    return tagPrevTagCounts


# driver
list_tokens_tags = read_file(corpus_abs_path)

tagCounts = getTagCounts(list_tokens_tags)

tokenTagCounts = getTokenTagCounts(list_tokens_tags)

tagPrevTagCounts = getTagPrevTagCounts(list_tokens_tags)

outputfile = open("output/bayes-model.txt", "w")

# outputfile.write("TOKEN TAG PROBABILITY\N\N")


i = 0
for key in tokenTagCounts.keys():
    token = key[0]
    tag = key[1]
    outputfile.write("P("+token+"|" + tag +") = "+ str(tokenTagCounts[(token, tag)]/tagCounts[tag]) +"\n")
    
outputfile.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

i = 1
for key in tagPrevTagCounts.keys():
    tag = key[0]
    prevtag = key[1]
    outputfile.write("P("+tag+"|" + prevtag +") = "+str(tagPrevTagCounts[key]/tagCounts[tag])+"\n")
    
    
