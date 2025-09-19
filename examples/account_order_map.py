import os
import sys
import pathlib
import json
from collections import defaultdict
import time

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

    pool_price_multiplier = {
        "SUI_USDC": 1000,
        "DEEP_SUI": 0.001,
        "DEEP_USDC": 1,
        "WUSDT_USDC": 1,
        "WUSDC_USDC": 1,
        "BETH_USDC": 1
    }


    # Safe call - sometimes it might throw index out of range
    def safe_get_order(pool, order_id, retries=3, delay=0.5):
        for attempt in range(retries):
            try:
                order = deepbook_client.get_order_normalized(pool, order_id)
                if order:
                    return order
            except (IndexError, KeyError, TypeError) as e:
                # Could log the error here if needed
                time.sleep(delay)
        print(f"Failed to fetch order {order_id} in pool {pool} after {retries} attempts")
        return None

    # Main loop over pools
    for pool in pools:
        multiplier = pool_price_multiplier.get(pool, 1)
        orders = deepbook_client.account_open_orders(pool, manager)
        bid_orders_map = defaultdict(float)
        ask_orders_map = defaultdict(float)

        for order_id in orders:
            order = safe_get_order(pool, order_id)
            if not order:
                continue

            # If order is a JSON string, parse it
            if isinstance(order, str):
                try:
                    order = json.loads(order)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON for order {order_id} in pool {pool}")
                    continue

            try:
                remaining_quantity = float(order["quantity"]) - float(order["filled_quantity"])
            except (KeyError, TypeError, ValueError):
                print(f"Skipping order {order_id} in pool {pool} due to missing quantity fields")
                continue

            order_map = bid_orders_map if order.get("is_bid") else ask_orders_map

            try:
                order_price = round(float(order["normalized_price"]) * multiplier, 5)
            except (KeyError, TypeError, ValueError):
                print(f"Skipping order {order_id} in pool {pool} due to invalid normalized_price")
                continue

            order_map[order_price] += remaining_quantity

        sorted_bid_orders = sorted(bid_orders_map.items(), key=lambda x: -x[0])
        sorted_ask_orders = sorted(ask_orders_map.items(), key=lambda x: x[0])

        print(f"{pool} bid orders:", sorted_bid_orders)
        print(f"{pool} ask orders:", sorted_ask_orders)