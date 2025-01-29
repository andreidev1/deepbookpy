from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class FlashLoanContract:
    def __init__(self, config: DeepBookConfig):
        """
        FlashLoanContract class for managing flash loans.

       
        :param config: Configuration object for DeepBook
        """
        self.__config = config
