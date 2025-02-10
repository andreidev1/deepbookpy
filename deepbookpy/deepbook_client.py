"""DeepBook Python SDK"""
import warnings
from typing import Any, Dict, List

from canoser import BoolT, Uint64
from pysui import SyncClient
from pysui.sui.sui_txn import SyncTransaction

from deepbookpy.utils.normalizer import normalize_sui_address
from deepbookpy.utils.config import DeepBookConfig, DEEP_SCALAR, FLOAT_SCALAR
from deepbookpy.transactions.balance_manager import BalanceManagerContract
from deepbookpy.transactions.deepbook_admin import DeepBookAdminContract
from deepbookpy.transactions.deepbook import DeepBookContract
from deepbookpy.transactions.flash_loans import FlashLoanContract
from deepbookpy.transactions.governance import GovernanceContract
from deepbookpy.custom_types.serialization_types import VecSet, Order, ID, Account, OrderDeepPrice


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


    def check_manager_balance(self, manager_key: str, coin_key: str) -> Dict[str, float]:
        """
        Check the balance of a balance manager for a specific coin

        :param manager_key: key of the balance manager
        :param coin_key: key of the coin
        :returns: a dictionary with coin type and balance.
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
        :returns: a boolean that indicates the whitelisted pool status
        """
        tx = SyncTransaction(client=self.client)
        self.deepbook.whitelisted(pool_key, tx)

        result = tx.inspect_all().results
        result_bytes = result[0]["returnValues"][0][0]

        whitelisted = BoolT.deserialize(bytes(result_bytes))

        return whitelisted 
    
    def get_quote_quantity_out(self, pool_key: str, base_quantity: int) -> Dict[str, float]:
        """
        Get the quote quantity out for a given base quantity

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        :returns: dictionary object with base quantity, base out, quote out, and deep required
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]


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
    
    def get_base_quantity_out(self, pool_key: str, quote_quantity: int) -> Dict[str, float]:
        """
        Get the base quantity out for a given quote quantity

        :param pool_key: key of the pool
        :param quote_quantity: quote quantity to convert
        :returns: a dictionary object with quote quantity, base out, quote out, and deep required
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
    
    def get_quantity_out(self, pool_key: str, base_quantity: int, quote_quantity: int) -> Dict[str, float]:
        """
        Get the output quantities for given base and quote quantities. Only one quantity can be non-zero

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        :param quote_quantity: quote quantity to convert
        :returns: a dictionary object with base quantity, quote quantity, base out, quote out, and deep required
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
    
    def account_open_orders(self, pool_key: str, manager_key: str) -> List[int]:
        """
        Get open orders for a balance manager in a pool

        :param pool_key: key of the pool
        :param manager_key: key of BalanceManager
        :returns: an array with open orders
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.account_open_orders(pool_key, manager_key, tx)

        result = tx.inspect_all().results
        order_ids = result[0]["returnValues"][0][0]

        deserialized_data = VecSet.deserialize(bytes(order_ids))

        return deserialized_data.__dict__["constants"]

    def get_order(self, pool_key: str, order_id: str) -> List[Any]:
        """
        Get the order information for a specific order in a pool

        :param pool_key: key to identify pool
        :param order_id: Order ID
        :returns: object containing the order information
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

    def get_order_normalized(self, pool_key: str, order_id: str) -> Dict[str, Any]:
        """
        Get the order information for a specific order in a pool, with normalized price

        :param pool_key: key to identify pool
        :param order_id: Order ID
        :returns: a dictionary object containing the order information with normalized price
        """

        tx = SyncTransaction(client=self.client)

        self.deepbook.get_order(pool_key, order_id, tx)

        result = tx.inspect_all().results
        
        parsed_bytes = result[0]["returnValues"][0][0]
    
        order = Order.deserialize(bytearray(parsed_bytes))
        order_info = order.__dict__

        if not order_info:
            return None
        
        base_coin = self._config.get_coin(self._config.get_pool(pool_key)["base_coin"])
        quote_coin = self._config.get_coin(self._config.get_pool(pool_key)["base_coin"])

        decoded = self.decode_order_id(int(order_info["order_id"]))
        is_bid = decoded['is_bid']
        raw_price = decoded['price']
        normalized_price = (raw_price * base_coin["scalar"]) / quote_coin["scalar"] / FLOAT_SCALAR

        order_info["quantity"] = float(order_info["quantity"]) / base_coin["scalar"]
        order_info["filled_quantity"] = float(order_info["filled_quantity"]) / base_coin["scalar"]
        order_info["order_deep_price"].__dict__["deep_per_asset"] = float(order_info["order_deep_price"].__dict__["deep_per_asset"]) / DEEP_SCALAR
        order_info['is_bid'] = is_bid
        order_info['normalized'] = normalized_price

        return order_info
        
    
    def decode_order_id(self, encoded_order_id: int) -> dict:
        """
        Decode the order ID to get bid/ask status, price, and orderId

        :param encoded_order_id: Encoded order ID
        :returns: dictionary object
        """
        is_bid = (encoded_order_id >> 127) == 0
        price = (encoded_order_id >> 64) & ((1 << 63) - 1)
        order_id = encoded_order_id & ((1 << 64) - 1)

        return dict(
            is_bid=is_bid,
            price=price,
            order_id=order_id
        )

    def vault_balances(self, pool_key: str) -> Dict[str, float]:
        """
        Get the vault balances for a pool

        :param pool_key: key to identify the pool
        :returns: a dictionary object with base, quote, and deep balances in the vault
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_coin_scalar = self._config.get_coin(pool['base_coin'])["scalar"]
        quote_coin_scalar = self._config.get_coin(pool['quote_coin'])["scalar"]

        self.deepbook.vault_balances(pool_key, tx)

        result = tx.inspect_all().results

        base_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        quote_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        deep_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        return dict(base=float(base_in_vault / base_coin_scalar), quote=float(quote_in_vault / quote_coin_scalar), deep=float(deep_in_vault))
    
    def get_pool_id_by_assets(self, base_type: str, quote_type: str) -> str:
        """
        Get the pool ID by asset types

        :param base_type: type of the base asset
        :param quote_type: type of the quote asset
        :returns: address of the pool
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.get_pool_id_by_assets(base_type, quote_type, tx)

        result = tx.inspect_all().results

        return "0x" + (bytes(result[0]["returnValues"][0][0])).hex()
    
    def mid_price(self, pool_key: str) -> float:
        """
        Get the mid price for a pool

        :param pool_key: key of the pool
        :returns: mid price
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        self.deepbook.mid_price(pool_key, tx)

        base_coin = self._config.get_coin(pool['base_coin'])
        quote_coin = self._config.get_coin(pool['quote_coin'])

        result = tx.inspect_all().results

        parsed_bytes = bytes(result[0]["returnValues"][0][0])

        parsed_mid_price = Uint64.deserialize(parsed_bytes)
        adjusted_mid_price = (parsed_mid_price * base_coin["scalar"]) / quote_coin["scalar"] / FLOAT_SCALAR

        return adjusted_mid_price
    
    def pool_trade_params(self, pool_key: str) -> Dict[str, float]:
        """
        Get the trade parameters for a given pool, including taker fee, maker fee, and stake required

        :param pool_key: key of the pool
        :returns: a dictionary with pool trade results
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.pool_trade_params(pool_key, tx)

        result = tx.inspect_all().results

        taker_fee = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        maker_fee = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        stake_required = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        return dict(
            taker_fee=taker_fee / FLOAT_SCALAR,
            maker_fee=maker_fee / FLOAT_SCALAR,
            stake_required=stake_required / DEEP_SCALAR
        )
    
    def pool_book_params(self, pool_key: str) -> Dict[str, float]:
        """
        Get the trade parameters for a given pool, including tick size, lot size, and min size.

        :param pool_key: key of the pool
        :returns: a dictionary with pool book results
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool['base_coin'])["scalar"]
        quote_scalar = self._config.get_coin(pool['quote_coin'])["scalar"]
        self.deepbook.pool_book_params(pool_key, tx)

        result = tx.inspect_all().results

        tick_size = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        lot_size = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        min_size = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        return dict(
            tick_size=(tick_size * base_scalar) / quote_scalar / FLOAT_SCALAR,
            lot_size=lot_size / base_scalar,
            min_size=min_size / base_scalar
        )
    
    def locked_balance(self, pool_key: str, balance_manager_key: str) -> Dict[str, float]:
        """
        Get the locked balances for a pool and balance manager

        :param pool_key: key of the pool
        :param balance_manager_key: key of the BalanceManager
        :returns: a dictionary object with base, quote, and deep locked for the balance manager in the pool
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool['base_coin'])["scalar"]
        quote_scalar = self._config.get_coin(pool['quote_coin'])["scalar"]

        self.deepbook.locked_balance(pool_key, balance_manager_key, tx)

        result = tx.inspect_all().results

        base_locked = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        quote_locked = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        deep_locked = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        return dict(
            base=base_locked / base_scalar,
            quote=quote_locked / quote_scalar,
            deep=deep_locked / DEEP_SCALAR
        )
    
    def get_pool_deep_price(self, pool_key: str) -> Dict[str, float]:
        """
        Get the DEEP price conversion for a pool

        :param pool_key: key of the pool
        :returns: a dictionary with deep price conversion
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_coin = self._config.get_coin(pool['base_coin'])
        quote_coin = self._config.get_coin(pool['quote_coin'])

        deep_coin = self._config.get_coin("DEEP")

        self.deepbook.get_pool_deep_price(pool_key, tx)

        result = tx.inspect_all().results

        pool_deep_price = OrderDeepPrice.deserialize(bytes(result[0]["returnValues"][0][0]))
        
        if(pool_deep_price.asset_is_base):
            return dict(
                asset_is_base=pool_deep_price.asset_is_base, 
                deep_per_base=((pool_deep_price.deep_per_asset / FLOAT_SCALAR) * base_coin["scalar"]) / deep_coin["scalar"]
                )
        else:
            return dict(
                asset_is_base=pool_deep_price.asset_is_base,
                deep_per_quote=((pool_deep_price.deep_per_asset / FLOAT_SCALAR) * quote_coin["scalar"]) / deep_coin["scalar"]
                )
