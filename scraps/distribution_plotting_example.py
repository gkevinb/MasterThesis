from modules import timeseries, distributionplotting as DP


size = 10000
#y = timeseries._generate_numbers(['EXP', 1/5], size)
#y = timeseries._generate_numbers(['NORMAL', 15, 2], size)
y = timeseries._generate_numbers(['WEIBULL', 60, 10], size)
#y = timeseries._generate_numbers(['LOGNORM', 1, 0.5], size)
print(max(y))
#DP.plot_exp('Name', 'Reliability',['EXP', 1/5], y)
#DP.plot_normal('Name', 'Reliability', ['NORMAL', 15, 2], y)
#DP.plot_lognorm('Name', 'Rel', ['LOGNORM', 1, 0.5], y)
#DP.plot_weibull('Name', 'Rel', ['WEIBULL', 60, 10], y)
DP.plot_arbitrary_distribution('Name', y)
