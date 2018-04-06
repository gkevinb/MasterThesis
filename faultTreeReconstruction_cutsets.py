from modules import faultTreeReconstruction as ftr

# minimal_cut_sets = [[1, 2], [3, 4]]
# minimal_cut_sets = [[1, 3], [1, 4], [2, 3], [2, 4]]
# minimal_cut_sets = ((1,), (2,))

# minimal_cut_sets = ((1, 2), (3,), (4,))
# minimal_cut_sets = ((1, 2),)
minimal_cut_sets = [[1, 2, 3], [1, 2, 4]]

# 2/3 (k/N) Voting cut set
# minimal_cut_sets = ((1, 2), (1, 3), (2, 3))
# minimal_cut_sets = [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5]]

# minimal_cut_sets = [[1, 3, 4, 5], [1, 3, 4, 6, 7], [2, 3, 4, 6, 7], [1, 2, 6, 7], [1, 2, 5], [2, 3, 4, 5]]

ftr.reconstruct_fault_tree(minimal_cut_sets, 'testFT.py')
