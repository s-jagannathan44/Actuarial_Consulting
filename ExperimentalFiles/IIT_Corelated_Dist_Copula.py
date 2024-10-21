from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import numpy as np

# from fitter import Fitter, get_common_distributions, get_distributions

df = pd.read_csv("AustralianAutoModified.csv")
# df = df[df["ClaimNb"] > 0]
# df.describe(percentiles=[0.25, 0.5, 0.75, .95]).to_csv("summary.csv")
# df.var().to_csv("var.csv")
x1 = df["ClaimNb"]
x2 = df["KillInjNb"]
a_plus_b = df["A_plus_B"]
# plt.hist(x1,  alpha=0.5, label='x1',color='red')
# plt.hist(x2,  alpha=0.5, label='x2', color='blue')
# plt.hist(a_plus_b,  alpha=0.5, label='x1+x2', color='green')
# plt.legend(loc='upper right')
# plt.show()

mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.95],
                                                     [0.95, 1.]])
x = mvnorm.rvs(15000)
norm = stats.norm()
x_unif = norm.cdf(x)
h = sns.jointplot(x=x_unif[:, 0], y=x_unif[:, 1], kind='scatter')
h.set_axis_labels('Y1', 'Y2', fontsize=16)
plt.show()
m1 = stats.gamma(a=0.532195193066068, scale=1115.06274805659)
m2 = stats.gamma(a=0.851708806158286, scale=763.898780284425)

x1_check = m1.rvs(15000)
x2_check = m2.rvs(15000)
np.savetxt("x1_check.csv", x1_check, delimiter=",")
np.savetxt("x2_check.csv", x2_check, delimiter=",")
# plt.hist(x1,  alpha=0.5, label='x1',color='red')
# plt.hist(x1_check,  alpha=0.5, label='marginal of x1', color='blue')
# plt.legend(loc='upper right')
# plt.show()
# plt.hist(x2,  alpha=0.5, label='x2',color='red')
# plt.hist(x2_check,  alpha=0.5, label='marginal of x2', color='blue')
# plt.legend(loc='upper right')
# plt.show()

x1_trans = m1.ppf(x_unif[:, 0])
x2_trans = m2.ppf(x_unif[:, 1])
a_plus_b_trans = x1_trans + x2_trans
np.savetxt("x1_trans.csv", x1_trans, delimiter=",")
np.savetxt("x2_trans.csv", x2_trans, delimiter=",")
np.savetxt("a_plus_b_trans.csv", a_plus_b_trans, delimiter=",")
# h = sns.jointplot(x=x1_trans, y=x2_trans, kind='scatter')
# h.set_axis_labels('X1', 'X2', fontsize=16)
# plt.show()

# Contrast that with the joint distribution without correlations
xx1 = m1.rvs(10000)
xx2 = m2.rvs(10000)
np.savetxt("xx1.csv", xx1, delimiter=",")
np.savetxt("xx2.csv", xx2, delimiter=",")

# h = sns.jointplot(x=xx1, y=xx2, kind='scatter')
# h.set_axis_labels('X1', 'X2',  fontsize=16)
# plt.show()

plt.hist(a_plus_b, alpha=0.5, label='x1+x2', color='red', weights=np.ones(len(a_plus_b)) / len(a_plus_b),
         histtype='step')
plt.hist(a_plus_b_trans, alpha=0.5, label='x1+x2 from copula', color='green', histtype='step', density=True,
         weights=np.ones(len(a_plus_b_trans)) / len(a_plus_b_trans))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend(loc='upper right')
# plt.show()


# a_plus_b = df["A_plus_B"]
# sns.histplot(a_plus_b ,kde=True)
# plt.show()


# x1 = np.log(df["ClaimNb"])
# x2 = np.log(df["KillInjNb"])
# x1 = df["ClaimNb"]
# x2 = df["KillInjNb"]
# h = sns.jointplot(x=x1, y=x2, kind='scatter', xlim=(0, 2000), ylim=(0, 2000))
# h.set_axis_labels('X1', 'X2', fontsize=16)
# plt.show()

# f = Fitter(x2)
# distributions=['beta',
#                'lognorm',
#                'dweibull',
#                'gausshyper'
#                ])

# f.fit()
# print(f.get_best(method='sumsquare_error'))
# print(f.summary())
# print(f.fitted_param["lognorm"])

# mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.95],
#                                                      [0.95, 1.]])
# Generate random samples from multivariate normal with correlation .5
# x = mvnorm.rvs(15000)

# h = sns.jointplot(x=x[:, 0], y=x[:, 1], kind='scatter')
# h.set_axis_labels('X1', 'X2', fontsize=16)
# plt.show()

