import json
from sys import platform as _platform
import matplotlib.pyplot as plt
import numpy as np



if _platform == "linux" or _platform == "linux2":
    THROUGHPUT_FILE = '/home/tejash/MSCS/CSIndependentStudy/Scripts/IndependentStudy/result/throughput.json'
    CPU_FILE = '/home/tejash/MSCS/CSIndependentStudy/Scripts/IndependentStudy/result/cpu_result.json'
    POWER_FILE = '/home/tejash/MSCS/CSIndependentStudy/Scripts/IndependentStudy/result/power_result.json'
elif _platform == "win32" or _platform == 'win64':
    THROUGHPUT_FILE = 'C:\PowerMeasurementStudy\Results\/throughput.json'
    CPU_FILE = 'C:\PowerMeasurementStudy\Results\cpu_result.json'
    POWER_FILE = 'C:\PowerMeasurementStudy\Results\power_result.json'

throughputFile = open(THROUGHPUT_FILE)
throughputStr = throughputFile.read()
throughputDict = json.loads(throughputStr)

cpuFile = open(CPU_FILE)
cpuStr = cpuFile.read()
cpuDict = json.loads(cpuStr)

powerFile = open(POWER_FILE)
powerStr = powerFile.read()
powerDict = json.loads(powerStr)

resultDict = {}

for freq in throughputDict:
    freqDict = {}
    raThroughputList = []
    raCPUList = []
    raWIFIList = []
    raEnergyPerBitList = []

    bestEfficientList = []
    bestEfficientValList = []
    bestEfficientCPUList = []
    bestEfficientWIFIList = []
    bestEfficientEnergyPerBitList = []

    highestThroughputList = []
    highestThroughputValList = []
    highestThroughputCPUList = []
    highestThroughputWIFIList = []
    highestThroughputEnergyPerBitList = []

    locationList = []

    for location in throughputDict[freq]:
        raThroughputList.append(throughputDict[freq][location]['MCSRA'])
        raCPUList.append(cpuDict[freq][location]['MCSRA'])
        raWIFIList.append(powerDict[freq][location]['MCSRA'] - cpuDict[freq][location]['MCSRA'])
        raEnergyPerBitList.append((powerDict[freq][location]['MCSRA'] - cpuDict[freq][location]['MCSRA'])/(throughputDict[freq][location]['MCSRA']*1000000))

        del(throughputDict[freq][location]['MCSRA'])

        highestThroughputMcs = max(throughputDict[freq][location].keys(), key=(lambda k: throughputDict[freq][location][k]))
        highestThroughputList.append(throughputDict[freq][location][highestThroughputMcs])
        highestThroughputValList.append(highestThroughputMcs)
        highestThroughputCPUList.append(cpuDict[freq][location][highestThroughputMcs])
        highestThroughputWIFIList.append(powerDict[freq][location][highestThroughputMcs]-cpuDict[freq][location][highestThroughputMcs])
        highestThroughputEnergyPerBitList.append((powerDict[freq][location][highestThroughputMcs] - cpuDict[freq][location][highestThroughputMcs])/(throughputDict[freq][location][highestThroughputMcs]*1000000))

        efficientMcs = min(throughputDict[freq][location].keys(), key=(lambda k: (powerDict[freq][location][k] - cpuDict[freq][location][k])/throughputDict[freq][location][k]))
        bestEfficientList.append(throughputDict[freq][location][efficientMcs])
        bestEfficientValList.append(efficientMcs)
        bestEfficientCPUList.append(cpuDict[freq][location][efficientMcs])
        bestEfficientWIFIList.append(powerDict[freq][location][efficientMcs]-cpuDict[freq][location][efficientMcs])
        bestEfficientEnergyPerBitList.append((powerDict[freq][location][efficientMcs] - cpuDict[freq][location][efficientMcs])/(throughputDict[freq][location][efficientMcs]*1000000))
        loc = 'L' + location[-2:]
        if loc[1] == 'n':
            loc = loc[0]+loc[2]
        locationList.append(loc)

    freqDict['RA_TH'] = raThroughputList

    freqDict['RA_CPU'] = raCPUList
    freqDict['RA_WIFI'] = raWIFIList
    freqDict['RA_EPB'] = raEnergyPerBitList

    freqDict['HS_TH'] = highestThroughputList
    freqDict['HS_CPU'] = highestThroughputCPUList
    freqDict['HS_WIFI'] = highestThroughputWIFIList
    freqDict['HS_EPB'] = highestThroughputEnergyPerBitList

    freqDict['EE_TH'] = bestEfficientList
    freqDict['EE_CPU'] = bestEfficientCPUList
    freqDict['EE_WIFI'] = bestEfficientWIFIList
    freqDict['EE_EPB'] = bestEfficientEnergyPerBitList

    freqDict['LOC'] = locationList
    resultDict[freq] = freqDict



GoodLinks = {'20MHz':['L1','L2','L8','L9','L19'],
             '40MHz':['L1','L2','L13','L14','L16','L18','L20','L21','L22']}
MediumLinks = {'20MHz':['L3','L10','L13','L15','L16','L17','L18','L20','L23','L24'],
             '40MHz':['L3','L5','L15','L17','L23','L24','L25','L26']}
BadLinks = {'20MHz':['L4','L5','L11','L12','L22','L25'],
             '40MHz':['L6','L7','L9','L10']}

################################    FOR 20 MHZ ####################################################

