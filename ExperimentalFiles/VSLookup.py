import pandas as pd

# Create DataFrame1
dataFrame1 = pd.DataFrame(
   {
      "Key": ["102", "305"],
      "Col2": [10, 30],
      "Col3": [2, 5]
   },
)

print(dataFrame1)

# Create DataFrame2
dataFrame2 = pd.DataFrame(
   {
      "Col1": [30, 30, 30, 30, 30, 10, 10],
      "Key": ["305", "305", "305", "305", "305", "102", "102"]
   },
)

print(dataFrame2)

dataFrame3 = pd.merge(dataFrame1, dataFrame2,  on='Key')

print(dataFrame3)