from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class BalanceManagerContract:
    def __init__(self, config: DeepBookConfig):
        """
         BalanceManagerContract class for managing BalanceManager operations

       
        :param config: Configuration for BalanceManagerContract
        """
        self.__config = config

    def generate_proof(self, tx: SuiTransaction, manager_key: str) -> SuiTransaction:
        """
        Generate a trade proof for the BalanceManager. Calls the appropriate function based on whether tradeCap is set.

        :param manager_key: key of the BalanceManagerr
        """

        balance_manager = self.__config.get_balance_manager(manager_key)

        