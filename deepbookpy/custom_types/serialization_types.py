from canoser import Struct, ArrayT, Uint128

class VecSet(Struct):
    _fields = [
        ("constants", ArrayT(Uint128))  
    ]