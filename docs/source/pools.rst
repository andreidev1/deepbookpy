=====
Pools
=====

Pools are shared objects that represent a market. 

Examples

Retrieve Account Information
----------------------------

Use `account()` method to retrieve the account information for a BalanceManager in a pool.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.account`

Output example

.. code-block:: json

    {
        "epoch": 704,
        "open_orders": {
            "constants": []
        },
        "taker_volume": 0,
        "maker_volume": 0,
        "active_stake": 0,
        "inactive_stake": 6,
        "created_proposal": false,
        "voted_proposal": null,
        "unclaimed_rebates": {
            "base": 0,
            "quote": 0,
            "deep": 0
        },
        "settled_balances": {
            "base": 0,
            "quote": 0,
            "deep": 0
        },
        "owed_balances": {
            "base": 0,
            "quote": 0,
            "deep": 0
        }
    }


Retrieve Open Orders
---------------------

Use `account_open_orders()` method to retrieve the open orders of an account.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.account_open_orders`

Output example

.. code-block:: python

    [
    "170141183460487678475761013267500113861",
    "170141183460487678475761013267500113862"
    ]


Check Balance Manager
---------------------

Use `check_manager_balance()` method to check the balance manager for a specific coin.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.check_manager_balance`

Get Order
---------

Use `get_order()` to retrieve an order's information.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_order`

Output example

.. code-block:: json

    {
        "balance_manager_id": "0x95784e000eedc2301d3fd1711f4132fdcacf5dec6137e7bfabcfd39e13fed537",
        "order_id": 18446762520453625325542354,
        "client_order_id": 1234,
        "quantity": 10000000000,
        "filled_quantity": 0,
        "fee_is_deep": true,
        "order_deep_price": {
            "asset_is_base": false,
            "deep_per_asset": 1000000000
        },
        "epoch": 733,
        "status": 0,
        "expire_timestamp": 1844674407370955161
    }


Get Normalized Order
--------------------

Use `get_order_normalized()` to get the order information for a specific order in a pool, with normalized price

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_order_normalized`

Output example

.. code-block:: json

    {
        "balance_manager_id": "0x95784e000eedc2301d3fd1711f4132fdcacf5dec6137e7bfabcfd39e13fed537",
        "order_id": 18446762520453625325542354,
        "client_order_id": 1234,
        "quantity": "10.0",
        "filled_quantity": "0",
        "fee_is_deep": true,
        "order_deep_price": {
            "asset_is_base": false,
            "deep_per_asset": "1000"
        },
        "epoch": 733,
        "status": 0,
        "expire_timestamp": 1844674407370955161,
        "is_bid": true,
        "normalized_price": 0.001
    }


Get Quote Quantity Out
----------------------

Use `get_quote_quantity_out()` to retrieve the quote quantity out for the base quantity you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_quote_quantity_out`

Output example

.. code-block:: json

    {
        "base_quantity": 1,
        "base_out": 0,
        "quote_out": 1,
        "deep_required": 0.001
    }


Get Base Quantity Out
---------------------

Use `get_base_quantity_out()` to retrieve the base quantity out for the quote quantity that you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_base_quantity_out`

Output example

.. code-block:: json

    {
        "quote_quantity": 1,
        "base_out": 0,
        "quote_out": 1,
        "deep_required": 0
    }


Get Quantity Out
----------------

Use `get_quantity_out()` to retrieve the output quantities for the base or quote quantity you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_quantity_out`


Get Level2 Range
----------------

Use `get_level2_range()` to retrieve level 2 order book within the boundary price range you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_level2_range`

Output example

.. code-block:: json

    {
        "prices": [
            1.99
        ],
        "quantities": [
            100.0
        ]
    }

Get Level2 Ticks from Mid
-------------------------

Use `get_level2_ticks_from_mid()` to retrieve level 2 order book ticks from mid-price for a pool with the ID you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_level2_ticks_from_mid`

Output example

.. code-block:: json

    {
        "bid_prices": [
            0.01
        ],
        "bid_quantities": [
            100.0
        ],
        "ask_prices": [
            1.99
        ],
        "ask_quantities": [
            100.0
        ]
    }


Get Locked Balance
------------------

Use `locked_balance()` to get locked balances for a pool and balance manager.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.locked_balance`

Output example

.. code-block:: json

    {
        "base": 0,
        "quote": 0,
        "deep": 0
    }


Get Pool Trade Params
---------------------

Use `pool_trade_params()` to get the trade parameters for a given pool, including taker fee, maker fee, and stake required.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.pool_trade_params`

Output example

.. code-block:: json

    {
        "taker_fee": 0.001,
        "maker_fee": 0.0005,
        "stake_required": 100
    }


Get Vault Balances
------------------

Use `vault_balances()` to get the vault balances for a pool with the ID you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.vault_balances`

Output example

.. code-block:: json

    {
        "base": 1,
        "quote": 10,
        "deep": 621815
    }


Get Pool ID by assets
---------------------

Use `get_pool_id_by_assets()` to retrieve the pool ID for the asset types you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.get_pool_id_by_assets`

Get Mid Price of a Pool
-----------------------

Use `mid_price()` to retrieve the mid price for a pool with the ID that you provide.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.mid_price`

Get Whitelist Status
--------------------

Use `whitelist()` to check if the pool with the ID you provide is whitelisted.

Reference : :py:meth:`deepbookpy.deepbook_client.DeepBookClient.whitelist`