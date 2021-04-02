import numpy as np
from math import sqrt
from operator import itemgetter

"""u.data: user ID, movie ID, rating, watched lengths """
ratingList = []
file = open('u.data')

for i in file:
    splited = i.split("\t")
  
    ratingList.append((int(splited[0]),int(splited[1]),int(splited[2])))

rating = np.array(ratingList)

a = max(l[0] for l in rating)
b = max(l[1] for l in rating)
userRating = np.zeros((a+1,b+1))
for i in rating:
    userRating[[i[0]],[i[1]]] = i[2]

p_count = 0
for i in range(b+1):
    if userRating[6][i] > 0:
        p_count +=1
    if p_count == 10:
        break


def computeCosineSimilarity(userRating, movieX, movieY):
    aibi = ai_square = bi_square = numPairs = 0
    for i in range(a):
        if userRating[i][movieX] > 0 and userRating[i][movieY] > 0:
            aibi += userRating[i][movieX]* userRating[i][movieY]
            ai_square += userRating[i][movieX]**2
            bi_square += userRating[i][movieY]**2
            numPairs +=1
  
    if ai_square == 0:
        return (0,0)
    score = aibi / (sqrt(ai_square) * sqrt(bi_square))
    
    
    
    return (score, numPairs)


def similarMovie(userRating, movie, scoreThreshold = 0.97, coOccurenceThreshold = 50):
    similarity = []
    for i in range(userRating.shape[1]):
        if i == movie:
            continue
        sim = computeCosineSimilarity(userRating, movie, i)
        if sim[0] > scoreThreshold and sim[1] > coOccurenceThreshold:
            similarity.append((i,sim[0],sim[1]))

    rank_similarity = sorted(similarity, key = itemgetter(1, 2), reverse = True)
   
    return rank_similarity


nameDict = {}
def loadMovieNames():
    movieNames = {}
    with open("u.item", encoding='ascii', errors='ignore') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

nameDict = loadMovieNames()

rank = similarMovie(userRating, 1)
print("Top similar movies with " + nameDict[1] + "are:")
count = 1
for movieID, sim, pairs in rank:
    print("rank " + str(count) + ": " + nameDict[movieID])
    count += 1
