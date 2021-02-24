from typing import BinaryIO
from CRData.storage import CRDataMap, CRDataType, CRDataValue, get_type_as_int
import struct

def convert_write_value(value: CRDataValue, key: str) -> bytearray:
    buffer = bytearray()

    buffer.append(get_type_as_int(value.type))

    buff = bytearray()
    buff.extend(key.encode('utf8'))
    buff.append(0x00)
    buffer.extend(buff)

    del buff

    if value.type == CRDataType.String:
        buff2 = bytearray()
        buff2.extend(value.get().encode('utf8'))
        buff2.append(0x00)
        buffer.extend(buff2)
        del buff2

    elif value.type == CRDataType.Boolean:
        if value.get() == True:
            buffer.append(1)
        else:
            buffer.append(0)

    elif value.type == CRDataType.Int:
        buffer.extend(value.get().to_bytes(length=8, byteorder='big'))
        
    elif value.type == CRDataType.Float:
        buffer.extend(struct.pack('>d', float(value.get())))

    elif value.type == CRDataType.Binary:
        buffer.extend(len(value.get()).to_bytes(length=8, byteorder='big'))
        buffer.extend(value.get())

    return buffer
        

def crdata_write(data: CRDataMap, io: BinaryIO) -> None:
    if not io.writable(): raise IOError("IO aren't writable")

    io.write(len(data).to_bytes(length=8, byteorder='big'))

    for key in data.keys():
        io.write(convert_write_value(value=data[key], key=key))