# norm = stats.norm()
# x_unif = norm.cdf(x)
# h = sns.jointplot(x= x_unif[:, 0], y= x_unif[:, 1],  kind='scatter')
# h.set_axis_labels('Y1', 'Y2', fontsize=16)
# plt.show()

# m1 = stats.dweibull(c=1.6905574433366104, loc=5.333725395647891, scale=1.5418778071544565)
# m2 = stats.gausshyper(a=2.535371945792323, b=0.5993361481185665, c=-5.547493116017217, z=0.6070235024156361,
#                       loc=3.3338729356221934, scale=5.009204935968379)

# m1 = stats.beta(a=2.42, b=2.51, loc=1.41, scale=7.77)
# m2 = stats.beta(a=2.11, b=2.47, loc=3.33, scale=5.44)
# m1 = stats.lognorm(s=1.7, loc=4.11, scale=168.57)
# m1 = stats.gamma(a=0.532195193066068, scale=1115.06274805659)
# m2 = stats.gamma(a=0.851708806158286, scale=763.898780284425)
#
# x1_check = m1.rvs(15000)
# x2_check = m2.rvs(15000)
# x1_trans = m1.ppf(x_unif[:, 0])
# x2_trans = m2.ppf(x_unif[:, 1])
# a_plus_b_trans = x1_trans + x2_trans
# print(x1_trans.mean())
# print(x2_trans.mean())
# print(a_plus_b_trans.mean())
# sns.histplot(a_plus_b_trans)
# plt.show()

# h = sns.jointplot(x=x1_trans, y=x2_trans, kind='scatter', xlim=(0, 30000), ylim=(0, 30000))
# h.set_axis_labels('X1', 'X2', fontsize=16)
# plt.show()

# f = Fitter(x2)
# f.fit()
# print(f.get_best(method = 'sumsquare_error'))


# from matplotlib import pyplot as plt
# import seaborn as sns
# from scipy import stats
#
# # # Let’s start by sampling uniformly distributed values between 0 and 1:
# # x = stats.uniform(0, 1).rvs(10000)
# # sns.displot(x)
# #
# # Next, we want to transform these samples so that instead of uniform they are now normally distributed. The
# # transform that does this is the inverse of the cumulative density function (CDF) of the normal distribution (which
# # we can get in scipy.stats with ppf):
# # norm = stats.distributions.norm()
# # x_trans = norm.ppf(x)
# # sns.histplot(x_trans)
#
# # # We can do this for arbitrary (univariate) probability distributions, like the Beta:
# # beta = stats.distributions.beta(a=10, b=3)
# # x_trans = beta.ppf(x)
# #
# # # In order to do the opposite transformation from an arbitrary distribution to the uniform(0, 1)
# # # we just apply the inverse of the inverse CDF – the CDF:
# #
# # x_trans_trans = beta.cdf(x_trans)
# # h = sns.displot(x_trans_trans)
#
# # Create samples from a correlated multivariate normal:
# mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.5],
#                                                      [0.5, 1.]])
# # Generate random samples from multivariate normal with correlation .5
# x = mvnorm.rvs(15000)
# #
# # h = sns.jointplot(x=x[:, 0], y=x[:, 1], kind='scatter')
# # h.set_axis_labels('X1', 'X2', fontsize=16)
#
# # Now we “uniformify” the marignals
# norm = stats.norm()
# x_unif = norm.cdf(x)
# # h = sns.jointplot(x= x_unif[:, 0], y= x_unif[:, 1],  kind='hex')
# # h.set_axis_labels('Y1', 'Y2', fontsize=16)
# # plt.show()
#
# # This joint plot above is usually how copulas are visualized.
#
# # Now we transform the marginals again to what we want (Gumbel and Beta):
# m1 = stats.gumbel_l()
# m2 = stats.beta(a=10, b=2)
# # #
# # x1_trans = m1.ppf(x_unif[:, 0])
# # x2_trans = m2.ppf(x_unif[:, 1])
# # h = sns.jointplot(x= x1_trans, y=x2_trans, kind='scatter', xlim=(-6, 2), ylim=(.6, 1.0))
# # h.set_axis_labels('X1', 'X2', fontsize=16)
# # plt.show()
#
# # Contrast that with the joint distribution without correlations
# x1 = m1.rvs(10000)
# x2 = m2.rvs(10000)
#
# h = sns.jointplot(x=x1, y=x2, kind='scatter', xlim=(-6, 2), ylim=(.6, 1.0))
# h.set_axis_labels('X1', 'X2',  fontsize=16)
# plt.show()
