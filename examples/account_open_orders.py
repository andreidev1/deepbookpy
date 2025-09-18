import os
import sys
import pathlib

from dotenv import load_dotenv
from pysui import SyncClient, SuiConfig
from pysui.sui.sui_txn import SyncTransaction

PROJECT_DIR = pathlib.Path(os.path.dirname(__file__))
PARENT = PROJECT_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(os.path.join(PARENT, "deepbookpy")))

from deepbookpy.deepbook_client import DeepBookClient
from deepbookpy.utils.config import DeepBookConfig

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")

if __name__ == "__main__":

    # Init pysui config
    def cfg_user():
        cfg = SuiConfig.user_config(
            # Required
            rpc_url="https://fullnode.mainnet.sui.io:443/",
            # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
            prv_keys=[private_key],
            # Needed for subscribing
            ws_url="wss://fullnode.mainnet.sui.io:443/",
        )
        return cfg

    cfg = cfg_user()
    client = SyncClient(cfg)
    current_sui_address = cfg.addresses[0]
    txn = SyncTransaction(client=client)

    # Balance Manager
    balance_manager = {
        "MANAGER_1" : {
            "address" : "0x344c2734b1d211bd15212bfb7847c66a3b18803f3f5ab00f5ff6f87b6fe6d27d",
            "trade_cap" : ""
        }
    }

    # Init deepbook client
    deepbook_client = DeepBookClient(client, current_sui_address, "mainnet", balance_manager)
    
    # Init deepbook config
    deepbook_config = DeepBookConfig("mainnet", "0x0", None, balance_manager)

    pools = ['SUI_USDC', 'DEEP_SUI', 'DEEP_USDC', 'WUSDT_USDC', 'WUSDC_USDC', 'BETH_USDC']

    manager = "MANAGER_1"

    for pool in pools:
        print(pool)
        result = deepbook_client.account_open_orders(pool, manager)
        print(result)


