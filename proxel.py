from scipy.stats import expon, norm, weibull_min, lognorm
import math
import matplotlib.pyplot as plt
import numpy as np

#10^-12
#TOLERANCE = 0.000000000001
TOLERANCE = 0.0000001


def get_opposite_state(state):
    if state is True:
        return False
    else:
        return True


def delete_proxels_with_low_probability(list_of_proxels):

    marked_for_removal = []
    for proxel in list_of_proxels:
        if proxel.probability < TOLERANCE:
            marked_for_removal.append(proxel)
    for proxel in marked_for_removal:
        #print('Deleting low probability proxels')
        list_of_proxels.remove(proxel)


def calculate_probabity_state_is_true(list_of_proxels):
    probability = 0
    for proxel in list_of_proxels:
        if proxel.state is True:
            probability += proxel.probability
    return probability


def calculate_probabity_state_is_false(list_of_proxels):
    probability = 0
    for proxel in list_of_proxels:
        if proxel.state is False:
            probability += proxel.probability
    return probability


class Proxel:
    def __init__(self, state, timestamp, delta_time, reliability_distribution, maintainability_distribution,
                 probability=1):
        self.state = state
        self.timestamp = timestamp
        self.delta_time = delta_time
        self.reliability_distribution = reliability_distribution
        self.maintainability_distribution = maintainability_distribution
        self.probability = probability

    def compute_probability(self, timestamp):
        #print('Computing for ' + str(self.state))
        # We look at if the state is False, and then we use reliability since we want the transition from
        # state True to state False.
        if self.state is False:
            distribution = self.reliability_distribution
        else:
            distribution = self.maintainability_distribution
        #print('Before Probability: ' + str(self.probability))
        if distribution[0] == 'EXP':
            lambda_ = distribution[1]
            scale_ = 1 / lambda_
            self.probability *= (expon.pdf(timestamp, scale=scale_)/(1 - expon.cdf(timestamp, scale=scale_))) \
                                * self.delta_time
        if distribution[0] == 'WEIBULL':
            scale = distribution[1]
            shape = distribution[2]
            self.probability *= (weibull_min.pdf(timestamp, shape, loc=0, scale=scale) \
                               / (1 - weibull_min.cdf(timestamp, shape, loc=0, scale=scale))) * self.delta_time
        if distribution[0] == 'NORMAL':
            mu = distribution[1]
            sigma = distribution[2]
            self.probability *= (norm.pdf(timestamp, loc=mu, scale=sigma) \
                               / (1 - norm.cdf(timestamp, loc=mu, scale=sigma))) * self.delta_time
        if distribution[0] == 'LOGNORM':
            mu = distribution[1]
            sigma = distribution[2]
            scale = math.exp(mu)
            self.probability *= (lognorm.pdf(timestamp, sigma, loc=0, scale=scale) \
                               / (1 - lognorm.cdf(timestamp, sigma, loc=0, scale=scale))) * self.delta_time

        #print('Probability: ' + str(self.probability))

    def expand_proxel(self):
        # ((A,t),delta_t, ((A, 0)), 1.0 − probability) and ((B, 0),delta_t, ((A, 0)), probability).
        #print('Time stamp: ' + str(self.timestamp))
        #print('Delta time: ' + str(self.delta_time))
        next_timestamp = self.timestamp + self.delta_time

        opposite_state = get_opposite_state(self.state)
        right_node = Proxel(opposite_state, 0, self.delta_time, self.reliability_distribution,
                            self.maintainability_distribution, self.probability)
        right_node.compute_probability(next_timestamp)

        left_node = Proxel(self.state, next_timestamp, self.delta_time, self.reliability_distribution,
                           self.maintainability_distribution, self.probability - right_node.probability)
        #print('Next Time stamp: ' + str(next_timestamp))

        return [left_node, right_node]

    def __repr__(self):
        return '(' + str(self.state) + ', ' + str(self.timestamp) + ', ' + str(self.probability) + ')'


rel_exp_dist = ['EXP', 1/4]
main_exp_dist = ['EXP', 1/2]
norm_dist = ['NORMAL', 3, 1]
lognorm_dist = ['LOGNORM', 2, 1]
rel_weibull_dist = ['WEIBULL', 10, 8]

proxel_list = []

p = Proxel(True, 0, 0.5, norm_dist, main_exp_dist)
proxel_list.append(p)
print(proxel_list)
'''
print(p)
p2 = p.expand_proxel()
print(p2)
p3 = p2[0].expand_proxel()
p4 = p2[1].expand_proxel()

print(p3 + p4)
'''
simultation_time = 20

y = [0]
x = np.linspace(0, 8, 16)
# change range to 1 when plotting
for i in range(1, 16):
    print('Depth: ' + str(i))
    #print(proxel_list)
    new_list = []
    for proxel in proxel_list:
        new_list.extend(proxel.expand_proxel())
    delete_proxels_with_low_probability(new_list)
    proxel_list = new_list
    #print('Number of nodes in layer: ' + str(len(proxel_list)))
    print(len(proxel_list))
    true_probability = calculate_probabity_state_is_true(proxel_list)
    false_probability = calculate_probabity_state_is_false(proxel_list)
    print('Probability for True: ' + str(true_probability))
    print('Probability for False: ' + str(false_probability))
    print('Total probability (shouldnt be more than 1): ' + str(true_probability + false_probability))
    y.append(false_probability)

#print(len(y))

#x = np.linspace(0, 1, 10)
#y = expon.pdf(1, scale=10)/(1 - expon.cdf(x, scale=10)) * x

plt.plot(x, y)
plt.show()
