import itertools


p = {0, 1, 2}
children = [{0, 1}, {0, 2}, {1, 2}]
for x, y in itertools.permutations(children, 2):
    print(x, y)

print('----------------------------------')
for x in children:
    # Get another cut_set(_under_test) from cut_sets
    for y in children:
        # Check if the two cut_set are not the same
        if x != y:
            print(x, y)

print('----------------------------------')

# is_EVEN = lambda i: i % 2 == 0
# is_ODD = lambda i: i % 2 == 1


def is_EVEN(i): return i % 2 == 0


def is_ODD(i): return i % 2 == 1


print(is_EVEN(10))
