from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats

# # Let’s start by sampling uniformly distributed values between 0 and 1:
# x = stats.uniform(0, 1).rvs(10000)
# sns.histplot(x, kde=False)
#
# # Next, we want to transform these samples so that instead of uniform they are now normally distributed. The
# # transform that does this is the inverse of the cumulative density function (CDF) of the normal distribution (which
# # we can get in scipy.stats with ppf):
# norm = stats.distributions.norm()
# x_trans = norm.ppf(x)
# sns.histplot(x_trans)
#
# # If we plot both of them together we can get an intuition for what the inverse CDF looks like and how it works:
# h = sns.jointplot(x)
# h.set_axis_labels('original', 'transformed', fontsize=16)
# plt.show()
# # We can do this for arbitrary (univariate) probability distributions, like the Beta:
# beta = stats.distributions.beta(a=10, b=3)
# x_trans = beta.ppf(x)
# h = sns.jointplot(x)
# h.set_axis_labels('orignal', 'transformed', fontsize=16)
#
# # In order to do the opposite transformation from an arbitrary distribution to the uniform(0, 1)
# # we just apply the inverse of the inverse CDF – the CDF:
#
# x_trans_trans = beta.cdf(x_trans)
# h = sns.jointplot(x_trans)
# h.set_axis_labels('original', 'transformed', fontsize=16)
# plt.show()

# Create samples from a correlated multivariate normal:
mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.5],
                                                     [0.5, 1.]])
# Generate random samples from multivariate normal with correlation .5
x = mvnorm.rvs(100000)
#
h = sns.jointplot(x= x[:, 0], y= x[:, 1], kind='kde')
h.set_axis_labels('X1', 'X2', fontsize=16)
plt.show()

# Now we “uniformify” the marignals
# norm = stats.norm()
# x_unif = norm.cdf(x)
# h = sns.jointplot(x= x_unif[:, 0], y= x_unif[:, 1],  kind='hex')
# h.set_axis_labels('Y1', 'Y2', fontsize=16)
# plt.show()

# This joint plot above is usually how copulas are visualized.

# Now we transform the marginals again to what we want (Gumbel and Beta):
# m1 = stats.gumbel_l()
# m2 = stats.beta(a=10, b=2)
#
# x1_trans = m1.ppf(x_unif[:, 0])
# x2_trans = m2.ppf(x_unif[:, 1])
# print("Plotting")
# h = sns.jointplot(x= x1_trans, y=x2_trans, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0))
# h.set_axis_labels('Maximum river level', 'Probablity of flooding', fontsize=16)
# plt.show()

# Contrast that with the joint distribution without correlations
# x1 = m1.rvs(10000)
# x2 = m2.rvs(10000)
#
# h = sns.jointplot(x=x1, y=x2, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0))
# h.set_axis_labels('Maximum river level', 'Probablity of flooding',  fontsize=16)
# plt.show()

