import pandas as pd
from distfit import distfit
from matplotlib import pyplot as plt

# Generate 10000 normal distribution samples with mean 0, std dev of 3
dataset = pd.read_csv("weight_height.csv")
# Initialize distfit
dist = distfit()
# Determine best-fitting probability distribution for data
results = dist.fit_transform(dataset["Weight"].values)
# Plot results
# dist.plot()
# plt.show()

df = pd.read_csv("Sheet2.csv")
dist.predict(df["Weight"].values, todf=True)
