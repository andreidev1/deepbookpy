"""DeepBook Python SDK"""
import math
from typing import List

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.common import handle_result
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.event_filter import MoveEventTypeQuery
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui.sui.sui_builders.exec_builders import InspectTransaction
from pysui.sui.sui_builders.get_builders import QueryEvents


from deepbookpy.utils.normalizer import normalize_sui_object_id, normalize_sui_address
from deepbookpy.utils.constants import CLOB, CREATION_FEE
from deepbookpy.utils.helpers import parse_struct


class DeepBookClient:
    """DeepBookClient class for managing DeepBook operations"""

   def __init__(self, client, address, env, balance_managers=None, coins=None, pools=None, admin_cap=None):
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
