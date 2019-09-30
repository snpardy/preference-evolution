import numpy as np
import matplotlib.pyplot as plt

# Create data
N = 100
x = np.array([])
y = np.array([])

for _ in range(N):
    x_payoffs = np.reshape((np.random.random(4)*5), (-1, 2))
    y_payoffs = np.reshape((np.random.random(4)*5), (-1, 2))
    x_pays = np.reshape(x_payoffs, (1,4))
    y_pays = np.reshape(y_payoffs, (1,4))
    x = np.concatenate((x, x_pays[0]))
    y = np.concatenate((y, y_pays[0]))

y_mean = np.random.choice(np.arange(0,5,0.5))
x_mean = np.random.choice(np.arange(0,5,0.5))

mean = (x_mean, y_mean)

data = (mean, (x,y))
colors = ("green", "pink")
groups = ("mutation", "payoffs")
areas = (np.pi*200, np.pi*5)

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for data, color, group, area in zip(data, colors, groups, areas):
    x, y = data
    ax.scatter(x, y, s=area, alpha=0.8, c=color, edgecolors='none', label=group)

plt.title('Symmetric Games')
# plt.legend(loc=2)
plt.show()
