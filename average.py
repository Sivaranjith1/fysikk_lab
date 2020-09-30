import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from os import listdir
from os.path import join




def loadFromFile(filename):
    dataFromFile = np.loadtxt(filename, skiprows=2)

    xfast = []
    yfast = []
    time = []
    
    xmin = dataFromFile[0][1]
    tmin = dataFromFile[0][0]
    for data in dataFromFile:
        time.append(data[0] - tmin)
        xfast.append(data[1]- xmin)
        yfast.append(data[2])

    time = np.array(time)
    xfast = np.array(xfast)
    yfast = np.array(yfast)

    return time, xfast, yfast;

'''
@returns a 2d array, 2d array, 2d array: y is the different files, x is the data
'''
def loadEveryFile(path):
    xfast = []
    yfast = []
    time = []

    for file in listdir(path):
        filename = join(path, file)
        t_temp, x_temp, y_temp = loadFromFile(filename)

        time.append(t_temp)
        xfast.append(x_temp)
        yfast.append(y_temp)

    time = np.array(time, dtype=object)
    xfast = np.array(xfast, dtype=object)
    yfast = np.array(yfast, dtype=object)

    return time, xfast, yfast
'''
@param data has to be a 2d array
@returns a np array with average of each measuring point
'''
def getAverage(data):
    data_average = []

    index = 0
    indexY = 0
    value = 0
    length = 0
    while(True):
        row = data[indexY]
        if (index < len(row)):
            value += row[index]
            length += 1

        indexY += 1

        if(indexY >= len(data)):
            index += 1
            data_average.append(value/length)
            length = 0
            indexY = 0
            value = 0

            if(index >= len(data[indexY])):
                break

    return data_average

def deviation(average):
    pass

'''
@returns an array of array. The first index is experiment, the last [velocity x direction, velocity y directio, speed]
'''
def speed(xfast, yfast, time):
    output = []
    for experiment in range(len(xfast)):
        vx = (xfast[experiment][-1] - xfast[experiment][-2]) / (time[experiment][-1] - time[experiment][-2])
        vy = (yfast[experiment][-1] - yfast[experiment][-2]) / (time[experiment][-1] - time[experiment][-2])
        output.append([vx, vy, np.sqrt(pow(vx,2) + pow(vy,2))]) 

    return np.array(output)

def speedDeviation(averageSpeed, speedArray):
    devi = 0

    for x in speedArray:
        devi += pow((x - averageSpeed), 2)

    devi = devi / len(speedArray - 2)

    return np.sqrt(devi)

def standardError(deviation, N):
    return deviation / np.sqrt(N)

if __name__ == '__main__':
    # print('time', time)
    # print('xfast', xfast)
    # print('yfast', yfast)

    time, xfast, yfast = loadEveryFile('Datafiles/')

    # averageY = getAverage(yfast)
    # averageX = getAverage(xfast)

    velocity = speed(xfast, yfast, time)
    speedArray = velocity[:,2]

    averageSpeed = np.average(speedArray)

    print('Average speed:', averageSpeed)

    deviation = speedDeviation(averageSpeed, speedArray)

    print('Standard deviation:', deviation)
    

    error = standardError(deviation, len(speedArray) - 1)
    print('Standard error: ', error)

    # plt.plot(averageX)
    # plt.show()