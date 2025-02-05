"""DeepBook Python SDK"""
import warnings
from typing import List

from canoser import BoolT, Uint64

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.common import handle_result
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui import SyncClient
from pysui.sui.sui_txn import SyncTransaction


from deepbookpy.utils.normalizer import normalize_sui_address
from deepbookpy.utils.config import DeepBookConfig
from deepbookpy.transactions.balance_manager import BalanceManagerContract
from deepbookpy.transactions.deepbook_admin import DeepBookAdminContract
from deepbookpy.transactions.deepbook import DeepBookContract
from deepbookpy.transactions.flash_loans import FlashLoanContract
from deepbookpy.transactions.governance import GovernanceContract

warnings.filterwarnings("ignore", category=DeprecationWarning) 
class DeepBookClient:

    """DeepBookClient class for managing DeepBook operations"""

    def __init__(self, client: SyncClient, address, env, balance_managers=None, coins=None, pools=None, admin_cap=None):
        """
        Initializes the DeepBookClient class.

        :param client: SyncClient instance
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
        self.deepbook = DeepBookContract(self._config)
        self.deepbook_admin = DeepBookAdminContract(self._config)
        self.flash_loans = FlashLoanContract(self._config)
        self.governance = GovernanceContract(self._config)


    def check_manager_balance(self, manager_key: str, coin_key: str):
        """
        Check the balance of a balance manager for a specific coin

        :param manager_key: key of the balance manager
        :param coin_key: key of the coin
        """
        tx = SyncTransaction(client=self.client)

        coin = self._config.get_coin(coin_key)
        self.balance_manager.check_manager_balance(manager_key, coin_key, tx)

        result = tx.inspect_all().results
        result_bytes = result[0]["returnValues"][0][0]

        parsed_balance = Uint64.deserialize(bytes(result_bytes))
        adjusted_balance = parsed_balance / coin["scalar"]

        return dict(coin_type=coin["type"], balance=adjusted_balance)

    def whitelisted(self, pool_key: str) -> bool:
        """
        Check if pool is whitelisted

        :param pool_key: key of the pool
        """
        tx = SyncTransaction(client=self.client)
        self.deepbook.whitelisted(pool_key, tx)

        result = tx.inspect_all().results
        result_bytes = result[0]["returnValues"][0][0]

        whitelisted = BoolT.deserialize(bytes(result_bytes))

        return whitelisted 
    
