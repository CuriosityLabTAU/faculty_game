import json
file_name = 'C:/Users/LENOVO-P50/AppData/Roaming/curiosity/2018_01_07_16_58_50_969000.log'

mydict = json.load(open(file_name, 'r'))
for key in sorted(mydict.iterkeys()):
    print "%s: %s" % (key, mydict[key])