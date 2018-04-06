import itertools

mylist = range(5)

for x,y in itertools.combinations(mylist, 2):
    print(x,y)