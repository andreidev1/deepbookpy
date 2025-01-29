from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class DeepBookAdminContract:
    def __init__(self, config: DeepBookConfig):
        """
        DeepBookAdminContract class for managing admin actions.

       
        :param config: Configuration for DeepBookAdminContract
        """
        self.__config = config


    def __admin_cap(self):
        """
        Returns the admin capability required for admin operations.
        """
        
        admin_cap = self.__config.admin_cap
        if not admin_cap:
            raise EnvironmentError('ADMIN_CAP environment variable not set')
        return admin_cap

    def create_pool_admin(self, tx: SuiTransaction, params) -> SuiTransaction: 
        base_coin_key = params[""]
        quote_coin_key = params[""]
        base_coin = self.__config.get_coin(base_coin_key)
        quote_coin = self.__config.get_coin(quote_coin_key)

        tx.move_call(
            target="",
            arguments=[],
            type_arguments=[]
        )

        return tx