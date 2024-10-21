from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import numpy as np
# from fitter import Fitter, get_common_distributions, get_distributions

df = pd.read_csv("AustralianAutoModified.csv")
# Step 1 Print summary statistics
df = df[df["ClaimNb"] > 0]
df.describe(percentiles=[0.25, 0.5, 0.75, .95]).to_csv("summary.csv")
df.var().to_csv("var.csv")

# Step 2 plot histograms of draw data
x1 = df["ClaimNb"]
x2 = df["KillInjNb"]
a_plus_b = df["A_plus_B"]
plt.hist(x1,  alpha=0.5, label='x1',color='red')
plt.hist(x2,  alpha=0.5, label='x2', color='blue')
plt.hist(a_plus_b,  alpha=0.5, label='x1+x2', color='green')
plt.legend(loc='upper right')
plt.show()

# Step 3 Create samples from a correlated multivariate normal:
mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.95],
                                                     [0.95, 1.]])
# Generate random samples from multivariate normal with correlation .95
x = mvnorm.rvs(15000)
# Now we “uniformify” the marignals
norm = stats.norm()
x_unif = norm.cdf(x)
h = sns.jointplot(x=x_unif[:, 0], y=x_unif[:, 1], kind='scatter')
h.set_axis_labels('Y1', 'Y2', fontsize=16)
plt.show()

# Step 4 Now we transform the marginals again to what we want
# (Gamma with parameters obtained by fitting x1 and x22 via a distribution fitting tool  ):
m1 = stats.gamma(a=0.532195193066068, scale=1115.06274805659)
m2 = stats.gamma(a=0.851708806158286, scale=763.898780284425)

# Generate random samples from above models m1 and m2 for comparison with raw data x1 and x2
x1_check = m1.rvs(15000)
x2_check = m2.rvs(15000)
np.savetxt("x1_check.csv", x1_check, delimiter=",")
np.savetxt("x2_check.csv", x2_check, delimiter=",")

plt.hist(x1,  alpha=0.5, label='x1',color='red')
plt.hist(x1_check,  alpha=0.5, label='marginal of x1', color='blue')
plt.legend(loc='upper right')
plt.show()
# plot histograms of x1 and x2 against the random samples generated from  models m1 and m2
plt.hist(x2,  alpha=0.5, label='x2',color='red')
plt.hist(x2_check,  alpha=0.5, label='marginal of x2', color='blue')
plt.legend(loc='upper right')
plt.show()

x1_trans = m1.ppf(x_unif[:, 0])
x2_trans = m2.ppf(x_unif[:, 1])
a_plus_b_trans = x1_trans + x2_trans
np.savetxt("x1_trans.csv", x1_trans, delimiter=",")
np.savetxt("x2_trans.csv", x2_trans, delimiter=",")
np.savetxt("a_plus_b_trans.csv", a_plus_b_trans, delimiter=",")
# plot joint distribution generated from m1 and m2 using inverse function
h = sns.jointplot(x=x1_trans, y=x2_trans, kind='scatter')
h.set_axis_labels('X1', 'X2', fontsize=16)
plt.show()

# Contrast that with the joint distribution generated from random samples without correlations
xx1 = m1.rvs(10000)
xx2 = m2.rvs(10000)
np.savetxt("xx1.csv", xx1, delimiter=",")
np.savetxt("xx2.csv", xx2, delimiter=",")

h = sns.jointplot(x=xx1, y=xx2, kind='scatter')
h.set_axis_labels('X1', 'X2',  fontsize=16)
plt.show()

plt.hist(a_plus_b, alpha=0.5, label='x1+x2', color='red', weights=np.ones(len(a_plus_b)) / len(a_plus_b),
         histtype='step')
plt.hist(a_plus_b_trans, alpha=0.5, label='x1+x2 from copula', color='green', histtype='step', density=True,
         weights=np.ones(len(a_plus_b_trans)) / len(a_plus_b_trans))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend(loc='upper right')
plt.show()
