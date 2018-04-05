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

sets = [{0, 1}, {0, 2}, {1, 2}]
parent = {0, 1, 2}
children = [{0, 1}, {0, 2}, {1, 2, 3, 4}]
# print(ftr.convert_list_of_sets_to_list(sets))
print(ftr.is_children_n_choose_k_of_parent(parent, children))
print(ftr.check_n_choose_k_pattern(parent, children))
# compress_interconnected_sets

# Combine the above three functions to make the k/N voting gate reconstruction better
