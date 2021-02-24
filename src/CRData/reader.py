import struct
from typing import BinaryIO
from CRData.storage import CRDataMap, CRDataValue

class CRDataError(Exception):
    pass

def crdata_read(io: BinaryIO) -> CRDataMap:
    if not io.readable(): raise IOError("IO aren't readable")

    obj = CRDataMap()
    
    io.seek(0, 2)
    file_length = io.tell()
    io.seek(0, 0)
    obj_length = int.from_bytes(io.read(8), byteorder='big')

    actual_index = 0
    processed_obj = 0

    while actual_index < file_length:
        if processed_obj >= obj_length: raise CRDataError("Processed objects has passed the length declared")

        if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
        obj_type = io.read(1)

        if obj_type == bytes([0]):
            buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            byte = io.read(1)

            while byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object name")
                buffer.extend(byte)
                byte = io.read(1)

            obj_key = buffer.decode('utf8')
            
            obj_bin_length = int.from_bytes(io.read(8), byteorder='big')

            obj[obj_key] = CRDataValue(bytearray(io.read(obj_bin_length)))
            
        elif obj_type == bytes([1]):
            buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            byte = io.read(1)

            while byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object name")
                buffer.extend(byte)
                byte = io.read(1)

            obj_key = buffer.decode('utf8')

            obj_buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            obj_byte = io.read(1)

            while obj_byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object string")
                obj_buffer.extend(obj_byte)
                obj_byte = io.read(1)

            obj[obj_key] = CRDataValue(obj_buffer.decode('utf8'))

        elif obj_type == bytes([2]):
            buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            byte = io.read(1)

            while byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object name")
                buffer.extend(byte)
                byte = io.read(1)

            obj_key = buffer.decode('utf8')

            obj[obj_key] = CRDataValue(int.from_bytes(io.read(8), byteorder='big'))
        elif obj_type == bytes([3]):
            buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            byte = io.read(1)

            while byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object name")
                buffer.extend(byte)
                byte = io.read(1)

            obj_key = buffer.decode('utf8')

            if (io.tell() + 8 >= file_length): raise CRDataError("Corrupted CRData file")
            obj[obj_key] = CRDataValue(struct.unpack('>d', io.read(8))[0])

        elif obj_type == bytes([4]):
            buffer = bytearray()
            
            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            byte = io.read(1)

            while byte != bytes([0]):
                if io.tell() == file_length - 1: raise CRDataError("Cannot parse object name")
                buffer.extend(byte)
                byte = io.read(1)

            obj_key = buffer.decode('utf8')

            if (io.tell() + 1 >= file_length): raise CRDataError("Corrupted CRData file")
            if io.read(1) == bytes([0]):
                obj[obj_key] = CRDataValue(False)
            else:
                obj[obj_key] = CRDataValue(True)
            
        else: raise CRDataError("Invalid type on CRData file")

        actual_index = io.tell()
        processed_obj += 1

    return obj
