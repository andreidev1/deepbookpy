===============
Getting Started
===============

DeepBook Python SDK uses legacy pysui and canoser libraries as main dependencies allowing the interaction with on-chain Deepbook protocol.

Install deepbookpy
******************

Using ``pip``

`pip install deepbookpy`


Using ``poetry``

`poetry add deepbookpy`


Set up pysui config
*******************

Replace ``rpc_url``, ``prv_keys``, ``ws_url`` sample arguments with your own arguments.

.. code:: py

    from pysui import SyncClient, SuiConfig
    from pysui.sui.sui_txn import SyncTransaction


    # Init pysui config
    def cfg_user():
        cfg = SuiConfig.user_config(
            # Required
            rpc_url="https://fullnode.mainnet.sui.io:443/",
            # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
            prv_keys=["AIUPxQveY18QggDDdTO0D0OD6PNVveet50072d1frIal"],
            # Needed for subscribing
            ws_url="wss://fullnode.mainnet.sui.io:443/",
        )
        return cfg

    cfg = cfg_user()
    client = SyncClient(cfg)
    current_sui_address = cfg.addresses[0]
    txn = SyncTransaction(client=client)


Set up DeepBook Python SDK
**************************

After instantiating pysui client , you also need to instantiate ``DeepBookClient`` and ``DeepBookConfig`` classes.

.. code:: py

    from deepbookpy.deepbook_client import DeepBookClient
    from deepbookpy.utils.config import DeepBookConfig

    # Sample of Balance Manager
    balance_manager = {
        "MANAGER_1" : {
            "address" : "0x95784e000eedc2301d3fd1711f4132fdcacf5dec6137e7bfabcfd39e13fed537",
            "trade_cap" : "",
            "deposit_cap" : "0xdf55ef1b583f30dda21504153a141003ebbb480b38be6b9f6b68a0d1aaa9d84c",
            "withdraw_cap" : "0x0ee74c68d83c78e9a29fe36fb110122f2451a82c64830a6d9e9a66c5190032df"
        }
    }

    # Init DeepBook Client
    deepbook_client = DeepBookClient(client, current_sui_address, "mainnet", balance_manager)

    # Init DeepBook Config
    deepbook_config = DeepBookConfig("mainnet", "0x0", None, balance_manager)


Query DeepBook Protocol
***********************

Get the balance manager ID by calling ``get_balance_manager()``

.. code:: py

   result = deepbook_config.get_balance_manager("MANAGER_1")
   print(result)

Check balance manager by calling ``check_manager_balance()``

.. code:: py

   result = deepbook_client.check_manager_balance("MANAGER_1", "SUI")
   print(result)

On-Chain DeepBook Operations
****************************

To start interacting with on-chain Deepbook protocol, you first need to create a balance manager ID and then deposit coins into the balance manager.

Sample of creating a balance manager with deepbookpy 

.. code:: py

    deepbook_client.balance_manager.create_and_share_balance_manager(txn) 

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="10000000"))
    print(tx_result.to_json(indent=2))

Depositing into balance manager

.. code:: py

    deepbook_client.balance_manager.deposit_into_manager(
        manager_key="MANAGER_1", 
        coin_key="SUI", 
        amount_to_deposit=1, 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="10000000"))
    print(tx_result.to_json(indent=2))