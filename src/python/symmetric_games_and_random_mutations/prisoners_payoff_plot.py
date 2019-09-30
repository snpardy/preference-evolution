import numpy as np
import matplotlib.pyplot as plt

# Create data
x = np.array([3,0,4,1])
y = np.array([3,4,0,1])


# Uncomment for payoff and mutation
data = (tuple(np.random.rand(2)*5), (x,y))
colors = ("green", "orange")
groups = ("Mutation", "Payoff point")
areas = (np.pi*200, np.pi*12)

# Uncomment for just payoff points
# data = [(x,y)]
# colors = ["orange"]
# groups = ["Payoff point"]
# areas = [np.pi*12]

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for data, color, group, area in zip(data, colors, groups, areas):
    x, y = data
    ax.scatter(x, y, s=area, alpha=0.8, c=color, edgecolors='none', label=group)

plt.xlim(-0.5,5)
plt.ylim(-0.5,5)
plt.title("Prisoner's Dilemma Payoff Points with a Random Mutation")

lgnd = plt.legend(loc="upper right", scatterpoints=1, fontsize=10)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]

plt.savefig('prisoners_dilemma_payoffs_and_mutation.png', dpi=300, bbox_inches='tight')
plt.show()
