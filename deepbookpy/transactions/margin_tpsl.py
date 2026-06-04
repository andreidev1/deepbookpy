from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64

from deepbookpy.utils.config import DeepBookConfig, FLOAT_SCALAR

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