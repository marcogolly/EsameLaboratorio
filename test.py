file = open("test.csv", "r")
data = []
for line in file:
  data.append(float(line.split(",")[1]))
print(sum(data)/len(data))