width = 0.25
ind = np.arange(len(resultDict['20MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['20MHz']['RA_TH'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['20MHz']['HS_TH'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['20MHz']['EE_TH'], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput All Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

width = 0.25
ind = np.arange(len(resultDict['20MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['20MHz']['RA_EPB'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['20MHz']['HS_EPB'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['20MHz']['EE_EPB'], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit All Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

width = 0.25
ind = np.arange(len(resultDict['20MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['20MHz']['RA_WIFI'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['20MHz']['HS_WIFI'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['20MHz']['EE_WIFI'], width, color='plum')
rects4 = ax.bar(ind, resultDict['20MHz']['RA_CPU'], width, color='grey',bottom = resultDict['20MHz']['RA_WIFI'])
rects5 = ax.bar(ind + width, resultDict['20MHz']['HS_CPU'], width, color='orange', bottom = resultDict['20MHz']['HS_WIFI'])
rects6 = ax.bar(ind + 2 * width, resultDict['20MHz']['EE_CPU'], width, color='c', bottom = resultDict['20MHz']['EE_WIFI'])
ax.set_ylabel('Power')
ax.set_xlabel('Locations')
ax.set_title('CPU and WiFi Usage 20 MHz All Links')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0],rects4[0], rects5[0], rects6[0]), ('RA WIFI', 'HSM WIFI', 'BEE WIFI','RA CPU','HSM CPU','BEE CPU'))
plt.show()


index = [resultDict['20MHz']['LOC'].index(i) for i in GoodLinks['20MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Good Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

index = [resultDict['20MHz']['LOC'].index(i) for i in MediumLinks['20MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Medium Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

index = [resultDict['20MHz']['LOC'].index(i) for i in BadLinks['20MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Bad Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['20MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()


index = [resultDict['20MHz']['LOC'].index(i) for i in GoodLinks['20MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Good Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['20MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

index = [resultDict['20MHz']['LOC'].index(i) for i in MediumLinks['20MHz']]
print([resultDict['20MHz']['EE_EPB'][i] for i in index])
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Medium Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['20MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

index = [resultDict['20MHz']['LOC'].index(i) for i in BadLinks['20MHz']]
print([resultDict['20MHz']['EE_EPB'][i] for i in index])
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['20MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['20MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['20MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Bad Links 20 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['20MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

################################    FOR 40 MHZ ####################################################

width = 0.25
ind = np.arange(len(resultDict['40MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['40MHz']['RA_TH'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['40MHz']['HS_TH'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['40MHz']['EE_TH'], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput All Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['40MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

width = 0.25
ind = np.arange(len(resultDict['40MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['40MHz']['RA_EPB'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['40MHz']['HS_EPB'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['40MHz']['EE_EPB'], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit All Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['40MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

width = 0.25
ind = np.arange(len(resultDict['40MHz']['LOC']))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, resultDict['40MHz']['RA_WIFI'], width, color='pink')
rects2 = ax.bar(ind + width, resultDict['40MHz']['HS_WIFI'], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, resultDict['40MHz']['EE_WIFI'], width, color='plum')
rects4 = ax.bar(ind, resultDict['40MHz']['RA_CPU'], width, color='grey',bottom = resultDict['40MHz']['RA_WIFI'])
rects5 = ax.bar(ind + width, resultDict['40MHz']['HS_CPU'], width, color='orange', bottom = resultDict['40MHz']['HS_WIFI'])
rects6 = ax.bar(ind + 2 * width, resultDict['40MHz']['EE_CPU'], width, color='c', bottom = resultDict['40MHz']['EE_WIFI'])
ax.set_ylabel('Power')
ax.set_xlabel('Locations')
ax.set_title('CPU and WiFi Usage 40 MHz All Links')
ax.set_xticks(ind + width)
ax.set_xticklabels(resultDict['40MHz']['LOC'])
ax.legend((rects1[0], rects2[0], rects3[0],rects4[0], rects5[0], rects6[0]), ('RA WIFI', 'HSM WIFI', 'BEE WIFI','RA CPU','HSM CPU','BEE CPU'))
plt.show()


index = [resultDict['40MHz']['LOC'].index(i) for i in GoodLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Good Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

index = [resultDict['40MHz']['LOC'].index(i) for i in MediumLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Medium Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()

index = [resultDict['40MHz']['LOC'].index(i) for i in BadLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_TH'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_TH'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_TH'][i] for i in index], width, color='plum')
ax.set_ylabel('Throughput Mbps')
ax.set_xlabel('Locations')
ax.set_title('Throughput Bad Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM','BEE'))
plt.show()


index = [resultDict['40MHz']['LOC'].index(i) for i in GoodLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Good Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

index = [resultDict['40MHz']['LOC'].index(i) for i in MediumLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Medium Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()

index = [resultDict['40MHz']['LOC'].index(i) for i in BadLinks['40MHz']]
width = 0.25
ind = np.arange(len(index))
fig, ax = plt.subplots()
rects1 = ax.bar(ind, [resultDict['40MHz']['RA_EPB'][i] for i in index], width, color='pink')
rects2 = ax.bar(ind + width, [resultDict['40MHz']['HS_EPB'][i] for i in index], width, color='tomato')
rects3 = ax.bar(ind + 2 * width, [resultDict['40MHz']['EE_EPB'][i] for i in index], width, color='plum')
ax.set_ylabel('Energy Per bit')
ax.set_xlabel('Locations')
ax.set_title('Energy Per Bit Bad Links 40 MHz')
ax.set_xticks(ind + width)
ax.set_xticklabels([resultDict['40MHz']['LOC'][i] for i in index])
ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
plt.show()
