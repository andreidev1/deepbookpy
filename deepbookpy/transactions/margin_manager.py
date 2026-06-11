from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from deepbookpy.utils.constants import CLOCK
from deepbookpy.custom_types import DepositDuringInitParams, DepositParams
from deepbookpy.utils.conversion import convert_quantity

class MarginManagerContract:
    """
    MarginManagerContract class for managing MarginManager operations.
    """
    def __init__(self, config: DeepBookConfig):
        self.__config = config

    def new_margin_manager(
        self,
        pool_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Create a new margin manager

        :param pool_key: The key to identify the pool
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::new",
            arguments=[
                ObjectID(pool["address"]),
                ObjectID(self.__config.REGISTRY_ID),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )
        return tx

    def new_margin_manager_with_initializer(
        self,
        pool_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Create a new margin manager with an initializer

        :param pool_key: The key to identify the pool
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::new_with_initializer",
            arguments=[
                ObjectID(pool["address"]),
                ObjectID(self.__config.REGISTRY_ID),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )
        return tx

    def share_margin_manager(
        self,
        pool_key: str,
        manager: any,
        initializer: any,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Share a margin manager

        :param pool_key: The key to identify the pool
        :param manager: The margin manager to share
        :param initializer: The initializer for the manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::share",
            arguments=[manager, initializer],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )
        return tx

    def register_margin_manager(
        self,
        manager_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Register a margin manager back to the margin registry. Lets owners restore
        visibility of a manager that was unregistered by another platform.

        :param manager_key: The key to identify the margin manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = self.__config.get_margin_manager(manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::register_margin_manager",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )
        return tx

    def unregister_margin_manager(
        self,
        manager_key: str,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Unregister a margin manager from the margin registry. Aborts if the manager
        holds any outstanding debt or base/quote/DEEP balance.

        :param manager_key: The key to identify the margin manager
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = self.__config.get_margin_manager(manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::unregister_margin_manager",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]],
        )
        return tx
    
    def deposit_during_initialization(
        self,
        params: DepositDuringInitParams,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Deposit into a margin manager during initialization (before sharing).
        Use this when you need to deposit funds into a newly created manager in the same transaction.

        :param params: The deposit parameters
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = params.manager
        pool_key = params.pool_key
        coin_type = params.coin_type

        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])
        deposit_coin = self.__config.get_coin(coin_type)

        coin = (
            convert_quantity(params.amount, deposit_coin["scalar"])
            if hasattr(params, "amount") and params.amount is not None
            else params.coin
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::deposit",
            arguments=[
                manager,
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                ObjectID(base_coin["price_info_object_id"]),
                ObjectID(quote_coin["price_info_object_id"]),
                coin,
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"], deposit_coin["type"]],
        )
        return tx

    def deposit_base(
        self,
        params: DepositParams,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Deposit base into a margin manager

        :param params: The deposit parameters
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = self.__config.get_margin_manager(params.manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        coin = (
            convert_quantity(params.amount, base_coin["scalar"])
            if hasattr(params, "amount") and params.amount is not None
            else params.coin
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::deposit",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                ObjectID(base_coin["price_info_object_id"]),
                ObjectID(quote_coin["price_info_object_id"]),
                coin,
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"], base_coin["type"]],
        )
        return tx

    def deposit_quote(
        self,
        params: DepositParams,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Deposit quote into a margin manager

        :param params: The deposit parameters
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = self.__config.get_margin_manager(params.manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])

        coin = (
            convert_quantity(params.amount, quote_coin["scalar"])
            if hasattr(params, "amount") and params.amount is not None
            else params.coin
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::deposit",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                ObjectID(base_coin["price_info_object_id"]),
                ObjectID(quote_coin["price_info_object_id"]),
                coin,
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"], quote_coin["type"]],
        )
        return tx

    def deposit_deep(
        self,
        params: DepositParams,
        tx: SuiTransaction,
    ) -> SuiTransaction:
        """
        Deposit deep into a margin manager

        :param params: The deposit parameters
        :param tx: SuiTransaction object
        :return: SuiTransaction object
        """
        manager = self.__config.get_margin_manager(params.manager_key)
        pool = self.__config.get_pool(manager["pool_key"])
        base_coin = self.__config.get_coin(pool["base_coin"])
        quote_coin = self.__config.get_coin(pool["quote_coin"])
        deep_coin = self.__config.get_coin("DEEP")

        coin = (
            convert_quantity(params.amount, deep_coin["scalar"])
            if hasattr(params, "amount") and params.amount is not None
            else params.coin
        )

        tx.move_call(
            target=f"{self.__config.MARGIN_PACKAGE_ID}::margin_manager::deposit",
            arguments=[
                ObjectID(manager["address"]),
                ObjectID(self.__config.MARGIN_REGISTRY_ID),
                ObjectID(base_coin["price_info_object_id"]),
                ObjectID(quote_coin["price_info_object_id"]),
                coin,
                CLOCK,
            ],
            type_arguments=[base_coin["type"], quote_coin["type"], deep_coin["type"]],
        )
        return tx