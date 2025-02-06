"""DeepBook Python SDK"""
import warnings
from typing import List
import json

from canoser import BoolT, Uint64, Struct, BytesT, Uint128, Uint8

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.common import handle_result
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui import SyncClient
from pysui.sui.sui_txn import SyncTransaction


from deepbookpy.utils.normalizer import normalize_sui_address
from deepbookpy.utils.config import DeepBookConfig, DEEP_SCALAR
from deepbookpy.transactions.balance_manager import BalanceManagerContract
from deepbookpy.transactions.deepbook_admin import DeepBookAdminContract
from deepbookpy.transactions.deepbook import DeepBookContract
from deepbookpy.transactions.flash_loans import FlashLoanContract
from deepbookpy.transactions.governance import GovernanceContract
from deepbookpy.custom_types.serialization_types import VecSet, Order

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
    
    def get_quote_quantity_out(self, pool_key: str, base_quantity: int):
        """
        Get the quote quantity out for a given base quantity

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar =self._config.get_coin(pool["quote_coin"])["scalar"]


        self.deepbook.get_quote_quantity_out(pool_key, base_quantity, tx)

        result = tx.inspect_all().results
        base_out = Uint64.deserialize(result[0]["returnValues"][0][0])
        quote_out = Uint64.deserialize(result[0]["returnValues"][1][0])
        deep_required = Uint64.deserialize(result[0]["returnValues"][2][0])

        return dict(
            base_quantity=base_quantity, 
            base_out=float(base_out / base_scalar), 
            quote_out=float(quote_out / quote_scalar), 
            deep_required=float(deep_required / DEEP_SCALAR)
            ) 
    
    def get_base_quantity_out(self, pool_key: str, quote_quantity: int):
        """
        Get the base quantity out for a given quote quantity

        :param pool_key: key of the pool
        :param quote_quantity: quote quantity to convert
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar =self._config.get_coin(pool["quote_coin"])["scalar"]


        self.deepbook.get_base_quantity_out(pool_key, quote_quantity, tx)

        result = tx.inspect_all().results
        base_out = Uint64.deserialize(result[0]["returnValues"][0][0])
        quote_out = Uint64.deserialize(result[0]["returnValues"][1][0])
        deep_required = Uint64.deserialize(result[0]["returnValues"][2][0])

        return dict(
            quote_quantity=quote_quantity, 
            base_out=float(base_out / base_scalar), 
            quote_out=float(quote_out / quote_scalar), 
            deep_required=float(deep_required / DEEP_SCALAR)
            )
    
    def get_quantity_out(self, pool_key: str, base_quantity: int, quote_quantity: int):
        """
        Get the output quantities for given base and quote quantities. Only one quantity can be non-zero

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        :param quote_quantity: quote quantity to convert
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]


        self.deepbook.get_quantity_out(pool_key, base_quantity, quote_quantity, tx)

        result = tx.inspect_all().results
        base_out = Uint64.deserialize(result[0]["returnValues"][0][0])
        quote_out = Uint64.deserialize(result[0]["returnValues"][1][0])
        deep_required = Uint64.deserialize(result[0]["returnValues"][2][0])

        return dict(
            base_quantity=base_quantity,
            quote_quantity=quote_quantity, 
            base_out=float(base_out / base_scalar), 
            quote_out=float(quote_out / quote_scalar), 
            deep_required=float(deep_required / DEEP_SCALAR)
            )
    
    def account_open_orders(self, pool_key: str, manager_key: str):
        """
        Get open orders for a balance manager in a pool

        :param pool_key: key of the pool
        :param manager_key: key of BalanceManager
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.account_open_orders(pool_key, manager_key, tx)

        result = tx.inspect_all().results
        order_ids = result[0]["returnValues"][0][0]

        deserialized_data = VecSet.deserialize(bytes(order_ids))

        return deserialized_data.__dict__["constants"]

    def get_order(self, pool_key: str, order_id: str):
        """
        Get the order information for a specific order in a pool

        :param pool_key: key to identify pool
        :param order_id: Order ID
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.get_order(pool_key, order_id, tx)

        result = tx.inspect_all().results

        try:
            parsed_bytes = result[0]["returnValues"][0][0]
            order_info = Order.deserialize(bytes(parsed_bytes))
            return order_info
        except:
            return None

