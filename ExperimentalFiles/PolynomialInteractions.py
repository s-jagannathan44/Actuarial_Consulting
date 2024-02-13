import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, OrdinalEncoder

df = pd.DataFrame({'a': ['red', 'e', 'bl', 'ue'],
                   'b': ['high', 'low', 'hi', 'ow'],
                   'x': [1, 1, 1, 2],
                   'y': [2, 3, 4, 2],
                   'z': [9, 8, 7, 6]
                   })

# interactions for features with no individual preprocessing works fine,
# i.e. numerical ones
column_trans = ColumnTransformer(
    [('xy_num',
      PolynomialFeatures(degree=2, interaction_only=True, include_bias=False),
      ['x', 'y']),
     ('yz_num',
      PolynomialFeatures(degree=2, interaction_only=True, include_bias=False),
      ['y', 'z'])
     ],
    remainder='drop')
dy = column_trans.fit_transform(df)

# interactions for ohe encoded also works with helper function
cat_cat = make_pipeline(
    OrdinalEncoder(),
    PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
)
column_trans = ColumnTransformer(
    [('ab_cat', cat_cat, ['a', 'b'])],
    remainder='drop')
dz = column_trans.fit_transform(df)
pass
