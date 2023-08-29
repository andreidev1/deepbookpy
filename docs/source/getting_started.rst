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

   from pysui.sui.sui_config import SuiConfig
   from pysui.sui.sui_clients.sync_client import SuiClient


   def cfg_user():
       """Config user"""
       cfg = SuiConfig.user_config(
           # Required
           rpc_url="https://fullnode.testnet.sui.io:443/",
           # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
           prv_keys=["AIUPxQveY18QggDDdTO0D0OD6PNVvtet50072d1grIyl"],
           # Needed for subscribing
           ws_url="wss://fullnode.testnet.sui.io:443/",
       )
       return cfg

   cfg = cfg_user()
   client = SuiClient(cfg)
   my_sui_address = cfg.addresses[0]

DeepBook Package ID
*******************

.. code:: py

   from deepbookpy.utils.normalizer import normalize_sui_object_id

   deepbook_package_id = normalize_sui_object_id("dee9")

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
