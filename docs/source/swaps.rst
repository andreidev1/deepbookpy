=====
Swaps
=====

DeepBookV3 provides a swap-like interface commonly seen in automatic market makers (AMMs). 
The deepbookpy SDK provides functions to leverage the features of this interface.

.. note::
    The official DeepBook TypeScript SDK uses the `CoinWithBalance` intent built into the Sui TypeScript SDK, 
    making it easy to retrieve a coin with a specific balance.

    Since there is no intent plugin to legacy pysui, deepbookpy comes with own solution
    by providing :py:meth:`deepbookpy.utils.coin.coin_with_balance` util that aims to replicate
    the basic functionality of `CoinWithBalance` intent as in the Sui TypeScript SDK.


Swap Exact Base For Quote
-------------------------

Use `swap_exact_base_for_quote()` method to swap exact base amount for quote amount.

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.swap_exact_base_for_quote`

.. code:: py

    # Add arguments for swap parameters
    swap_params = SwapParams(
        pool_key="SUI_DBUSDC",
        amount=1,
        deep_amount=2,
        min_out=0
    )

    # Call swap_exact_base_for_quote method
    coin_result = deepbook_client.deepbook.swap_exact_base_for_quote(
        sender_with_result=client.get_objects(), 
        params=swap_params, 
        tx=txn
        )

    # Transfer output objects
    txn.transfer_objects(transfers=[coin_result[0], coin_result[1], coin_result[2]], recipient=SuiAddress(current_sui_address))

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Swap Exact Quote For Base
-------------------------

Use `swap_exact_quote_for_base()` method to swap exact quote amount for base amount.

Reference : :py:meth:`deepbookpy.transactions.deepbook.DeepBookContract.swap_exact_quote_for_base`

.. code:: py

    # Add arguments for swap parameters
    swap_params = SwapParams(
        pool_key="SUI_DBUSDC",
        amount=1,
        deep_amount=1,
        min_out=0.1
    )

    # Call swap_exact_quote_for_base method
    coin_result = deepbook_client.deepbook.swap_exact_quote_for_base(
        sender_with_result=client.get_objects(), 
        params=swap_params, 
        tx=txn
        )

    # Transfer output objects
    txn.transfer_objects(transfers=[coin_result[0], coin_result[1], coin_result[2]], recipient=SuiAddress(current_sui_address))

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))
