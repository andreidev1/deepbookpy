from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8

from deepbookpy.utils.config import DeepBookConfig, FLOAT_SCALAR, MAX_TIMESTAMP
from deepbookpy.utils.constants import CLOCK
from deepbookpy.utils.conversion import convert_price, convert_quantity
from deepbookpy.custom_types import PendingLimitOrderParams, PendingMarketOrderParams, AddConditionalOrderParams

class MarginTPSLContract:
    """
    MarginTPSLContract class for managing Take Profit / Stop Loss operations.
    """
    def __init__(self, config: DeepBookConfig):
        """
        GovernanceContract class for managing governance operations in DeepBook


        :param config: Configuration for GovernanceContract
        """
        self.__config = config

        
    # Helper methods
    def new_condition(
        self,
        pool_key: str,
        trigger_below_price: bool,
        trigger_price: float,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Create a new condition for a conditional order

        :param pool_key: The key to identify the pool
        :param trigger_below_price: Whether to trigger when price is below trigger price
        :param trigger_price: The price at which to trigger the order
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        pool = self.__config.get_pool(pool_key)

        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        input_price = round(
            (trigger_price * FLOAT_SCALAR * quote_coin["scalar"]) / base_coin["scalar"]
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::tpsl::new_condition",
            arguments=[
                trigger_below_price,
                SuiU64(input_price),
            ],
        )

        return tx

    def new_pending_limit_order(
        self,
        params: PendingLimitOrderParams,
        pool_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Create a new pending limit order for use in conditional orders

        :param pool_key: The key to identify the pool
        :param params: Parameters for the pending limit order
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        client_order_id = params.client_order_id
        order_type = params.order_type or 0
        self_matching_option = params.self_matching_option or 0
        price = params.price
        quantity = params.quantity
        is_bid = params.is_bid
        pay_with_deep = params.pay_with_deep
        expire_timestamp = params.expire_timestamp or MAX_TIMESTAMP

        pool = self.__config.get_pool(pool_key)

        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        input_price = convert_price(
            price, FLOAT_SCALAR, quote_coin["scalar"], base_coin["scalar"]
        )
        input_quantity = convert_quantity(quantity, base_coin["scalar"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::tpsl::new_pending_limit_order",
            arguments=[
                SuiU64(client_order_id),
                SuiU8(order_type),
                SuiU8(self_matching_option),
                SuiU64(input_price),
                SuiU64(input_quantity),
                is_bid,
                pay_with_deep,
                SuiU64(expire_timestamp),
            ],
        )

        return tx

    def new_pending_market_order(
        self,
        params: PendingMarketOrderParams,
        pool_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Create a new pending market order for use in conditional orders

        :param params: Parameters for the pending market order
        :param pool_key: The key to identify the pool
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        client_order_id = params.client_order_id
        self_matching_option = params.self_matching_option
        quantity = params.quantity
        is_bid = params.is_bid
        pay_with_deep = params.pay_with_deep

        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool["base_coin"])
        input_quantity = convert_quantity(quantity, base_coin["scalar"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::tpsl::new_pending_market_order",
            arguments=[
                SuiU64(client_order_id),
                SuiU8(self_matching_option),
                SuiU64(input_quantity),
                is_bid,
                pay_with_deep,
            ],
        )

        return tx

    def add_conditional_order(
        self,
        params: AddConditionalOrderParams,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Add a conditional order (take profit or stop loss)

        :param params: Parameters for adding the conditional order
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        margin_manager_key = params.margin_manager_key
        conditional_order_id = params.conditional_order_id
        trigger_below_price = params.trigger_below_price
        trigger_price = params.trigger_price
        pending_order = params.pending_order

        manager = self.__config.get_margin_manager(margin_manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        condition = self.new_condition(
            pool_key=manager["pool_key"],
            trigger_below_price=trigger_below_price,
            trigger_price=trigger_price,
            tx=tx,
        )

        is_limit_order = isinstance(pending_order, PendingLimitOrderParams)
        pending = (
            self.new_pending_limit_order(params=pending_order, pool_key=manager["pool_key"], tx=tx)
            if is_limit_order
            else self.new_pending_market_order(params=pending_order, pool_key=manager["pool_key"], tx=tx)
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::add_conditional_order",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(pool["address"]),
                ObjectID(base_coin["price_info_object_id"]),
                ObjectID(quote_coin["price_info_object_id"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                SuiU64(conditional_order_id),
                condition,
                pending,
                ObjectID(CLOCK)
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx
  
    def cancel_all_conditional_orders(
        self,
        margin_manager_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Cancel all conditional orders for a margin manager

        :param margin_manager_key: The key to identify the margin manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        manager = self.__config.get_margin_manager(margin_manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::cancel_all_conditional_orders",
            arguments=[
                ObjectID(manager["address"]),
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx

    def cancel_conditional_order(
        self,
        margin_manager_key: str,
        conditional_order_id: int,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Cancel a specific conditional order

        :param margin_manager_key: The key to identify the margin manager
        :param conditional_order_id: The ID of the conditional order to cancel
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        manager = self.__config.get_margin_manager(margin_manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::cancel_conditional_order",
            arguments=[
                ObjectID(manager["address"]),
                SuiU64(conditional_order_id),
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx  

    # Read-only methods
    def conditional_order_ids(
        self, pool_key: str, margin_manager_id: str, tx: SuiTransaction
    ) -> SuiTransaction:
        """
        Get all conditional order IDs for a margin manager

        :param pool_key: The key to identify the pool
        :param margin_manager_id: The ID of the margin manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        pool = self.__config.get_pool(pool_key)

        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::conditional_order_ids",
            arguments=[
                ObjectID(margin_manager_id),
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx


    def conditional_order(
        self,
        pool_key: str,
        margin_manager_id: str,
        conditional_order_id: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Get a specific conditional order by ID

        :param pool_key: The key to identify the pool
        :param margin_manager_id: The ID of the margin manager
        :param conditional_order_id: The ID of the conditional order
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        pool = self.__config.get_pool(pool_key)

        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::conditional_order",
            arguments=[
                ObjectID(margin_manager_id),
                SuiU64(conditional_order_id),
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx


    def lowest_trigger_above_price(
        self, pool_key: str, margin_manager_id: str, tx: SuiTransaction
    ) -> SuiTransaction:
        """
        Get the lowest trigger price for trigger_above orders
        Returns max_u64 if there are no trigger_above orders

        :param pool_key: The key to identify the pool
        :param margin_manager_id: The ID of the margin manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """

        pool = self.__config.get_pool(pool_key)

        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::lowest_trigger_above_price",
            arguments=[
                ObjectID(margin_manager_id),
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )

        return tx