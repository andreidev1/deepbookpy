from pysui.sui.sui_config import SuiConfig
from pysui.sui.sui_clients.sync_client import SuiClient

def cfg_user():
    """."""
    cfg = SuiConfig.user_config(
        # Required
        rpc_url="https://fullnode.devnet.sui.io:443",
        # Required. First entry becomes the 'active-address'
        # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
        prv_keys=["AOM6UAQrFe7r9nNDGRlWwj1o7m1cGK6mDZ3efRJJmvcG"],
        # Optional, only needed for subscribing
        ws_url="wss://fullnode.devnet.sui.io:443",
    )
    return cfg

client = SuiClient(cfg_user())



