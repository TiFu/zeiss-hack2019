import pandas as pd

data = pd.read_csv("../../data/data.csv")
df = data
pd.set_option('display.max_columns', 500)
print(data.loc[data["machineNumber"] == 500363])


#print(list(subset.columns.values))
import matplotlib.pyplot as plt
from datetime import datetime
print(data["machineNumber"].value_counts())


# 151280

#plt.plot(subset["tempBoardSLAVE"])
data = df.sort_values(by=["machineNumber", "remainingLifetime"]).query("remainingLifetime<30")
for machine in data.machineNumber.unique():
    print(machine)
    subset = data.loc[data["machineNumber"] == machine]
    subset["timestamp"] = pd.to_datetime(subset["timestamp"])
    subset = subset.sort_values(by=["timestamp"])
    plt.subplot(3, 1, 1)
    plt.scatter(subset["timestamp"], subset["tempBoardAK0"])
    plt.subplot(3, 1, 2)
    plt.scatter(subset["timestamp"], subset["tempBoardSLAVE"])
    plt.subplot(3, 1, 3)
    plt.scatter(subset["timestamp"], subset["remainingLifetime"])
#plt.plot(subset["remainingLifetime"])
#print(subset["remainingLifetime"])
#print(data.dtypes)

    plt.show()
