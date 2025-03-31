Quick Start
------------------

Install deepbookpy
******************

Using ``pip``

`pip install deepbookpy`


Using ``poetry``

`poetry add deepbookpy`


Set up pysui config
*******************

Replace ``rpc_url``, ``prv_keys``, ``ws_url`` with your desired data.

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


Instantiate DeepBook Python SDK
**********************

    # Sample of Balance Manager
    balance_manager = {
        "MANAGER_1" : {
            "address" : "0x344c2734b1d211bd15212bfb7847c66a3b18803f3f5ab00f5ff6f87b6fe6d27d",
            "trade_cap" : ""
        }
    }

    # Init DeepBook Client
    deepbook_client = DeepBookClient(client, current_sui_address, "mainnet", balance_manager)

    # Init deepbook config
    deepbook_config = DeepBookConfig("mainnet", "0x0", None, balance_manager)


Query DeepBook Package
**********************

In order to query the deepbook package you have to instantiate
``DeepBookQuery`` class

.. code:: py

   from deepbookpy.deepbook_client import DeepBookClient


   deepbook_query = DeepBookClient(
       client=client,
       package_id=deepbook_package_id
   )

Sample of calling ``get_market_price()``

.. code:: py


   deepbook_query.get_market_price(
       pool_id="0xdb4ec5cdc7b98f085ffc8d3e6d7bfaeff5fafe6fb928e2617be9ea501ce1036c"
   )

Write to DeepBook Package
*************************

In order to write to the deepbook package you have to instantiate
``DeepBookClient`` class

.. code:: py

   from deepbookpy.deepbook_client import DeepBookClient


   deepbook = DeepBookClient(
       client=client,
       package_id=deepbook_package_id
   )

Sample of executing ``create_pool()``

.. code:: py

   from deepbookpy.deepbook_client import DeepBookClient

   create_pool = deepbook.create_pool(
       base_asset="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
       quote_asset="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
       tick_size=10000000,
       lot_size=10000
   )

   # Execute the transaction
   tx_result = create_pool.execute(gas_budget="10000000")
   if tx_result.is_ok():
       if hasattr(tx_result.result_data, "to_json"):
           print(tx_result.result_data.to_json(indent=2))
       else:
           print(tx_result.result_data)
   else:
       print(tx_result.result_string)
