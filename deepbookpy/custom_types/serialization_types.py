from canoser import Struct, ArrayT, Uint8, Uint64, Uint128, BoolT, BytesT

class VecSet(Struct):
    _fields = [
        ("constants", ArrayT(Uint128))  
    ]

class ID(Struct):
    _fields = [
        ("bytes", BytesT(32)) 
    ]

class OrderDeepPrice(Struct):
    _fields = [
        ("asset_is_base", BoolT),
        ("deep_per_asset", Uint64),
    ]

class Order(Struct):
    _fields = [
        ("balance_manager_id", ID),
        ("order_id", Uint128),
        ("client_order_id", Uint64),
        ("quantity", Uint64),
        ("filled_quantity", Uint64),
        ("fee_is_deep", BoolT),
        ("order_deep_price", OrderDeepPrice),
        ("epoch", Uint64),
        ("status", Uint8),
        ("expire_timestamp", Uint64),
    ]
