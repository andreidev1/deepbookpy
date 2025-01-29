from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class BalanceManagerContract:
    def __init__(self, config: DeepBookConfig):
        """
         BalanceManagerContract class for managing BalanceManager operations

       
        :param config: Configuration for BalanceManagerContract
        """
        self.__config = config
