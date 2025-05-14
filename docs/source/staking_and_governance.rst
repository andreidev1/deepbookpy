======================
Staking and Governance
======================

Examples of interacting with staking and governance. These functions typically require a `balance_manager_key`, `pool_key`, or both.

Stake 
-----

Use `stake()` method to stake a specified amount in the pool.

Reference : :py:meth:`deepbookpy.transactions.governance.GovernanceContract.stake`

.. code:: py

    # Call stake method
    deepbook_client.governance.stake(
        pool_key="DEEP_SUI", 
        balance_manager_key="MANAGER_1", 
        stake_amount=5, 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))

Unstake
-------

Use `unstake()` method to unstake amount from the pool.

Reference : :py:meth:`deepbookpy.transactions.governance.GovernanceContract.unstake`

.. code:: py

    # Call unstake method
    deepbook_client.governance.unstake(
        pool_key="DEEP_SUI", 
        balance_manager_key="MANAGER_1", 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Submit Proposal
---------------

Use `submit_proposal()` method to submit a governance proposal.

Reference : :py:meth:`deepbookpy.transactions.governance.GovernanceContract.submit_proposal`

.. code:: py

    # Add arguments for proposal parameters
    proposal_params = ProposalParams(
        pool_key="DEEP_SUI",
        balance_manager_key="MANAGER_1",
        taker_fee=0.1,
        maker_fee=0.1,
        stake_required=1
    )

    # Call submit proposal method
    deepbook_client.governance.submit_proposal(
        params=proposal_params, 
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))


Vote
----

Use `vote()` method to vote on a governance proposal.

Reference : :py:meth:`deepbookpy.transactions.governance.GovernanceContract.vote`

.. code:: py

    # Call submit proposal method
    deepbook_client.governance.vote(
        pool_key="DBUSDT_DBUSDC",
        balance_manager_key="MANAGER_1",
        proposal_id="0x123456789",
        tx=txn
        )

    # Execute the transaction
    tx_result = handle_result(txn.execute(gas_budget="100000000"))
    print(tx_result.to_json(indent=2))
