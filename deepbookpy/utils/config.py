from pysui.sui.sui_config import SuiConfig
from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_builders.get_builders import GetAllCoins
from pysui.sui.sui_txresults.single_tx import SuiCoinObjects
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_clients.common import handle_result


def cfg_user():
    """."""
    cfg = SuiConfig.user_config(
        # Required
        rpc_url="https://fullnode.testnet.sui.io:443/",
        # Required. First entry becomes the 'active-address'
        # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
        prv_keys=["AIUPxQveY18QxhDDdTO0D0OD6PNVvtet50068d1grIyl"],
        # Optional, only needed for subscribing
        ws_url="wss://fullnode.testnet.sui.io:443/",
    )
    return cfg
cfg = cfg_user()
address = cfg.addresses[0]
client = SuiClient(cfg)
''''''
if __name__ == '__main__':

    cfg = cfg_user()
    address = cfg.addresses[0]
    client = SuiClient(cfg)
    for gas in handle_result(client.get_gas()).data:
        print(f"Gas ID {gas.coin_object_id} balance (mist) {gas.balance}")

    last_gas = None
    '''
    # SPLIT COINS / 2
    txn = SuiTransaction(client=client)
    txn.split_coin_equal(coin=txn.gas, split_count=2)
    tx_response = handle_result(txn.execute(gas_budget="1500000"))
    '''


    # MERGE COINS
    '''
    txn = SuiTransaction(client=client)
    sender = SuiAddress("0xffd8243510abac793771d998950d08d7a3ec6ad8f39d8e06b7b73687a93de2b9")
    print(sender)

    e_coins: SuiCoinObjects = handle_result(client.get_gas(address))
    txn.merge_coins(merge_to=txn.gas, merge_from=e_coins.data[1:])
        # Execute
    tx_result = txn.execute(gas_budget="100000")    
    '''

    ''''
    sender = SuiAddress("0xffd8243510abac793771d998950d08d7a3ec6ad8f39d8e06b7b73687a93de2b9")
        # Instantiate transaction block builder
    # SuiTransaction(client=client)    
    txer = SuiTransaction(client)
        # Get senders coin inventory and ensure there is at least 2
    e_coins: SuiCoinObjects = handle_result(client.get_gas(sender))
    assert len(e_coins.data) > 1, "Nothing to merge"
        # Merge all other coins but 1st (gas) to  gas
    txer.merge_coins(merge_to=txer.gas, merge_from=e_coins.data[1:])
        # Execute
    tx_result = txer.execute(gas_budget="100000")
    if tx_result.is_ok():
        if hasattr(tx_result.result_data, "to_json"):
            print(tx_result.result_data.to_json(indent=2))
        else:
            print(tx_result.result_data)
    else:
        print(tx_result.result_string)
    '''

    # AIUPxQveY18QxhDDdTO0D0OD6PNVvtet50068d1grIyl

    # provided by fastfrank : AOM6UAQrFe7r9nNDGRlWwj1o7m1cGK6mDZ3efRJJmvcG




