======
Orders
======


Before you can place orders, though, you must first set up a `balance manager <https://deepbookpy.readthedocs.io/en/latest/getting_started.html>`_.


Place a limit order
-------------------

To place a limit order use ``place_limit_order()`` method. This method call returns `SuiTransaction` object

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.place_limit_order`

.. code:: py

    # Add arguments for place_limit_order() method
    place_limit_order_params = PlaceLimitOrderParams(
        pool_key="SUI_DBUSDC",
        balance_manager_key="MANAGER_1",
        client_order_id=1234,
        price=1,
        quantity=2,
        is_bid=False,
    )

    # Call place_limit_order() method
    deepbook_client.deepbook.place_limit_order(place_limit_order_params, txn)

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Place a market order
--------------------

To place a limit order use ``place_market_order()`` method. This method returns `SuiTransaction` object

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.place_market_order`

.. code:: py

    # Add arguments for place_market_order() method
    place_market_order_params = PlaceMarketOrderParams(
        pool_key="SUI_DBUSDC",
        balance_manager_key="MANAGER_1",
        client_order_id=1234,
        quantity=5,
        is_bid=True
    )

    # Call place_market_order() method
    deepbook_client.deepbook.place_market_order(place_market_order_params, txn)

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Cancel an order
---------------

To cancel an active order you have to pass the order id. This method call returns `SuiTransaction` object.

.. warning::

    The `order_id` is the protocol `order_id` generated during order placement, which is different from the client `order_id`

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.cancel_order`

.. code:: py
    
    # Call cancel_order() method
    deepbook_client.deepbook.cancel_order(
        pool_key="SUI_DBUSDC", 
        balance_manager_key="MANAGER_1", 
        order_id="170141183460487678475761013267500113857", 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Cancel all orders
-----------------

Use `cancel_all_orders()` method to cancel all active orders. This method call returns `SuiTransaction` object.

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.cancel_all_orders`

.. code:: py
    
    # Call cancel_all_orders() method
    deepbook_client.deepbook.cancel_all_orders(
        pool_key="SUI_DBUSDC", 
        balance_manager_key="MANAGER_1", 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))
