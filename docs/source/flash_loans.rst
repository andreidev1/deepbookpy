===========
Flash Loans
===========

A flash loan is one where the borrowing and returning of loans from pools is performed within a single programmable transaction block. 
The SDK exposes functions that allow you to implement this functionality.


Borrow Base Asset
-----------------

Use `borrow_base_asset()` to borrow a base asset from the pool identified by the `pool_key` value you provide.

Reference : :py:meth:`deepbookpy.transactions.flash_loans.FlashLoanContract.borrow_base_asset`

Return Base Asset
-----------------

Use `return_base_asset()` to return the base asset to the pool identified by the `pool_key` value you provide.

Reference : :py:meth:`deepbookpy.transactions.flash_loans.FlashLoanContract.return_base_asset`

Borrow Quote Asset
------------------

Use `borrow_quote_asset()` to borrow a quote asset from the pool identified by the `pool_key` value you provide.

Reference : :py:meth:`deepbookpy.transactions.flash_loans.FlashLoanContract.borrow_quote_asset`

Return Quote Asset
------------------

Use `return_quote_asset()` to return a quote asset to the pool identified by the `pool_key` you provide.

Reference : :py:meth:`deepbookpy.transactions.flash_loans.FlashLoanContract.return_quote_asset`


Basic Flash Loan Example
------------------------

.. code:: py

    # Call borrow_base_asset method to borrow 1 DEEP from DEEP_SUI pool
    [deep_coin, flash_loan] = deepbook_client.flash_loans.borrow_base_asset(
        pool_key="DEEP_SUI", 
        borrow_amount=borrow_amount, 
        tx=txn
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

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))

Advanced Flash Loan Example
---------------------------

.. code:: py
    
    """
    - Borrow 1 DEEP from the DEEP_SUI pool
    - Swap 0.5 DBUSDC for SUI in the SUI_DBUSDC pool, paid using the borrowed DEEP
    - Swap SUI back to DEEP
    - Return 1 DEEP to the DEEP_SUI pool
    """
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

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))