from canoser import Struct, ArrayT, Uint8, Uint64, Uint128, BoolT, BytesT, RustOptional
from pysui.sui.sui_types.bcs import Address

class VecSet(Struct):
    _fields = [
        ("constants", ArrayT(Uint128))  
    ]


class OrderDeepPrice(Struct):
    _fields = [
        ("asset_is_base", BoolT),
        ("deep_per_asset", Uint64),
    ]


class OptionID(RustOptional):
    _type = BytesT(32)


class Order(Struct):
    _fields = [
        ("balance_manager_id", Address),
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


class Balances(Struct):
    _fields = [
        ("base", Uint64),
        ("quote", Uint64),
        ("deep", Uint64)
    ]


class Account(Struct):
    _fields = [
        ("epoch", Uint64),
        ("open_orders", VecSet),
        ("taker_volume", Uint128),
        ("maker_volume", Uint128),
        ("active_stake", Uint64),
        ("inactive_stake", Uint64),
        ("created_proposal", BoolT),
        ("voted_proposal", OptionID),  # Optional ID
        ("unclaimed_rebates", Balances),
        ("settled_balances", Balances),
        ("owed_balances", Balances)
    ]


class RangeInput(Struct):
    _fields = [("range", ArrayT(Uint64))]    
