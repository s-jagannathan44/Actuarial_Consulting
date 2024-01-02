### Read in the data with Pandas
from datetime import time

import pandas as pd

#s = time.time()
# df = pd.read_csv("C:\\SHAI\FY23-Policy mem data mapped new.csv")
# print(df.columns)
# e = time.time()
# print("Pandas Loading Time = {}".format(e-s))
#
### Read in the data with Modin
import modin.pandas as pd

s = time.time()
df = pd.read_csv("C:\\SHAI\FY23-Policy mem data mapped new.csv")
e = time.time()
print("Modin Loading Time = {}".format(e-s))