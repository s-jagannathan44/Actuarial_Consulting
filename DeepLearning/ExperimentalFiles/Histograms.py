import pandas as pd

from matplotlib import pyplot as plt

# Generate data on commute times.
commutes = pd.read_csv("Output\\freq_pred.csv")
print(commutes.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.95, 1]))
ax = commutes.plot.hist(alpha=0.5, grid=True, bins=50, rwidth=None,
                        color='#607c8e')
plt.title('Histogram for FMTPL Claims <5000')
plt.xlabel('Claim Amount')
plt.ylabel('Count')

ax.grid()
plt.show()

'''
commutes.hist(column="Actual",
              xlabelsize=20, ylabelsize=20,
              xrot=45, bins=5, color='orange')

plt.show()

commutes.hist(column="Predicted",
              xlabelsize=20, ylabelsize=20,
              xrot=45, bins=5, color='orange')

plt.show()
'''
