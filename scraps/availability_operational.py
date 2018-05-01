from modules import timeseries


is_EVEN = lambda i: i % 2 == 0
is_ODD = lambda i: i % 2 == 1


def get_time_series_up_to(time_series, up_to_time):
    time_series_up_to = []
    for i in range(0, len(time_series)):
        if time_series[i] < up_to_time:
            time_series_up_to.append(time_series[i])
        else:
            break
    return time_series_up_to


def calculate_up_time(time_series):
    return timeseries.calculate_time_to_failures(time_series)


def calculate_remaining_time(time_series, up_to_time):
    if is_EVEN(len(time_series)):
        return up_to_time - time_series[-1]
    else:
        return 0


def calculate_total_up_time_up_to(time_series, up_to_time):
    if up_to_time < time_series[-1]:
        time_series_up_to = get_time_series_up_to(time_series, up_to_time)
        up_times = calculate_up_time(time_series_up_to)

        total_up_time = sum(up_times)
        total_up_time += calculate_remaining_time(time_series_up_to, up_to_time)

        return total_up_time
    else:
        return 0


def calculate_operational_availability(time_series, operating_cycle):
    if operating_cycle < time_series[-1]:
        up_time = calculate_total_up_time_up_to(time_series, operating_cycle)
        return up_time / operating_cycle
    else:
        return 0


rel_exp_dist = ['EXP', 1/4]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 240, 10]
main_exp_dist = ['EXP', 1/2]

ts = timeseries.generate_time_series(rel_exp_dist, main_exp_dist, 10000)
#ts = [3, 5, 8, 10, 15, 18]
#ts = [8, 17, 20, 24, 32, 42]
print(len(ts))
print(ts[-1])

up_to = 12000

print('Total uptime: ' + str(calculate_total_up_time_up_to(ts, up_to)))

print('Operating Availability: ' + str(calculate_operational_availability(ts, up_to)))