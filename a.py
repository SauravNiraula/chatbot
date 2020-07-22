listA = ['apple', 'orange', 'apple', 'apple', 'banana', 'orange'] # (length = 6)
listB = ['apple', 'orange', 'grapefruit', 'apple'] # (length = 4)

from collections import Counter
import math

counterA = Counter(listA)
counterB = Counter(listB)

data_set = set(counterA).union(counterB)

for k in data_set:
    counterA.get(k, 0)




def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


print(counter_cosine_similarity(counterA, counterB))