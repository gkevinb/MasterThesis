import seaborn.apionly as sns
import numpy as np; np.random.seed(0)
import matplotlib.pyplot as plt

x = np.random.randn(100)
print(type(x))
ax = sns.distplot(x, hist_kws={"ec":"k"})
data_x, data_y = ax.lines[0].get_data()
print(data_x)
print(data_y)
xi = 0 # coordinate where to find the value of kde curve
yi = np.interp(xi,data_x, data_y)
print ("x={},y={}".format(xi, yi)) # prints x=0,y=0.3698
ax.plot([0],[yi], marker="o")


fig, subplots = plt.subplots(1, 1)
subplots.plot(data_x, data_y)
plt.show()
