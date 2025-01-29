from deepbookpy.utils.config import DeepBookConfig
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


class GovernanceContract:
    def __init__(self, config: DeepBookConfig):
        """
        GovernanceContract class for managing governance operations in DeepBook

       
        :param config: Configuration for GovernanceContract
        """
        self.__config = config
