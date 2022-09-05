from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Output\\X_test.csv")

t = df.GroupId
mu1 = df.Actual
mu2 = df.Predicted


# plot it!
fig, ax = plt.subplots(1)
ax.plot(t, mu1, lw=2, label='Actual')
ax.plot(t, mu2, lw=2, label='Predicted')
ax.set_title('Actual Vs Predicted Claims by Group')
ax.legend(loc='upper left')
ax.set_xlabel('GroupId')
ax.set_ylabel('Claims')
ax.grid()
plt.show()
