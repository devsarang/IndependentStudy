
filename = "/media/tejash/Tejash/MSCS/CSEIndependentStudy/PowerMeasurementStudy/Readings/40MHz/Location17/MCSRA/2/40MHz_MCSRA_2.txt"
startIndex = 29000
endIndex = 79000
startBaseIndex = 0
endBaseIndex = 8000

avgBasePower =0
avgPower = 0
powerList = []
basepowerlist = []
with open(filename) as logFile:
    lines = logFile.readlines()

for count in range(startIndex,endIndex):
    current = float(lines[count].split(',')[0])
    # print current
    voltage = float(lines[count].split(',')[3])
    # print voltage
    power = current * voltage
    powerList.append(power)
print (startIndex)
print (endIndex)


avgPower = sum(powerList) / (endIndex - startIndex)
print("Avg power: "+ str(avgPower))


for count in range(startBaseIndex,endBaseIndex):
    current = float(lines[count].split(',')[0])
    voltage = float(lines[count].split(',')[3])
    basepower = current * voltage
    basepowerlist.append(basepower)

avgBasePower = sum(basepowerlist) / (endBaseIndex - startBaseIndex)
print("avg base power: " +str(avgBasePower))
print("final power : "+str(avgPower-avgBasePower))