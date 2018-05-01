import filecmp


def compare_truth_tables(truth_table_1, truth_table_2):
    return filecmp.cmp(truth_table_1, truth_table_2)


# print(compare_truth_tables('truth_table_generated.txt', 'truth_table_reconstructed.txt'))
