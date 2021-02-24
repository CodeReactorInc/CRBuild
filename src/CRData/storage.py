from enum import Enum
from io import SEEK_CUR

class CRDataType(Enum):
    Binary = 0x00
    String = 0x01
    Int = 0x02
    Float = 0x03
    Boolean = 0x04

def get_type_as_int(value: CRDataType) -> int:
    if value == CRDataType.Binary:
        return 0x00
    elif value == CRDataType.String:
        return 0x01
    elif value == CRDataType.Boolean:
        return 0x04
    elif value == CRDataType.Int:
        return 0x02
    elif value == CRDataType.Float:
        return 0x03
    else:
        raise TypeError("Type from value aren't supported")

def get_type(value) -> CRDataType:
    if isinstance(value, bytearray):
        return CRDataType.Binary
    elif isinstance(value, str):
        return CRDataType.String
    elif isinstance(value, bool):
        return CRDataType.Boolean
    elif isinstance(value, int):
        return CRDataType.Int
    elif isinstance(value, float):
        return CRDataType.Float
    else:
        raise TypeError("Type from value aren't supported")

class CRDataValue:
    def __init__(self, value) -> None:
        self.__value__ = value
        self.type: CRDataType = get_type(value)

    def set(self, value) -> None:
        self.__value__ = value
        self.type: CRDataType = get_type(value)

    def get(self):
        return self.__value__

class CRDataMap(dict[str, CRDataValue]):
    def compare(self, dic: 'CRDataMap'):
        for key in self.keys():
            if self[key].get() != dic[key].get():
                return False

        for key in dic.keys():
            if self[key].get() != dic[key].get():
                return False
        
        return True

