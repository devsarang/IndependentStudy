import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.signal as scpy
import numpy as np
import sys

manual_counter = 0
auto_counter = 0
window_size = 13

MAX_THRESHOLD = {'MCS0': 100, 'MCS1': 100, 'MCS2': 100, 'MCS3': 100, 'MCS4': 160, 'MCS5': 180, 'MCS6': 400, 'MCS7': 600,
             'MCSRA': 600}
MIN_THRESHOLD = {'MCS0': 10, 'MCS1': 10, 'MCS2': 10, 'MCS3': 10, 'MCS4': 16, 'MCS5': 18, 'MCS6': 40, 'MCS7': 60,
             'MCSRA': 60}

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
                    with open(readingDir + "/" + freq + "_" + mcs + "_" + reading + ".txt") as logFile:
                        lines = logFile.readlines()
                    print(logFile.name)
                except FileNotFoundError:
                    sys.exit("Fail")
                powerList = []
                medPowerList = []

                for line in lines:
                    current = float(line.split(',')[0])
                    voltage = float(line.split(',')[3])
                    power = current * voltage
                    powerList.append(power)
                medPowerList = scpy.medfilt(powerList, kernel_size=15)

                # with PdfPages(BASE_OP_DIR + "/" + freq + "/" + location + "/" + mcs + "/" + reading + "/" + "pt4_graph_pdf.pdf") as pdf:
                #     plt.plot(powerList, c='r', marker='o', markersize=0.0, linewidth=0.1)
                #     plt.title('Power')
                #     plt.axis([0, 85000, 0, 5000])
                #     pdf.savefig(dpi=200)
                #     plt.close()
                count = 0
                with open(BASE_OP_DIR + "/" + freq + "/" + location + "/" + mcs + "/" + reading + "/" + "power_reading.txt", "a") as text_file:
                    for power in powerList:
                        text_file.write(str(count) + ',' + str(power) + '\n')
                        count += 1
                for i in range(len(medPowerList) - 1, window_size, -1):
                        if medPowerList[i - window_size] - medPowerList[i] > MAX_THRESHOLD[mcs]:
                            endIndex = i
                        if()

                    tempendindex = endIndex
                    for i in range(0,window_size-1,1):
                        if medPowerList[tempendindex-i] - medPowerList[tempendindex-i-1] < MAX_THRESHOLD[mcs]:
                            endIndex -=1
                        # elif medPowerList[i] - medPowerList[i - 7] > THRESHOLD[mcs]:
                        #     startIndex = i - 7
                        startIndex = endIndex-100 if endIndex>100 else 0
                    else:
                            print('calculate manually')
                            print("start index" + str(startIndex) + " end index : " + str(endIndex))
                            manual_counter +=1
                    # if 90 < endIndex - startIndex < 110:
                    #     auto_counter += 1
                    # else:
                    #     manual_counter += 1;
                    #     print("start index" + str(startIndex) + " end index : " + str(endIndex))
                print("manual_count : " + str(manual_counter) + "auto counter: " + str(auto_counter));
