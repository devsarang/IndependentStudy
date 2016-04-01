import json
import os
from sys import platform as _platform

BASE_IP_DIR = ''
BASE_OP_DIR = ''
SLASH_SEPARATOR = ''
if _platform == "linux" or _platform == "linux2":
    BASE_IP_DIR = "/media/tejash/Media/CSEIndependentStudy/Results"
    BASE_OP_DIR = "/media/tejash/Media/CSEIndependentStudy/Results"
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_IP_DIR = "C:\PowerMeasurementStudy\Readings"
    BASE_OP_DIR = "C:\PowerMeasurementStudy\Results"
    SLASH_SEPARATOR = "\/"

print (
    'input directory: ' + BASE_IP_DIR + ' :::: output directory: ' + BASE_OP_DIR + ' ::: ' + 'Slash Separator:' + SLASH_SEPARATOR)
freqDictionary = {}
for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + SLASH_SEPARATOR + freq
    locationPowerDictionary = {}
    if os.path.isdir(freqDir):
        for location in os.listdir(freqDir):
            locationDir = freqDir + SLASH_SEPARATOR + location
            mcsValues = {}
            if os.path.isdir(locationDir):
                for mcs in os.listdir(locationDir):
                    try:
                        with open(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt') as logFile:
                            lines = logFile.readlines()
                            print(logFile.name)
                    except IOError:
                            print ('Error reading file:  '+BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt')
                            continue
                    try :
                        avg_power = lines[len(lines)-1].split(':')[1].strip()
                    except IndexError :
                            print ('Error in this file:  '+BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt')
                            continue
                    if not 'manually' in avg_power:
                        mcsValues[mcs] = float(avg_power)
                        locationPowerDictionary[location] = mcsValues
                    else :
                        mcsValues[mcs] = avg_power
                        locationPowerDictionary[location] = mcsValues
        freqDictionary [freq] = locationPowerDictionary
    with open(BASE_OP_DIR + SLASH_SEPARATOR  + "power_output.json", 'w') as fp:
        json.dump(freqDictionary, fp)


