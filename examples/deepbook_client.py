from pysui import SyncClient, SuiConfig
from pysui.sui.sui_txn import SyncTransaction
import sys, os, pathlib

PROJECT_DIR = pathlib.Path(os.path.dirname(__file__))
PARENT = PROJECT_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(os.path.join(PARENT, "deepbookpy")))


from deepbookpy.deepbook_client import DeepBookClient

# git clone https://github.com/andreidev1/deepbookpy
# cd deepbookpy 
# python3 -m venv env && source ./env/bin/activate
# python3 examples/deepbook_client.py
if __name__ == "__main__":

    def cfg_user():

        cfg = SuiConfig.user_config(
            # Required
            rpc_url="https://fullnode.mainnet.sui.io:443/",
            # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
            prv_keys=["AIUPxQveY18QggDDdTO0D0OD6PNVvtet50072d1grIyl"],
            # Needed for subscribing
            ws_url="wss://fullnode.mainnet.sui.io:443/",
        )
        return cfg

    cfg = cfg_user()
    client = SyncClient(cfg)
    current_sui_address = cfg.addresses[0]
    txn = SyncTransaction(client=client)

    deepbook_client = DeepBookClient(client, current_sui_address, "mainnet")
    print(deepbook_client.whitelisted("SUI_USDC", txn))