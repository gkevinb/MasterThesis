from modules import timeseries, distributionplotting as DP


size = 10000
#y = timeseries._generate_numbers(['EXP', 1/5], size)
#y = timeseries._generate_numbers(['NORMAL', 15, 2], size)
#y = timeseries._generate_numbers(['WEIBULL', 3, 2], size)
#y = timeseries._generate_numbers(['LOGNORM', 1, 0.5], size)
#print(max(y))

#DP.plot_exp('Name', 'Reliability', ['EXP', 1/5], y)
#DP.plot_normal('Name', 'Maintainability', ['NORMAL', 15, 2], y)
#DP.plot_lognorm('Name', 'Maintainability', ['LOGNORM', 1, 0.5], y)
#DP.plot_weibull('Name', 'Maintainability', ['WEIBULL', 3, 2], y)


#ts = timeseries.generate_time_series(['NORMAL', 15, 2], ['WEIBULL', 3, 2], 10000)
#y = timeseries.calculate_time_differences(ts)

#DP.plot_arbitrary_distribution('Name', y)

DP.plot_()
