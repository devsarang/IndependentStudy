import linecache
import os
import json


BASE_IP_DIR = "C:\PowerMeasurementStudy\Readings"
BASE_OP_DIR = "C:\PowerMeasurementStudy\Results"

resultDict = {}
#BASE_IP_DIR = "C:\Test\Readings"
#BASE_OP_DIR = "C:\Test\Results"

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + "\/" + freq
    freqDict = {}
    for location in os.listdir(freqDir):
        locationDict = {}
        locationDir = freqDir + "\/" + location
        for mcs in os.listdir(locationDir):
            mcsDir = locationDir + "\/" + mcs
            throughputSum = 0
            numSample = 0
            for reading in os.listdir(mcsDir):
                readingDir = mcsDir + "\/" + reading
                iperfFile = readingDir + "\/" + "iperfoutput"
                if os.path.isfile(iperfFile):
                    lineNum = 8   # for finding the bandwidth value
                    while len(linecache.getline(iperfFile, lineNum).split("/sec")) != 2:
                        lineNum += 1                                                          #increase linunumber if not found in the current line
                    line = linecache.getline(iperfFile, lineNum)
                    if line != '':
                        throughput = float(line.split("/sec")[0].split(" ")[-2])
                        if line.split("/sec")[0].split(" ")[-1] == 'Kbits':
                            throughputSum += throughput/1000
                            numSample += 1
                        elif line.split("/sec")[0].split(" ")[-1] == 'Mbits':
                            throughputSum += throughput
                            numSample += 1
            locationDict[mcs] = throughputSum/numSample
        freqDict[location] = locationDict
    resultDict[freq] = freqDict

with open(BASE_OP_DIR + '\/' + 'throughput.json', 'w') as fpJson:
    json.dump(resultDict, fpJson)
with open(BASE_OP_DIR + '\/' + 'throughput.txt', 'w') as fpText:
    for freq in resultDict:
        fpText.write('\t' + freq + '\n\n')
        for location in resultDict[freq]:
            fpText.write(location + '\t')
            for i in range(8):
                mcs = 'MCS'+ str(i)
                if mcs in resultDict[freq][location].keys():
                    fpText.write(str(resultDict[freq][location][mcs]) + '\t')
            fpText.write(str(resultDict[freq][location]['MCSRA']) + '\t')
            fpText.write('\n')
        fpText.write('\n\n')

