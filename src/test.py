from CRData import *

obj = CRDataMap()

obj["BinaryV"] = CRDataValue(bytearray([0, 24, 243, 140, 80]))
obj["IntV"] = CRDataValue(1)
obj["FloatV"] = CRDataValue(1.5)
obj["BoolV"] = CRDataValue(True)
obj["StringV"] = CRDataValue("A string test")

"""file = open(file='./test.crdata', mode='bw')

crdata_write(obj, file)

file.close()"""

file = open(file='./test.crdata', mode='br')

obj2 = crdata_read(file)

file.close()

if obj.compare(obj2): print("Objects are equal")
else: print("Objects aren't equal")