import os
import dpkt
import binascii
import json

BASE_IP_DIR = "C:\PowerMeasurementStudy\Readings"
BASE_OP_DIR = "C:\PowerMeasurementStudy\Results"

resultDict = {}

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + "\/" + freq
    locationDict = {}
    for location in os.listdir(freqDir):
        locationList = [0, 0, 0, 0, 0, 0, 0, 0]
        locationDir = freqDir + "\/" + location + "\/" + 'MCSRA'
        for reading in os.listdir(locationDir):
            readingDir = locationDir + "\/" + reading
            wiresharkFile = readingDir + "\/" + "wireshark.cap"
            f = open(wiresharkFile,'rb')
            print (wiresharkFile)
            pcap = dpkt.pcap.Reader(f)
            dl=pcap.datalink()
            if pcap.datalink() == 127:  # Check if RadioTap
                for timestamp, rawdata in pcap:
                    tap = dpkt.radiotap.Radiotap(rawdata)
                    mcs=binascii.hexlify(rawdata[28:29])
                    mcs=int(mcs,16)
                    locationList[mcs] += 1
        locationDict[location] = [i/5 for i in locationList]
    resultDict[freq] = locationDict
print (resultDict)
with open(BASE_OP_DIR + '\/' + 'ra_mcs.json', 'w') as fpJson:
    json.dump(resultDict, fpJson)