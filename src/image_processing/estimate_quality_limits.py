import numpy as np

data = np.loadtxt("./displacements.csv", delimiter=",")

left = np.abs(data[:,2]) + np.abs(data[:, 3])# * data[:, 3]
right = np.abs(data[:, 5]) + np.abs(data[:, 6])# * data[:, 6]
print(left)
print(right)
together = np.append(np.array(left), np.array(right))
together.sort()

print(np.max(together))

print("50%: " + str(np.percentile(together, 50)))
print("80%: " + str(np.percentile(together, 80)))
print("100%: " + str(np.percentile(together, 100)))