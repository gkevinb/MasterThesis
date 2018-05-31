from scipy.stats import expon, norm, weibull_min, lognorm
import math
import matplotlib.pyplot as plt
import numpy as np

#10^-12
#TOLERANCE = 0.000000000001
TOLERANCE = 0.00000001


def get_opposite_state(state):
    if state is True:
        return False
    else:
        return True


class ProxelNetwork:
    def __init__(self, delta_time, simulation_time, reliability_distribution, maintainability_distribution):
        self.initial_proxel = Proxel(True, 0)
        self.delta_time = delta_time
        self.simulation_time = simulation_time
        self.reliability_distribution = reliability_distribution
        self.maintainability_distribution = maintainability_distribution
        self.current_proxels = [self.initial_proxel]
        self.time_series = [0]
        self.probability_of_failure = [0]
        self.probability_of_OK = [1]

    def delete_proxels_with_low_probability(self):
        marked_for_removal = []
        for proxel in self.current_proxels:
            if proxel.probability < TOLERANCE:
                marked_for_removal.append(proxel)
        for proxel in marked_for_removal:
            self.current_proxels.remove(proxel)

    def add_delta_time_to_time_series(self):
        next_timestamp = self.time_series[-1] + self.delta_time
        self.time_series.append(next_timestamp)

    def calculate_probabity_state_is_true(self):
        probability = 0
        for proxel in self.current_proxels:
            if proxel.state is True:
                probability += proxel.probability
        self.probability_of_OK.append(probability)

    def calculate_probabity_state_is_false(self):
        probability = 0
        for proxel in self.current_proxels:
            if proxel.state is False:
                probability += proxel.probability
        self.probability_of_failure.append(probability)

    def compute_probability(self, proxel, timestamp):
        #print('Computing for ' + str(self.state))
        # We look at if the state is False, and then we use reliability since we want the transition from
        # state True to state False.
        if proxel.state is False:
            distribution = self.reliability_distribution
        else:
            distribution = self.maintainability_distribution
        #print('Before Probability: ' + str(self.probability))
        if distribution[0] == 'EXP':
            lambda_ = distribution[1]
            scale_ = 1 / lambda_
            proxel.probability *= (expon.pdf(timestamp, scale=scale_)/(1 - expon.cdf(timestamp, scale=scale_))) \
                                   * self.delta_time
        if distribution[0] == 'WEIBULL':
            scale = distribution[1]
            shape = distribution[2]
            proxel.probability *= (weibull_min.pdf(timestamp, shape, loc=0, scale=scale)
                                   / (1 - weibull_min.cdf(timestamp, shape, loc=0, scale=scale))) * self.delta_time
        if distribution[0] == 'NORMAL':
            mu = distribution[1]
            sigma = distribution[2]
            proxel.probability *= (norm.pdf(timestamp, loc=mu, scale=sigma)
                                   / (1 - norm.cdf(timestamp, loc=mu, scale=sigma))) * self.delta_time
        if distribution[0] == 'LOGNORM':
            mu = distribution[1]
            sigma = distribution[2]
            scale = math.exp(mu)
            proxel.probability *= (lognorm.pdf(timestamp, sigma, loc=0, scale=scale)
                                   / (1 - lognorm.cdf(timestamp, sigma, loc=0, scale=scale))) * self.delta_time

    def expand_proxel(self, proxel):
        # ((A,t),delta_t, ((A, 0)), 1.0 − probability) and ((B, 0),delta_t, ((A, 0)), probability).
        next_timestamp = proxel.timestamp + self.delta_time

        opposite_state = get_opposite_state(proxel.state)
        right_node = Proxel(opposite_state, 0, proxel.probability)
        self.compute_probability(right_node, next_timestamp)

        left_node = Proxel(proxel.state, next_timestamp, proxel.probability - right_node.probability)

        return [left_node, right_node]

    def expand_network(self):
        stop = int(self.simulation_time / self.delta_time)
        for i in range(1, stop):
            print('Depth: ' + str(i))
            next_proxels = []
            for proxel in self.current_proxels:
                next_proxels.extend(self.expand_proxel(proxel))
            self.current_proxels = next_proxels
            self.delete_proxels_with_low_probability()
            print('Number of nodes in layer: ' + str(len(self.current_proxels)))
            #print(self.current_proxels)
            self.add_delta_time_to_time_series()
            self.calculate_probabity_state_is_true()
            self.calculate_probabity_state_is_false()
            total_probability = (self.probability_of_OK[-1] + self.probability_of_failure[-1])
            print('Total Probability: ' + str(total_probability))
            if total_probability < 0.999 or total_probability > 1.001:
                print('INVALID RESULT DUE TO TOTAL PROBABILITY TOO FAR FROM 1')
                break


class Proxel:
    def __init__(self, state, timestamp, probability=1.0):
        self.state = state
        self.timestamp = timestamp
        self.probability = probability

    def __repr__(self):
        return '(' + str(self.state) + ', ' + str(self.timestamp) + ', ' + str(self.probability) + ')'

