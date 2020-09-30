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

    time = np.array(time)
    xfast = np.array(xfast)
    yfast = np.array(yfast)

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
                break;

    return data_average

def deviation(average):
    pass

if __name__ == '__main__':
    # print('time', time)
    # print('xfast', xfast)
    # print('yfast', yfast)

    time, xfast, yfast = loadEveryFile('Datafiles/')

    print(yfast)

    averageY = getAverage(yfast)
    averageX = getAverage(xfast)
    

    plt.plot(averageX)
    plt.show()