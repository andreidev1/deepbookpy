from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui.sui.sui_types.address import SuiAddress

from deepbookpy.utils.config import DeepBookConfig, FLOAT_SCALAR
from deepbookpy.custom_types import CreatePoolAdminParams

class DeepBookAdminContract:
    def __init__(self, config: DeepBookConfig):
        """
        DeepBookAdminContract class for managing admin actions.

       
        :param config: Configuration for DeepBookAdminContract
        """
        self.__config = config


    def __admin_cap(self):
        """
        Get the admin capability required for admin operations.
        """
        
        admin_cap = self.__config.admin_cap
        if not admin_cap:
            raise EnvironmentError('ADMIN_CAP environment variable not set')
        return admin_cap

    def create_pool_admin(self, tx: SuiTransaction, params: CreatePoolAdminParams) -> SuiTransaction:
        """
        Create a new pool as admin

        :param params: parameters for creating pool as admin
        
        """
        base_coin_key = params.base_coin_key
        quote_coin_key = params.quote_coin_key
        tick_size = params.tick_size
        lot_size = params.lot_size
        min_size = params.min_size
        whitelisted = params.whitelisted
        stable_pool = params.stable_pool

        base_coin = self.__config.get_coin(base_coin_key)
        quote_coin = self.__config.get_coin(quote_coin_key)
        
        base_scalar = base_coin.scalar
        quote_scalar = quote_coin.scalar

        adjusted_tick_size = tick_size * FLOAT_SCALAR * quote_scalar
        adjusted_lot_size = lot_size * base_scalar
        adjusted_min_size = min_size * base_scalar

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::create_pool_admin",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                SuiU64(adjusted_tick_size),
                SuiU64(adjusted_lot_size),
                SuiU64(adjusted_min_size),
                SuiBoolean(whitelisted),
                SuiBoolean(stable_pool),
                ObjectID(self.__admin_cap)
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]]
        )

        return tx
    
    def unregister_pool_admin(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction:
        """
        Unregister a pool as admin
        
        :param pool_key: key of the pool to be unregistered by admin
        """

        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::unregister_pool_admin",
            arguments=[
                ObjectID(pool.address),
                ObjectID(self.__config.REGISTRY_ID),
                ObjectID(self.__admin_cap)
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]]
        )

        return tx
    
    def updated_allowed_versions(self, tx: SuiTransaction, pool_key: str) -> SuiTransaction :
        """
        Update the allowed versions for a pool

        :param pool_key: key of the pool to update allowed versions
        """
        
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::update_allowed_versions",
            arguments=[
                ObjectID(pool["address"]),
                ObjectID(self.__config.REGISTRY_ID),
                ObjectID(self.__admin_cap)
            ],
            type_arguments=[base_coin["type"], quote_coin["type"]]
        )

        return tx
    
    def enable_version(self, tx: SuiTransaction, version: int) -> SuiTransaction:
        """
        Enable a specific transaction

        :param version: the version to be enabled
        """
        
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::registry::enable_version",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                SuiU64(version),
                ObjectID(self.__admin_cap)
            ],
        )

        return tx
    
    def disable_version(self, tx: SuiTransaction, version: int) -> SuiTransaction:
        """
        Disable a specific transaction

        :param version: the version to be disabled
        """
        
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::registry::disable_version",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                SuiU64(version),
                ObjectID(self.__admin_cap)
            ],
        )

        return tx
    
    def set_treasury_address(self, tx: SuiTransaction, treasury_address: int) -> SuiTransaction:
        """
        Sets the treasury address where pool creation fees will be sent

        :param treasury_address: the treasury address
        """
        
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::registry::set_treasury_address",
            arguments=[
                ObjectID(self.__config.REGISTRY_ID),
                SuiAddress(treasury_address),
                ObjectID(self.__admin_cap)
            ],
        )

        return tx
    