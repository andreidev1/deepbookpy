from typing import Union

from pysui import SuiRpcResult
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU128, SuiU64, SuiU8, SuiBoolean

from deepbookpy.utils.config import DeepBookConfig, FLOAT_SCALAR, DEEP_SCALAR, POOL_CREATION_FEE
from deepbookpy.custom_types import PlaceLimitOrderParams, PlaceMarketOrderParams, SwapParams, CreatePermissionlessPoolParams
from deepbookpy.utils.constants import CLOCK, DEFAULT_EXPIRATION_TIMESTAMP
from deepbookpy.utils.coin import coin_with_balance

class DeepBookContract:
    def __init__(self, config: DeepBookConfig):
        """
        DeepBookContract class for managing DeepBook operations

        :param config: Configuration for DeepBookContract
        """
        self.__config = config


    def place_limit_order(self, params: PlaceLimitOrderParams, tx: SuiTransaction) -> SuiTransaction:
        """
        Place a limit order

        :param params: PlaceLimitOrder parameters
        :return: SuiTransaction object
        """
        pool_key = params.pool_key
        balance_manager_key = params.balance_manager_key
        client_order_id = params.client_order_id
        price = params.price
        quantity = params.quantity
        is_bid = params.is_bid
        expiration = params.expiration or DEFAULT_EXPIRATION_TIMESTAMP
        order_type = params.order_type or 0
        self_matching_option = params.self_matching_option or 0
        pay_with_deep = True

        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_price = round((price * FLOAT_SCALAR * quote_coin["scalar"]) / base_coin["scalar"])
        input_quantity = round(quantity * base_coin["scalar"])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::place_limit_order",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                SuiU64(client_order_id),
                SuiU8(order_type),
                SuiU8(self_matching_option),
                SuiU64(input_price),
                SuiU64(input_quantity),
                SuiBoolean(is_bid),
                SuiBoolean(pay_with_deep),
                SuiU64(expiration),
                ObjectID(CLOCK)
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx

    def place_market_order(self, params: PlaceMarketOrderParams, tx: SuiTransaction) -> SuiTransaction:
        """
        Place a market order

        :param params: PlaceMarketOrderParams parameters
        :return: SuiTransaction object
        """
        pool_key = params.pool_key
        balance_manager_key = params.balance_manager_key
        client_order_id = params.client_order_id
        quantity = params.quantity
        is_bid = params.is_bid
        self_matching_option = params.self_matching_option or 0
        pay_with_deep = True
        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(quantity * base_coin["scalar"])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::place_market_order",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                SuiU64(client_order_id),
                SuiU8(self_matching_option),
                SuiU64(input_quantity),
                SuiBoolean(is_bid),
                SuiBoolean(pay_with_deep),
                ObjectID(CLOCK)
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def modify_order(self, pool_key: str, balance_manager_key: str, order_id: str, new_quantity: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Modify a placed order

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :param order_id: order ID to modify
        :param new_quantity: new quantity for the order
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(new_quantity * base_coin["scalar"])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::modify_order",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                SuiU128(order_id),
                SuiU64(input_quantity),
                ObjectID(CLOCK)
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def cancel_order(self, pool_key: str, balance_manager_key: str, order_id: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Cancel a placed order

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :param order_id: order ID to cancel
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::cancel_order",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                SuiU128(order_id),
                ObjectID(CLOCK)
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    

    def cancel_all_orders(self, pool_key: str, balance_manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Cancel all placed orders

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::cancel_all_orders",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                ObjectID(CLOCK)
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def withdraw_settled_amounts(self, pool_key: str, balance_manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Withdraw settled amounts for a balance manager

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)(tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::withdraw_settled_amounts",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(balance_manager['address']),
                trade_proof,
                ],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def add_deep_price_point(self, target_pool_key: str, reference_pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Add a deep price point for a target pool using a reference pool

        :param target_pool_key: key to indentify the target pool
        :param reference_pool_key: key to identify the reference pool
        :return: SuiTransaction object
        """        
        target_pool = self.__config.get_pool(target_pool_key)
        reference_pool = self.__config.get_pool(reference_pool_key)
        target_base_coin = self.__config.get_coin(target_pool['base_coin'])
        target_quote_coin = self.__config.get_coin(target_pool['quote_coin'])
        reference_base_coin = self.__config.get_coin(reference_pool['base_coin'])
        reference_quote_coin = self.__config.get_coin(reference_pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::add_deep_price_point",
            arguments=[
                ObjectID(target_pool['address']),
                ObjectID(reference_pool['address']),
                ObjectID(CLOCK)
                ],
            type_arguments=[
                target_base_coin['type'],
                target_quote_coin['type'],
                reference_base_coin['type'],
                reference_quote_coin['type']
            ],
        )

        return tx
    
    def get_order(self, pool_key: str, order_id: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Gets an order

        :param pool_key: key to identify the pool
        :param order_id: order ID to get
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_order",
            arguments=[
                ObjectID(pool['address']),
                SuiU128(order_id)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_orders(self, pool_key: str, order_ids: list[str], tx: SuiTransaction) -> SuiTransaction:
        """
        Prepares a transaction to retrieve multiple orders from a specified pool.

        :param pool_key: key to identify the pool
        :param order_id: array of order IDs to retrieve.
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_orders",
            arguments=[
                ObjectID(pool['address']),
                [SuiU128(order_id) for order_id in order_ids]
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def burn_deep(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Burn DEEP tokens from the pool

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
       
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::burn_deep",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(self.__config.DEEP_TREASURY_ID)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx

    def mid_price(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the mid price for a pool

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::mid_price",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def whitelisted(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Check if a pool is whitelisted

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::whitelisted",
            arguments=[
                ObjectID(pool['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_quote_quantity_out(self, pool_key: str, base_quantity: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the quote quantity out for a given base quantity in

        :param pool_key: key to identify the pool
        :param base_quantity: base quantity to convert
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_quote_quantity_out",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(base_quantity * base_coin["scalar"]),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_base_quantity_out(self, pool_key: str, quote_quantity: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the base quantity out for a given quote quantity in

        :param pool_key: key to identify the pool
        :param quote_quantity: quote quantity to convert
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_base_quantity_out",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(quote_quantity * quote_coin["scalar"]),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_quantity_out(self, pool_key: str, base_quantity: int, quote_quantity: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the base quantity out for a given quote quantity in

        :param pool_key: key to identify the pool
        :param quote_quantity: quote quantity to convert
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_quantity_out",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(base_quantity * base_coin["scalar"]),
                SuiU64(quote_quantity * quote_coin["scalar"]),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def account_open_orders(self, pool_key: str, manager_key: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Get open orders for a balance manager in a pool

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        manager = self.__config.get_balance_manager(manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::account_open_orders",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(manager['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx

    def get_level2_range(self, pool_key: str, price_low: int, price_high: int, is_bid: bool, tx: SuiTransaction) -> SuiTransaction:
        """
        Get level 2 order book specifying range of price

        :param pool_key: key to identify the pool
        :param price_low: lower bound of the price range
        :param price_high: upper bound of the price range
        :param is_bid: whether to get bid or ask orders
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_level2_range",
            arguments=[
                ObjectID(pool['address']),
                SuiU64((price_low * FLOAT_SCALAR * quote_coin["scalar"]) / base_coin["scalar"]),
                SuiU64((price_high * FLOAT_SCALAR * quote_coin["scalar"]) / base_coin["scalar"]),
                SuiBoolean(is_bid),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_level2_ticks_from_mid(self, pool_key: str, tick_from_mid: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Get level 2 order book ticks from mid-price for a pool

        :param pool_key: key to identify the pool
        :param tick_from_mid: number of ticks from mid price
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_level2_ticks_from_mid",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(tick_from_mid),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def vault_balances(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the vault balances for a pool

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::vault_balances",
            arguments=[
                ObjectID(pool['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_pool_id_by_assets(self, base_type: str, quote_type: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the pool ID by asset types

        :param base_type: type of the base asset
        :param quote_type: type of the quote asset
        :return: SuiTransaction object
        """        
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_pool_id_by_asset",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID)
                ],
           type_arguments=[base_type, quote_type],
        )

        return tx

    def swap_exact_base_for_quote(self, sender_with_result: Union[SuiRpcResult, Exception], params: SwapParams, tx: SuiTransaction ) -> SuiTransaction:

        """
        Swap exact base amount for quote amount

        :param sender_with_result: list of owned objects
        :param SwapParams: Parameters for the swap
        :param coin_object: coin object ID
        :return: SuiTransaction object
        """

        if(params.quote_coin) :
            raise ValueError("quote coin is not accepted for swapping base asset")

        pool_key = params.pool_key
        base_amount = params.amount
        deep_amount = round(params.deep_amount * DEEP_SCALAR)
        min_quote = params.min_out

        pool = self.__config.get_pool(pool_key)
        deep_coin_type = self.__config.get_coin("DEEP")["type"]
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        quote = round(base_amount * base_coin["scalar"])

        base_coin_input = params.base_coin if params.base_coin is not None else coin_with_balance(sender_with_result, base_coin["type"], quote, tx)

        deep_coin_test = params.deep_coin if params.deep_coin is not None else coin_with_balance(sender_with_result, deep_coin_type, deep_amount, tx)

        min_quote_input = round(min_quote * quote_coin["scalar"])

        base_coin_result, quote_coin_result, deep_coin_result = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::swap_exact_base_for_quote",
            arguments=[
                ObjectID(pool["address"]),
                base_coin_input,
                deep_coin_test,
                SuiU64(min_quote_input),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return base_coin_result, quote_coin_result, deep_coin_result

    def swap_exact_quote_for_base(self, sender_with_result: Union[SuiRpcResult, Exception],  params: SwapParams, tx: SuiTransaction ) -> SuiTransaction:
        """
        Swap exact quote amount for base amount

        :param sender_with_result: list of owned objects
        :param SwapParams: Parameters for the swap
        :param coin_object: coin object ID
        :return: SuiTransaction object
        """

        if(params.quote_coin) :
            raise ValueError("quote coin is not accepted for swapping base asset")

        pool_key = params.pool_key
        quote_amount = params.amount
        deep_amount = params.deep_amount
        min_base = params.min_out

        pool = self.__config.get_pool(pool_key)
        deep_coin_type = self.__config.get_coin("DEEP")["type"]
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        quote_coin_input = params.quote_coin if params.quote_coin is not None else coin_with_balance(sender_with_result, quote_coin["type"], round(quote_amount * quote_coin["scalar"]), tx)

        deep_coin = params.deep_coin if params.deep_coin is not None else coin_with_balance(sender_with_result, deep_coin_type, round(deep_amount * DEEP_SCALAR), tx)

        min_base_input = round(min_base * quote_coin["scalar"])

        base_coin_result, quote_coin_result, deep_coin_result = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::swap_exact_quote_for_base",
            arguments=[
                ObjectID(pool["address"]),
                quote_coin_input,
                deep_coin,
                SuiU64(min_base_input),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return base_coin_result, quote_coin_result, deep_coin_result

    def pool_trade_params(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the trade parameters for a given pool, including taker fee, maker fee, and stake required.

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])


        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::pool_trade_params",
            arguments=[
                ObjectID(pool['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx

    def pool_book_params(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the book parameters for a given pool, including tick size, lot size, and min size.

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::pool_book_params",
            arguments=[
                ObjectID(pool['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def account(self, pool_key: str, manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the account information for a given pool and balance manager

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        manager_id = self.__config.get_balance_manager(manager_key)["address"]

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::account",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(manager_id)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def locked_balance(self, pool_key: str, manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the locked balance for a given pool and balance manager

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        manager_id = self.__config.get_balance_manager(manager_key)["address"]

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::locked_balance",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(manager_id)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_pool_deep_price(self, pool_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the DEEP price conversion for a pool

        :param pool_key: key to identify the pool
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_order_deep_price",
            arguments=[
                ObjectID(pool['address'])
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
        
    def create_permisionless_pool(self, sender_with_result: Union[SuiRpcResult, Exception], params: CreatePermissionlessPoolParams, tx: SuiTransaction) -> SuiTransaction:
        """
        Create a new pool permissionlessly

        :param sender_with_result: list of owned objects
        :param pool_key: Parameters for creating permissionless pool
        :return: SuiTransaction object
        """
        
        base_coin_key = params.base_coin_key
        quote_coin_key = params.quote_coin_key
        tick_size = params.tick_size
        lot_size = params.lot_size
        min_size = params.min_size
        deep_coin = params.deep_coin

        base_coin = self.__config.get_coin(base_coin_key)
        quote_coin = self.__config.get_coin(quote_coin_key)
        deep_coin_type = self.__config.get_coin("DEEP")["type"]

        base_scalar = base_coin["scalar"]
        quote_scalar = quote_coin["scalar"]

        adjusted_tick_size = tick_size * FLOAT_SCALAR * quote_scalar / base_scalar
        adjusted_lot_size = lot_size * base_scalar
        adjusted_min_size = min_size * base_scalar

        deep_coin_input = deep_coin if deep_coin is not None else coin_with_balance(sender_with_result, deep_coin_type, POOL_CREATION_FEE, tx)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::create_permissionless_pool",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                SuiU64(adjusted_tick_size),
                SuiU64(adjusted_lot_size),
                SuiU64(adjusted_min_size),
                deep_coin_input
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    