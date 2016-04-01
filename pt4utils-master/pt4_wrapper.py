import os
import sys
from pt4_filereader import Pt4FileReader

BASE_IP_DIR = "/media/tejash/Tejash/MSCS/CSEIndependentStudy/PowerMeasurementStudy/Readings"

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
                    try:
                        with open(readingDir + "/" + mcs.lower() + "_" + reading + ".pt4") as logFile:
                            lines = logFile.readlines()
                        print(logFile.name)
                    except :
                        print('Error reading file: '+readingDir + "/" + freq + "_" + mcs + "_" + reading + ".pt4")
                        print('Error reading file: '+readingDir + "/" + mcs.lower() + "_" + reading + ".pt4" )

                        # continue
                if not os.path.exists(os.path.splitext(logFile.name)[0] + ".txt"):
                    file = open(os.path.splitext(logFile.name)[0] + ".txt", 'w')
                    for smpl in Pt4FileReader.readAsVector(logFile.name):
                        file.write(str(smpl[2]) + '\n')
                    # print(smpl[2])