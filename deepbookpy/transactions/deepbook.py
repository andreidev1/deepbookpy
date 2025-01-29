from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class DeepBookContract:
    def __init__(self, config: DeepBookConfig):
        """
        DeepBookContract class for managing DeepBook operations

       
        :param config: Configuration for DeepBookContract
        """
        self.__config = config
