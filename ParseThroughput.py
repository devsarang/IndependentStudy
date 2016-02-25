import linecache
import os

BASE_DIR = "C:\PowerMeasurementStudy\wifi"
T20MHZ_DIR = "20MHz_S4"
T40MHZ_DIR = "40MHz_S4"

#throughput for 20MHz
curDir = BASE_DIR + "\/" + T20MHZ_DIR
throughputMap = {}

for mcsDir in os.listdir(curDir):
    mcsDirs = curDir + "\/" + mcsDir
    tempMap = {}
    for locationDir in os.listdir(mcsDirs):
        locationDirs = mcsDirs + "\/" + locationDir
        throughputSum = 0
        numSample = 0
        for readNum in os.listdir(locationDirs):
            readNums = locationDirs + "\/" + readNum
            iperfFile = readNums+"\/"+"iperfoutput"
            if os.path.isfile(iperfFile):
                lineNum = 8   # for finding the bandwidth value
                #while len(linecache.getline(iperfFile, lineNum).split("/sec")) != 2:
                  #  lineNum += 1                                                          #increase linunumber if not found in the current line
                line = linecache.getline(iperfFile, lineNum)

                if line != '':
                    throughput = float(line.split("/sec")[0].split(" ")[-2])
                    if line.split("/sec")[0].split(" ")[-1] == 'Kbits':
                        throughputSum += throughput/1000
                        numSample += 1
                    elif line.split("/sec")[0].split(" ")[-1] == 'Mbits':
                        throughputSum += throughput
                        numSample += 1
                    else:
                        throughputSum += throughput
        if numSample < 5:
            print (mcsDir)
            print (locationDir)
            print (numSample)
            #tempMap[locationDir] = throughputSum/numSample
    throughputMap[mcsDir] = tempMap
#print throughputMap


