import numpy as np
import matplotlib.pyplot as plt

# Create data
N = 100
x = np.array([])
y = np.array([])

y_mean = np.random.choice(np.arange(0,5,0.5))
x_mean = np.random.choice(np.arange(0,5,0.5))
variance = 0.5

x_min = x_mean - variance
x_max = x_mean + variance
if x_min < 0:
    x_min =0
if x_max > 5:
    x_max = 5

y_min = y_mean - variance
y_max = y_mean + variance
if y_min < 0:
    y_min =0
if y_max > 5:
    y_max = 5

for _ in range(N):
    payoff_array = np.zeros(4)
    # A
    payoff_array[0] = np.random.random(1)*5
    #D
    payoff_array[3] = np.random.random(1)*5
    #B
    payoff_array[1] = x_min + np.random.random(1)*(x_max - x_min)
    #C
    payoff_array[2] = y_min + np.random.random(1)*(y_max - y_min)

    x_payoffs = np.reshape(payoff_array, (-1, 2))
    y_payoffs = np.reshape(np.transpose(x_payoffs), (-1, 2))
    x_pay_array = np.reshape(x_payoffs, (1,4))
    y_pay_array = np.reshape(y_payoffs, (1,4))
    x = np.concatenate((x, x_pay_array[0]))
    y = np.concatenate((y, y_pay_array[0]))


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

plt.title('Semi-Localised Symmetric Games')
# plt.legend(loc=2)
plt.savefig('Semi-Localised Symmetric Games.png', dpi=300, bbox_inches='tight')
plt.show()
