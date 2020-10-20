import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from os import listdir
from os.path import join
from scipy.interpolate import CubicSpline

ystart = 25.5e-2

def getNumericForm():
    h = 200
    xfast=np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])
    xfast = xfast/1000
    yfast = np.asarray([0.255,0.183,0.189,0.188,0.129,0.091,0.151,0.171])
    cs = CubicSpline(xfast, yfast, bc_type='natural')
    xmin = xfast[0]
    xmax = xfast[-1]
    dx = 0.001
    x = np.arange(xmin, xmax, dx)
    y = cs(x)
    return x,y

def getNumericTime():
    t = np.loadtxt('time.txt')
    return t

def loadFromFile(filename):
    dataFromFile = np.loadtxt(filename, skiprows=2)

    xfast = []
    yfast = []
    time = []
    
    xmin = dataFromFile[0][1]
    tmin = dataFromFile[0][0]
    ymin = dataFromFile[0][2]
    for data in dataFromFile:
        time.append(data[0] - tmin)
        xfast.append(data[1]- xmin)
        yfast.append(data[2] - ymin + ystart)

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

    devi = devi / (len(speedArray)-2)

    return np.sqrt(devi)

def standardError(deviation, N):
    return deviation / np.sqrt(N)

if __name__ == '__main__':
    # print('time', time)
    # print('xfast', xfast)
    # print('yfast', yfast)

    time, xfast, yfast = loadEveryFile('Datafiles/')

    averageY = getAverage(yfast)
    averageX = getAverage(xfast)

    for i in range(len(xfast)):
        xNumeric, yNumeric = getNumericForm()

        mal = plt.figure('Maaling '+str(i+1), figsize=(12,3))
        plt.title('Baneformen av måling '+ str(i+1))
        plt.ylim(0,yNumeric[-1]*1.5)
        plt.plot(xfast[i],yfast[i], label='Eksperimentell bane')
        plt.plot( xfast[i],yfast[i], '*', label='Målepunkter')
        plt.plot(xNumeric, yNumeric, 'r', linestyle='dashed', label='Numerisk bane')
        plt.xlabel('x ($m$)', fontsize=20)
        plt.ylabel('y ($m$)', fontsize=20)
        plt.legend(loc="lower center")
    
        plt.grid()
        mal.savefig("img/mal"+str(i+1)+".svg", bbox_inches='tight')

    #x(t)
    xNumeric, _ = getNumericForm()
    tNumeric = getNumericTime()
    graf_x_t = plt.figure('x(t)',figsize=(12,3))
    plt.grid()
    plt.title('X-posisjon over tid for måling ' + str(4+1))
    plt.xlabel('Tid ($s$)')
    plt.ylabel('X posisjon ($m$)')
    plt.plot(time[4], xfast[4])
    plt.plot(time[4], xfast[4], '*')
    plt.plot(tNumeric,xNumeric)
    graf_x_t.savefig("img/x_av_t_maaling_"+str(4+1)+".svg", bbox_inches='tight')

    velocity = speed(xfast, yfast, time)
    speedArray = velocity[:,2]

    averageSpeed = np.average(speedArray)

    print('Average speed:', averageSpeed)

    deviation = speedDeviation(averageSpeed, speedArray)

    print('Standard deviation:', deviation)
    

    error = standardError(deviation, len(speedArray) - 1)
    print('Standard error: ', error)

    print('speed array', speedArray)


    bane_avg = plt.figure('bane average',figsize=(12,3))
    plt.title('Gjennomsnittlig baneform fra målinger')
    plt.plot(averageX, averageY, averageX, averageY, '*')
    plt.xlabel('x_avg ($m$)', fontsize=20)
    plt.ylabel('y_avg ($m$)', fontsize=20)
    plt.grid()
    bane_avg.savefig("img/bane_avg.svg", bbox_inches='tight')


    speedIndex = [i+1 for i in range(0, len(speedArray))]
    speed_plot = plt.figure('speed_plot',figsize=(12,3))
    plt.title('Slutthastigheten til målingene')
    plt.plot(speedIndex, speedArray, '*', label="Slutthastighet")
    plt.xlabel('Måling', fontsize=20)
    plt.ylabel('Slutthastighet ($\dfrac{m}{s}$)', fontsize=20)
    plt.hlines(averageSpeed, speedIndex[0], len(speedArray), color='r',label='Gjennomsnitt', linestyles='dashed')
    plt.legend(loc="lower center")

    speed_plot.savefig("img/slutthastighet.svg", bbox_inches='tight')

    plt.show()