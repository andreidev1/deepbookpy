"""DeepBook Python SDK"""
from typing import List

from canoser import BoolT

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.common import handle_result
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.event_filter import MoveEventTypeQuery
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui.sui.sui_builders.exec_builders import InspectTransaction
from pysui.sui.sui_builders.get_builders import QueryEvents
from pysui import SuiConfig, SyncClient
from pysui.sui.sui_txn import SyncTransaction


from utils.normalizer import normalize_sui_address
from utils.config import DeepBookConfig
from transactions.balance_manager import BalanceManagerContract
from transactions.deepbook_admin import DeepBookAdminContract
from transactions.deepbook import DeepBookContract
from transactions.flash_loans import FlashLoanContract
from transactions.governance import GovernanceContract


class DeepBookClient:

    """DeepBookClient class for managing DeepBook operations"""

    def __init__(self, client: SuiClient, address, env, balance_managers=None, coins=None, pools=None, admin_cap=None):
        """
        Initializes the DeepBookClient class.

        :param client: SuiClient instance
        :param address: Address of the client
        :param env: Environment configuration
        :param balance_managers: Optional initial balance managers map
        :param coins: Optional initial coin map
        :param pools: Optional initial pool map
        :param admin_cap: Optional admin capability
        """
        self.client = client
        self._address = normalize_sui_address(address)
        self._config = DeepBookConfig(
            address=self._address,
            env=env,
            balance_managers=balance_managers,
            coins=coins,
            pools=pools,
            admin_cap=admin_cap,
        )
        self.balance_manager = BalanceManagerContract(self._config)
        self.deep_book = DeepBookContract(self._config)
        self.deep_book_admin = DeepBookAdminContract(self._config)
        self.flash_loans = FlashLoanContract(self._config)
        self.governance = GovernanceContract(self._config)


    def check_manager_balance(self, tx: SuiTransaction, manager_key: str, coin_key: str):
        """
        Check the balance of a balance manager for a specific coin

        :param manager_key: key of the balance manager
        :param coin_key: key of the coin
        """
        #res = self.client.devInspect
        pass

    def whitelisted(self, tx: SuiTransaction, pool_key: str):
        """
        Check if pool is whitelisted

        :param pool_key: key of the pool
        """

        result = tx.inspect_all(self.deep_book.whitelisted(tx, pool_key))
        result = self.deep_book.whitelisted(pool_key, tx)
        result_bytes = result[0]["returnValues"][0][0]

        whitelisted = BoolT.deserialize(bytes(result_bytes))

        return whitelisted 
    
