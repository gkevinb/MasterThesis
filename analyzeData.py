file = open('testfile.txt', 'r')


topEvent = []
basicEvents = []

line = file.readline()
for time in line.split():
    topEvent.append(float(time))

lines = file.readlines()
for line in lines:
    basicEvent = []
    for time in line.split():
        basicEvent.append(float(time))
    basicEvents.append(basicEvent)

# Print time series
print(topEvent)
for basicEvent in basicEvents:
    print(basicEvent)


file.close()
