import csv
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import os

count = 1000
step = 6

flist = os.listdir("./ddarmist_data")
placeData = {}
for idx, fname in enumerate(flist):
    if (idx % step == 0):
        with open('./ddarmist_data/' + fname, encoding="utf8") as csv_file:
            print(fname)
            csv_data = csv.DictReader(csv_file)
            for i in csv_data:
                stationId = i.get("stationId")
                if placeData.get(stationId) == None:
                    placeData[stationId] = []
                i["fname"] = fname
                placeData[stationId].append(i)
    if idx >= count*step:
        break

for i in placeData.keys():
    tmp = [{"parkingBikeTotCnt":0} for i in range(count)]
    for j in range(len(placeData[i])-1):
        tmp[j] = placeData[i][j]
    placeData[i] = tmp

dataX = [float(placeData[name][0]["stationLongitude"]) for name in placeData.keys()]
dataY = [float(placeData[name][0]["stationLatitude"]) for name in placeData.keys()]
dataSize = [int(placeData[name][0]["parkingBikeTotCnt"]) ** 2 for name in placeData.keys()]

dataX = list(filter(lambda x: x != 0, dataX))
dataY = list(filter(lambda x: x != 0, dataY))
dataColors = np.random.rand(len(dataX))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


def animate(i):
    dataSize = [int(placeData[name][i]["parkingBikeTotCnt"]) ** 2 for name in placeData.keys()]
    nowTime = dict(placeData[list(placeData.keys())[0]][i])["fname"]
    print(i)

    ax.clear()
    ax.set(xlim=[126.78, 127.20], ylim=[37.42, 37.70], title=nowTime)
    ax.scatter(dataX, dataY, s=dataSize, c=dataColors, alpha=0.3)


anim = animation.FuncAnimation(fig, animate, interval=10)
anim.save('ddarmist.gif', writer='imagemagick', fps=30, dpi=100)
plt.show()
