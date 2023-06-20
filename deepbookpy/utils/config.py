from pysui.sui.sui_config import SuiConfig
from pysui.sui.sui_clients.sync_client import SuiClient


def cfg_user():
    """Config user"""
    cfg = SuiConfig.user_config(
        # Required
        rpc_url="https://fullnode.testnet.sui.io:443/",
        # Required. First entry becomes the 'active-address'
        # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
        prv_keys=["AIUPxQveY18QxhDDdTO0D0OD6PNVvtet50068d1grIyl"],
        # needed for subscribing
        ws_url="wss://fullnode.testnet.sui.io:443/",
    )
    return cfg

cfg = cfg_user()
client = SuiClient(cfg)
