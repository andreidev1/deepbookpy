from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU128, SuiU64, SuiU8, SuiBoolean

from utils.config import DeepBookConfig, FLOAT_SCALAR
from custom_types import PlaceLimitOrderParams, PlaceMarketOrderParams, SwapParams
from utils.constants import CLOCK




class DeepBookContract:
    def __init__(self, config: DeepBookConfig):
        """
        DeepBookContract class for managing DeepBook operations

        :param config: Configuration for DeepBookContract
        """
        self.__config = config


    def place_limit_order(self, tx: SuiTransaction, params: PlaceLimitOrderParams) -> SuiTransaction:
        """
        Place a limit order

        :param params: PlaceLimitOrder parameters
        """
        pool_key = params.pool_key
        balance_manager_key = params.balance_manager_key
        client_order_id = params.client_order_id
        price = params.price
        quantity = params.quantity
        is_bid = params.is_bid
        expiration = params.expiration
        order_type = params.order_type
        self_matching_option = params.self_matching_option
        pay_with_deep = True

        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_price = round((price * FLOAT_SCALAR * quote_coin.scalar) / base_coin.scalar)
        input_quantity = round(quantity * base_coin.scalar)

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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

    def place_market_order(self, tx: SuiTransaction, params: PlaceMarketOrderParams) -> SuiTransaction:
        """
        Place a market order

        :param params: PlaceMarketOrderParams parameters
        """
        pool_key = params.pool_key
        balance_manager_key = params.balance_manager_key
        client_order_id = params.client_order_id
        quantity = params.quantity
        is_bid = params.is_bid
        self_matching_option = params.self_matching_option
        pay_with_deep = True

        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(quantity * base_coin.scalar)

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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
    
    def modify_order(self, tx: SuiTransaction, pool_key: str, balance_manager_key: str, order_id: str, new_quantity: int) -> SuiTransaction:
        """
        Modify a placed order

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :param order_id: order ID to modify
        :param new_quantity: new quantity for the order
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(new_quantity * base_coin.scalar)

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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
    
    def cancel_order(self, tx: SuiTransaction, pool_key: str, balance_manager_key: str, order_id: str) -> SuiTransaction:
        """
        Cancel a placed order

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :param order_id: order ID to cancel
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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
    

    def cancel_all_orders(self, tx: SuiTransaction, pool_key: str, balance_manager_key: str) -> SuiTransaction:
        """
        Cancel all placed orders

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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
    
    def withdraw_settled_amounts(self, tx: SuiTransaction, pool_key: str, balance_manager_key: str) -> SuiTransaction:
        """
        Withdraw settled amounts for a balance manager

        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        """        
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        trade_proof = self.__config.balance_manager.generate_proof(balance_manager_key)

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
    
    def add_deep_price_point(self, tx: SuiTransaction, target_pool_key: str, reference_pool_key: str) -> SuiTransaction:
        """
        Add a deep price point for a target pool using a reference pool

        :param target_pool_key: key to indentify the target pool
        :param reference_pool_key: key to identify the reference pool
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
                ObjectID(reference_pool['address'])
                ],
            type_arguments=[
                target_base_coin['type'],
                target_quote_coin['type'],
                reference_base_coin['type'],
                reference_quote_coin['type']
            ],
        )

        return tx
    
    def get_order(self, tx: SuiTransaction, pool_key: str, order_id: str) -> SuiTransaction:
        """
        Gets an order

        :param pool_key: key to identify the pool
        :param order_id: order ID to get
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
    
    def get_orders(self, tx: SuiTransaction, pool_key: str, order_ids: list[str]) -> SuiTransaction:
        """
        Prepares a transaction to retrieve multiple orders from a specified pool.

        :param pool_key: key to identify the pool
        :param order_id: array of order IDs to retrieve.
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
       

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_orders",
            arguments=[
                ObjectID(pool['address']),
                SuiU128(order_ids)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def burn_deep(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Burn DEEP tokens from the pool

        :param pool_key: key to identify the pool
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

    def mid_price(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Get the mid price for a pool

        :param pool_key: key to identify the pool
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
        """        
        pool = self.__config.get_pool(pool_key)
        print("this is pool", pool)

        base_coin = self.__config.get_coin(pool['base_coin'])
        print('this is base coin', base_coin)
        quote_coin = self.__config.get_coin(pool['quote_coin'])
       

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::whitelisted",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_quote_quantity_out(self, tx: SuiTransaction, pool_key: str, base_quantity: int) -> SuiTransaction:
        """
        Get the quote quantity out for a given base quantity in

        :param pool_key: key to identify the pool
        :param base_quantity: base quantity to convert
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
       

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_quote_quantity",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(base_quantity * base_coin.scalar),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_base_quantity_out(self, tx: SuiTransaction, pool_key: str, quote_quantity: int) -> SuiTransaction:
        """
        Get the base quantity out for a given quote quantity in

        :param pool_key: key to identify the pool
        :param quote_quantity: quote quantity to convert
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_base_quantity",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(quote_quantity * quote_coin.scalar),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_quantity_out(self, tx: SuiTransaction, pool_key: str, quote_quantity: int) -> SuiTransaction:
        """
        Get the base quantity out for a given quote quantity in

        :param pool_key: key to identify the pool
        :param quote_quantity: quote quantity to convert
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_base_quantity",
            arguments=[
                ObjectID(pool['address']),
                SuiU64(quote_quantity * quote_coin.scalar),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def account_open_orders(self, tx: SuiTransaction, pool_key: str, manager_key: int) -> SuiTransaction:
        """
        Get open orders for a balance manager in a pool

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
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

    def get_level2_range(self, tx: SuiTransaction, pool_key: str, price_low: int, price_high: int, is_bid: bool) -> SuiTransaction:
        """
        Get level 2 order book specifying range of price

        :param pool_key: key to identify the pool
        :param price_low: lower bound of the price range
        :param price_high: upper bound of the price range
        :param is_bid: whether to get bid or ask orders
        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_level2_range",
            arguments=[
                ObjectID(pool['address']),
                SuiU64((price_low * FLOAT_SCALAR * quote_coin.scalar) / base_coin.scalar),
                SuiU64((price_high * FLOAT_SCALAR * quote_coin.scalar) / base_coin.scalar),
                SuiBoolean(is_bid),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_level2_ticks_from_mid(self, tx: SuiTransaction, pool_key: str, tick_from_mid: int) -> SuiTransaction:
        """
        Get level 2 order book ticks from mid-price for a pool

        :param pool_key: key to identify the pool
        :param tick_from_mid: number of ticks from mid price
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
    
    def vault_balances(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Get the vault balances for a pool

        :param pool_key: key to identify the pool

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
    
    def get_pool_id_by_assets(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Get the pool ID by asset types

        :param pool_key: key to identify the pool

        """        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::get_pool_id_by_asset",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    # TO DO
    """
    def swap_exact_base_for_quote(self, tx: SuiTransaction, params: SwapParams) -> SuiTransaction:

        #Swap exact base amount for quote amount

        #:param pool_key: key to identify the pool


        if(params.quote_coin) :
            raise ValueError("quote coin is not accepted for swapping base asset")

        pool_key = params.pool_key
        amount = params.amount
        deep_amount = params.deep_amount
        min_quote = params.min_out

        pool = self.__config.get_pool(pool_key)
        deep_coin_type = self.__config.get_coin("DEEP").type
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        base_coin_input = (
            params.base_coin 
            if params.base_coin is not None 
            else coin_with_balance({
                "type": base_coin.type, 
                "balance": round(base_amount * base_coin.scalar)
            })
        )
        deep_coin = ""

        min_quote_input = round(min_quote * quote_coin.scalar)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::swap_exact_base_for_quote",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                base_coin_input,
                deep_coin,
                SuiU64(min_quote_input),
                ObjectID(CLOCK)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    """
    def pool_book_params(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Get the trade parameters for a given pool, including taker fee, maker fee, and stake required.

        :param pool_key: key to identify the pool
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
    
    def account(self, tx: SuiTransaction, pool_key: str, manager_key: str) -> SuiTransaction:
        """
        Get the account information for a given pool and balance manager

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        manager_id = self.__config.get_balance_manager(manager_key).address

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::account",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(manager_id)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def locked_balance(self, tx: SuiTransaction, pool_key: str, manager_key: str) -> SuiTransaction:
        """
        Get the locked balance for a given pool and balance manager

        :param pool_key: key to identify the pool
        :param manager_key: key of the BalanceManager
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        manager_id = self.__config.get_balance_manager(manager_key).address

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::locked_balance",
            arguments=[
                ObjectID(pool['address']),
                ObjectID(manager_id)
                ],
           type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return tx
    
    def get_pool_deep_price(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Get the DEEP price conversion for a pool

        :param pool_key: key to identify the pool
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