"""Helpers module with built-in features"""
import time
from deepbookpy.utils.constants import ORDER_DEFAULT_EXPIRATION_IN_MS


def parse_struct(response):
    """Parse pool data -> base_asset_type and quote_asset_type"""
    response = (
        response.replace("0xdee9::clob_v2::Pool<", "").replace(">", "").split(",")
    )
    return [el.strip() for el in response]


def order_24h_expiration():
    """Get +24 hour UNIX timestamp"""
    return int(time.time()) * 1000 + ORDER_DEFAULT_EXPIRATION_IN_MS
