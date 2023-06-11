"""Normalize Sui Objects"""

from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_types.address import SuiAddress


SUI_ADDRESS_LENGTH = 32


def normalize_sui_address(value: str, force_add_0x: bool = False) -> SuiAddress:
    """
    Make Sui address lower case.
    Prepend `0x` if the string does not start with `0x`.
    Add more zeros if the length of the address(excluding `0x`) is less than `SUI_ADDRESS_LENGTH
    
    WARNING: if the address value itself starts with contains doubled `0x`.
    the standardized rule is to treat the first `0x` not as part of the address.

    See more : https://github.com/MystenLabs/sui/blob/fdb569464ea61c672a6d81b5233d2531d59bcfcf/sdk/typescript/src/types/common.ts#L151

    """

    # Set address to lower case
    address = value.lower()

    if (force_add_0x != True and address.startswith('0x')):
        address = address[2:]
    
    # Fill necessarily `0` if `SUI_ADDRESS_LENGTH` < than required
    return f"0x{address.zfill(SUI_ADDRESS_LENGTH * 2)}"


def normalize_sui_object_id(value: str, force_add_0x: bool = False) -> ObjectID:
    """Normalize Sui Object Id"""
    
    return normalize_sui_address(value, force_add_0x)