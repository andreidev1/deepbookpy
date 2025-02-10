from pysui import SyncClient, SuiConfig
from pysui.sui.sui_txn import SyncTransaction
import sys, os, pathlib

PROJECT_DIR = pathlib.Path(os.path.dirname(__file__))
PARENT = PROJECT_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(os.path.join(PARENT, "deepbookpy")))


from deepbookpy.deepbook_client import DeepBookClient
from deepbookpy.utils.config import DeepBookConfig

# git clone https://github.com/andreidev1/deepbookpy
# cd deepbookpy 
# python3 -m venv env && source ./env/bin/activate
# python3 examples/deepbook_client.py
if __name__ == "__main__":

    # Init pysui config
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


    # call get_balance_manager method from deepbook configuration
    # print(deepbook_config.get_balance_manager("MANAGER_1"))

    # call check_manager_balance method from deepbook client
    #print(deepbook_client.check_manager_balance("MANAGER_1", "SUI"))

    # call whitelisted method from deepbook_client
    #print(deepbook_client.whitelisted("SUI_USDC"))

    # call get_quote_quantity method from deepbook_client
    #print(deepbook_client.get_quote_quantity_out("SUI_USDC", 1))

    # call get_base_quantity_out method from deepbook_client
    #print(deepbook_client.get_base_quantity_out("SUI_USDC", 1))

    # call get_quantity_out method from deepbook_client
    #print(deepbook_client.get_quantity_out("SUI_USDC", 1, 5))

    # call account_open_orders method from deepbook_client
    #print(deepbook_client.account_open_orders("SUI_USDC", "MANAGER_1"))

    # call get_order method from deepbook_client
    #print(deepbook_client.get_order("SUI_USDC", deepbook_client.account_open_orders("SUI_USDC", "MANAGER_1")[0]))

    # call get_order_norrmalized method from deepbook_client
    #order_id = deepbook_client.account_open_orders("SUI_USDC", "MANAGER_1")[0]
    #print(deepbook_client.get_order_normalized("SUI_USDC", order_id))

    # call get_orders method from deepbook_client
    #print(deepbook_client.get_orders("SUI_USDC", [62589821088840582335273900, 170141183460533205040134928440896149600, 63198563643272997538601259, 170141183460533463294551960374618773601, 170141183460534035143618245370718869602, 63438371316231221709609250, 170141183460532983679206043926276757613, 63715072477336864983849248]))

    # call get_level2_range method from deepbook_client
    #print(deepbook_client.get_level2_range("SUI_USDC", 0.1, 100, True))

    # call vault_balances method from deepbook_client
    #print(deepbook_client.vault_balances("SUI_USDC"))

    # call get_pool_id_by_assets method from deepbook_client
    #print(deepbook_client.get_pool_id_by_assets("0xdeeb7a4662eec9f2f3def03fb937a663dddaa2e215b8078a284d026b7946c270::deep::DEEP", "0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI"))

    # call mid_price method from deepbook_client
    #print(deepbook_client.mid_price("SUI_USDC"))

    # call pool_trade_params method from deepbook_client
    #print(deepbook_client.pool_trade_params("SUI_USDC"))

    # call pool_book_params method from deepbook_client
    #print(deepbook_client.pool_book_params("SUI_USDC"))

    # call account method from deepbook_client
    #print(deepbook_client.account("SUI_USDC", "MANAGER_1"))

    # call locked_balance method from deepbook_client
    #print(deepbook_client.locked_balance("DEEP_SUI", "MANAGER_1"))

    # call get_pool_deep_price method from deepbook_client
    #print(deepbook_client.get_pool_deep_price("SUI_USDC"))