import random


def _generate_numbers(distribution, length):
    """
    Generate random numbers of length according to the distribution.
    :param distribution: A list which holds information about a distribution and its parameters,
    first element is always the name, the rest depends on the distribution.
    Ex: exponential distribution = distribution = ['EXP', lambda]
    :param length: The length of random numbers to be generated
    :return: A list of random numbers
    """
    name, *parameters = distribution
    random_numbers = []
    if name == 'EXP':
        lambda_, = parameters
        for i in range(length):
            num = random.expovariate(lambda_)
            random_numbers.append(num)
    if name == 'WEIBULL':
        scale_, shape_ = parameters
        for i in range(length):
            num = random.weibullvariate(scale_, shape_)
            random_numbers.append(num)
    if name == 'LOGNORM':
        mu_, sigma_ = parameters
        for i in range(length):
            num = random.lognormvariate(mu_, sigma_)
            random_numbers.append(num)
    if name == 'NORMAL':
        mu_, sigma_ = parameters
        for i in range(length):
            num = random.normalvariate(mu_, sigma_)
            random_numbers.append(num)
    return random_numbers


def _merge_streams(stream1, stream2):
    """
    Merges two streams of data into one, by taking the first element from the first stream,
    then first element from second stream, then second element from first, second from second,
    and so on.
    :param stream1: First stream of data
    :param stream2: Second stream of data
    :return: Returns merged stream of the two streams of data
    """
    stream_total = []
    if len(stream1) == len(stream2):
        for i in range(len(stream1)):
            stream_total.append(stream1[i])
            stream_total.append(stream2[i])
    return stream_total


def _create_time_series(stream):
    """
    Create time series from stream of data by keeping the first element the same,
    but afterwards the next elements will also have the time from the previous
    elements added to it.
    Example: stream = [4, 3, 1, 6]
             time series = [4, 7, 8, 14]
    :param stream: Stream of data
    :return: Time series data
    """
    time_series = [stream[0]]
    for i in range(len(stream) - 1):
        time_series.append(time_series[i] + stream[i + 1])
    return time_series


def generate_time_series(reliability_dist, maintainability_dist, size):
    """
    Generate time series according to distributions
    :param reliability_dist:
    :param MTTF:
    :param maintainability_dist:
    :param MTTR:
    :param size:
    :return:
    """

    time_to_failure = _generate_numbers(reliability_dist, size)
    time_to_repair = _generate_numbers(maintainability_dist, size)

    '''
    # For logging
    print('Time to failure')
    print(time_to_failure)
    print('Average: ' + str(sum(time_to_failure)/len(time_to_failure)))
    print('Length: ' + str(len(time_to_failure)))
    print('Time to repair')
    print(time_to_repair)
    print('Average: ' + str(sum(time_to_repair)/len(time_to_repair)))
    print('Length: ' + str(len(time_to_repair)))
    '''

    times = _merge_streams(time_to_failure, time_to_repair)
    '''
    print(times)
    '''
    time_series = _create_time_series(times)
    return time_series
