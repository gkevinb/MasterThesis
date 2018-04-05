import faultTreeReconstruction as ftr

# cut_sets = [[1, 2], [3, 4]]
# cut_sets = [[1, 3], [1, 4], [2, 3], [2, 4]]
# cut_sets = ((1,), (2,))

# cut_sets = ((1, 2), (3,), (4,))
# cut_sets = ((1, 2),)
# cut_sets = [[1, 2, 3], [1, 2, 4]]

# 2/3 (k/N) Voting cut set
# cut_sets = ((1, 2), (1, 3), (2, 3))
cut_sets = [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5]]

ftr.reconstruct_fault_tree(cut_sets)
