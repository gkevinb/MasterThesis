import random

'''
Generate random numbers based on a specific distribution.
Arguments:
distribution - a list which holds information about a distribution and its parameters,
    first element is always the name, the rest depends on the distribution.
    Ex: exponential distribution = distribution = ['EXP', lambda]
size - is the amount of random numbers to be generated
Returns: a list of random numbers
'''


def generate_numbers(distribution, length):
    name, *parameters = distribution
    random_numbers = []
    if name == 'EXP':
        lambd, = parameters
        for i in range(length):
            num = random.expovariate(lambd)
            random_numbers.append(num)
    return random_numbers


'''
Merges two streams of data into one, by taking the first element from the first stream,
then first element from second stream, then second element from first, second from second,
and so on.
Arguments:
stream1 - first stream of data
stream2 - second stream of data
Returns merged stream of the two streams of data
'''


def merge_streams(stream1, stream2):
    stream_total = []
    if len(stream1) == len(stream2):
        for i in range(len(stream1)):
            stream_total.append(stream1[i])
            stream_total.append(stream2[i])
    return stream_total


'''
Create time series from stream of data by keeping the first element the same,
but afterwards the next elements will also have the time from the previous
elements added to it.
Example: stream = [4, 3, 1, 6]
    time series = [4, 7, 8, 14]
Arguments:
stream - stream of data
Returns: time series data 
'''


def create_time_series(stream):
    time_series = [stream[0]]
    for i in range(len(stream) - 1):
        time_series.append(time_series[i] + stream[i + 1])
    return time_series


def generate_time_series(reliability_dist, mttf, maintainability_dist, mttr, size):
    dist1 = [reliability_dist, 1/mttf]
    dist2 = [maintainability_dist, 1/mttr]

    time_to_failure = generate_numbers(dist1, size)
    time_to_repair = generate_numbers(dist2, size)

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

    times = merge_streams(time_to_failure, time_to_repair)
    '''
    print(times)
    '''
    time_series = create_time_series(times)
    return time_series
