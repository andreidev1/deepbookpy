"""
Borrow 1 DEEP from the DEEP_SUI pool
Swap 0.5 DBUSDC for SUI in the SUI_DBUSDC pool, paid using the borrowed DEEP
Swap SUI back to DEEP
Return 1 DEEP to the DEEP_SUI pool
"""
import os
import sys
import pathlib

from dotenv import load_dotenv
from pysui import SyncClient, SuiConfig, SuiAddress, handle_result
from pysui.sui.sui_txn import SyncTransaction

PROJECT_DIR = pathlib.Path(os.path.dirname(__file__))
PARENT = PROJECT_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(os.path.join(PARENT, "deepbookpy")))

from deepbookpy.deepbook_client import DeepBookClient
from deepbookpy.utils.config import DeepBookConfig
from deepbookpy.custom_types import SwapParams, PlaceLimitOrderParams

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")


if __name__ == "__main__":

    # Init pysui config
    def cfg_user():
        cfg = SuiConfig.user_config(
            # Required
            rpc_url="https://fullnode.testnet.sui.io:443/",
            # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
            prv_keys=[private_key],
            # Needed for subscribing
            ws_url="wss://fullnode.testnet.sui.io:443/",
        )
        return cfg

    cfg = cfg_user()
    client = SyncClient(cfg)
    current_sui_address = cfg.addresses[0]
    txn = SyncTransaction(client=client)

    balance_manager = {
        "MANAGER_1" : {
            "address" : "0x95784e000eedc2301d3fd1711f4132fdcacf5dec6137e7bfabcfd39e13fed537",
            "trade_cap" : "",
            "deposit_cap" : "0xdf55ef1b583f30dda21504153a141003ebbb480b38be6b9f6b68a0d1aaa9d84c",
            "withdraw_cap" : "0x0ee74c68d83c78e9a29fe36fb110122f2451a82c64830a6d9e9a66c5190032df"
        }
    }
    # Init deepbook client
    deepbook_client = DeepBookClient(client, current_sui_address, "testnet", balance_manager)
    
    # Init deepbook config
    deepbook_config = DeepBookConfig("testnet", "0x0", None, balance_manager)

    # Set borrow amount
    borrow_amount = 1

    # Call borrow_base_asset method to borrow 1 DEEP from DEEP_SUI pool
    [deep_coin, flash_loan] = deepbook_client.flash_loans.borrow_base_asset(
        pool_key="DEEP_SUI",
        borrow_amount=borrow_amount,
        tx=txn
        )

    # Add arguments for borrow deep parameters
    borrow_deep_params = SwapParams(
        pool_key="SUI_DBUSDC",
        amount=0.5,
        deep_amount=1,
        min_out=0,
        deep_coin=deep_coin
    )

    # Call swap_exact_base_for_quote method to trade using borrowed DEEP
    borrow_deep_tx = deepbook_client.deepbook.swap_exact_base_for_quote(
        sender_with_result=client.get_objects(),
        params=borrow_deep_params,
        tx=txn
        )

    txn.transfer_objects(
        transfers=[
            borrow_deep_tx[0],
            borrow_deep_tx[1],
            borrow_deep_tx[2],
        ],
        recipient=SuiAddress(current_sui_address),
    )

    # Add arguments for deep repayment parameters
    repay_deep_params = SwapParams(
        pool_key="DEEP_SUI",
        amount=10,
        deep_amount=0,
        min_out=0
    )

    # Execute second trade to get back DEEP for repayment
    coin_result = deepbook_client.deepbook.swap_exact_base_for_quote(
        sender_with_result=client.get_objects(),
        params=repay_deep_params,
        tx=txn
        )

    txn.transfer_objects(
        transfers=[
            coin_result[0],
            coin_result[1],
            coin_result[2],
        ],
        recipient=SuiAddress(current_sui_address),
    )

    # Call return_base_asset method to return borrowed DEEP
    loan_remain = deepbook_client.flash_loans.return_base_asset(
        pool_key="DEEP_SUI",
        borrow_amount=borrow_amount,
        base_coin_input=deep_coin,
        flash_loan=flash_loan,
        tx=txn
        )

    # Transfer the remaining coin to user's address
    txn.transfer_objects(transfers=[loan_remain], recipient=SuiAddress(current_sui_address))


    # Add arguments for place_limit_order() method
    place_limit_order_params = PlaceLimitOrderParams(
        pool_key="SUI_DBUSDC",
        balance_manager_key="MANAGER_1",
        client_order_id=123456789,
        price=1,
        quantity=10,
        is_bid=True,
    )

    # Call place_limit_order() method
    deepbook_client.deepbook.place_limit_order(place_limit_order_params, txn)

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))

