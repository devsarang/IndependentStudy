import os
import sys
from pt4_filereader import Pt4FileReader

BASE_IP_DIR = "/home/tejash/MSCS/CSIndependentStudy/TestReadings"
BASE_OP_DIR = "/home/tejash/MSCS/CSIndependentStudy/Results"

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + "/" + freq
    for location in os.listdir(freqDir):
        locationDir = freqDir + "/" + location
        for mcs in os.listdir(locationDir):
            mcsDir = locationDir + "/" + mcs
            for reading in os.listdir(mcsDir):
                readingDir = mcsDir + "/" + reading
                # print (readingDir + "/" + "log_" + freq + "_" + mcs + "_" + reading)
                try:
                    with open(readingDir + "/" + freq + "_" + mcs + "_" + reading + ".pt4") as logFile:
                        lines = logFile.readlines()
                    print(logFile.name)
                except IOError:
                    continue

                for smpl in Pt4FileReader.readAsVector(logFile.name):
                    with open(os.path.splitext(logFile.name)[0]+".txt", 'a') as the_file:
                        the_file.write(str(smpl[2])+'\n')
                    print(smpl[2])
                    print(logFile.name)
