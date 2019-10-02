# @author: yash pradhan
# net-id: ypp170130
# Homework 2 - Brill's tagging
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

# function to find out by which all tags has a token been tagged with
# eg:- race: [VB, NN, VB, VB]
def findAllWordsTagging(list_tokens_tags):
    allWordsTagsMap = {}
    
    for token, tag in list_tokens_tags:
        if token not in allWordsTagsMap.keys():
            allWordsTagsMap[token] = [tag]
        else:
            allWordsTagsMap[token].append(tag)
            
    return allWordsTagsMap

# finds all unique tags in the corpus
def getUniqueTags(list_tokens_tags):
    setTags = set()
    
    for token, tag in list_token_tags:
        if tag not in setTags:
            setTags.add(tag)
    
    return setTags

def getMostLikelyTags(allWordsTagsMap):
    list_most_likely_tag = {}
    
    for key in allWordsTagsMap:
#         print(Counter(allWordsTagsMap[key]).most_common(1)[0][0])
        list_most_likely_tag[key] = Counter(allWordsTagsMap[key]).most_common(1)[0][0]
    return list_most_likely_tag

def applyMostLikelyTags(list_tokens_tags, list_most_likely_tag):
    list_most_probable_tokens_tags = []
    for token, tag in list_tokens_tags:
        list_most_probable_tokens_tags.append((token, list_most_likely_tag[token]))
    return list_most_probable_tokens_tags

def brillTransformationBasedLabelling(correct_tokens_tags, most_probable_tokens_tags, tags):
    transformationQueue = []
    corpus_size = len(correct_tokens_tags)
    current_tokens_tags = most_probable_tokens_tags[:] 
    #deep copy of most probable tags, will be modified over iterations
    
    iteration = 0
    
    for iteration in range(0, 10):
#         print("rule ", iteration)
        globalMax_score = -1000000000
        
        for from_tag in tags:
            for to_tag in tags: 
                num_good_transforms = Counter({})
                num_bad_transforms = Counter({})
                if(from_tag == to_tag):
                    continue
                
                for pos in range(1, corpus_size):
                    if(correct_tokens_tags[pos][1] == to_tag and current_tokens_tags[pos][1] == from_tag):
#                         print("good")
                        num_good_transforms[current_tokens_tags[pos-1][1]]+=1
                    elif(correct_tokens_tags[pos][1] == from_tag and current_tokens_tags[pos][1] == from_tag):
#                         print("bad")
                        num_bad_transforms[current_tokens_tags[pos-1][1]]+=1
                best_score = -1000000000
                best_z = None
                # argmax
                for key_tag in num_good_transforms.keys():
                    if(best_score < num_good_transforms[key_tag] - num_bad_transforms[key_tag] and not(num_good_transforms[key_tag]==0 and num_bad_transforms[key_tag]==0)):
                        best_score = num_good_transforms[key_tag] - num_bad_transforms[key_tag]
                        best_z = key_tag
                
                if(num_good_transforms[best_z] - num_bad_transforms[best_z] > globalMax_score and not(num_good_transforms[best_z]==0 and num_bad_transforms[best_z]==0)):
                    best_rule = (best_z, from_tag, to_tag)
                    globalMax_score = num_good_transforms[best_z] - num_bad_transforms[best_z]
        
        transformationQueue.append((best_rule, globalMax_score))
        for pos in range(1, corpus_size):
            if(current_tokens_tags[pos][1] == best_rule[1] and current_tokens_tags[pos-1][1] == best_rule[0]):
                current_tokens_tags[pos] = (current_tokens_tags[pos][0], best_rule[2])
        
    return transformationQueue
    







# driver
list_tokens_tags = read_file(corpus_abs_path)

allWordsTagsMap = findAllWordsTagging(list_tokens_tags)

list_most_likely_tag = getMostLikelyTags(allWordsTagsMap)

list_most_probable_tokens_tags = applyMostLikelyTags(list_tokens_tags, list_most_likely_tag)

rules = brillTransformationBasedLabelling(list_token_tags, list_most_probable_tokens_tags, ["VB", "NN"])

outputfile = open("output/brill-rules.txt", "w")

outputfile.write("Prev Tag \t\t From Tag \t\t To Tag \t\t Score\n")

i = 0

for i in range(0, 7):
    rule = rules[i]
    outputfile.write(str(rule[0][0])+ "\t\t"+ str(rule[0][1])+ "\t\t"+ str(rule[0][2])+ "\t\t"+ str(rule[1])+"\n")
outputfile.close()

print("Rules written to output/brill-rules file")