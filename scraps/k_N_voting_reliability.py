from functools import reduce


def k_N_voting(k, N, input_reliabilities):
    """
    Pseudocode on page 38 of Fault tree analysis: A survey of the state-of-the-art
    in modeling, analysis and tools
    Using recursion to calculate reliability when the gate is k/N Voting

    :param k:
    :param N:
    :param input_reliabilities:
    :return:
    """
    if k == 0:
        return 1
    if k == N:
        return reduce(lambda x, y: x*y, input_reliabilities)
    
    result = input_reliabilities[0] * k_N_voting(k - 1, N - 1, input_reliabilities[1:]) + \
                    (1 - input_reliabilities[0]) * k_N_voting(k, N - 1, input_reliabilities[1:])
    return result


prob = [0.5, 0.6, 0.8]
print(k_N_voting(2, 3, prob))
