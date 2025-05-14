"""DeepBook Python SDK"""
import json
import warnings
from typing import List

from canoser import BoolT, Uint64
from pysui import SyncClient
from pysui.sui.sui_txn import SyncTransaction

from deepbookpy.utils.normalizer import normalize_sui_address
from deepbookpy.utils.coin import format_value
from deepbookpy.utils.config import DeepBookConfig, DEEP_SCALAR, FLOAT_SCALAR
from deepbookpy.transactions.balance_manager import BalanceManagerContract
from deepbookpy.transactions.deepbook_admin import DeepBookAdminContract
from deepbookpy.transactions.deepbook import DeepBookContract
from deepbookpy.transactions.flash_loans import FlashLoanContract
from deepbookpy.transactions.governance import GovernanceContract
from deepbookpy.custom_types.serialization_types import (
    VecSet,
    Order,
    Account,
    RangeInput,
    OrderDeepPrice,
)


warnings.filterwarnings("ignore", category=DeprecationWarning)


class DeepBookClient:
    """DeepBookClient class for managing DeepBook operations"""

    def __init__(
        self,
        client: SyncClient,
        address,
        env,
        balance_managers=None,
        coins=None,
        pools=None,
        admin_cap=None,
    ):
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

    def check_manager_balance(
        self, manager_key: str, coin_key: str
    ) -> str:
        """
        Check the balance of a balance manager for a specific coin

        :param manager_key: key of the balance manager
        :param coin_key: key of the coin
        :returns: JSON string object with coin type and balance.
        """
        tx = SyncTransaction(client=self.client)

        coin = self._config.get_coin(coin_key)
        self.balance_manager.check_manager_balance(manager_key, coin_key, tx)

        result = tx.inspect_all().results
        result_bytes = result[0]["returnValues"][0][0]

        parsed_balance = Uint64.deserialize(bytes(result_bytes))
        adjusted_balance = parsed_balance / coin["scalar"]

        formatted_result = dict(
            coin_type=coin["type"], 
            balance=adjusted_balance
            )

        return json.dumps(formatted_result, indent=4)

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

    def get_quote_quantity_out(
        self, pool_key: str, base_quantity: int
    ) -> str:
        """
        Get the quote quantity out for a given base quantity

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        :returns: JSON string object with base quantity, base out, quote out, and deep required
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

        formatted_result = dict(
            base_quantity=base_quantity,
            base_out=format_value(base_out / base_scalar),
            quote_out=format_value(quote_out / quote_scalar),
            deep_required=format_value(deep_required / DEEP_SCALAR),
        )

        return json.dumps(formatted_result, indent=4)
    
    def get_base_quantity_out(
        self, pool_key: str, quote_quantity: int
    ) -> str:
        """
        Get the base quantity out for a given quote quantity

        :param pool_key: key of the pool
        :param quote_quantity: quote quantity to convert
        :returns: JSON string object with quote quantity, base out, quote out, and deep required
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]

        self.deepbook.get_base_quantity_out(pool_key, quote_quantity, tx)

        result = tx.inspect_all().results
        base_out = Uint64.deserialize(result[0]["returnValues"][0][0])
        quote_out = Uint64.deserialize(result[0]["returnValues"][1][0])
        deep_required = Uint64.deserialize(result[0]["returnValues"][2][0])

        formatted_result = dict(
            quote_quantity=quote_quantity,
            base_out=format_value(base_out / base_scalar),
            quote_out=format_value(quote_out / quote_scalar),
            deep_required=format_value(deep_required / DEEP_SCALAR),
        )

        return json.dumps(formatted_result, indent=4)

    def get_quantity_out(
        self, pool_key: str, base_quantity: int, quote_quantity: int
    ) -> str:
        """
        Get the output quantities for given base and quote quantities. Only one quantity can be non-zero

        :param pool_key: key of the pool
        :param base_quantity: base quantity to convert
        :param quote_quantity: quote quantity to convert
        :returns: JSON string object with base quantity, quote quantity, base out, quote out, and deep required
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

        formatted_result = dict(
            base_quantity=base_quantity,
            quote_quantity=quote_quantity,
            base_out=format_value(base_out / base_scalar),
            quote_out=format_value(quote_out / quote_scalar),
            deep_required=format_value(deep_required / DEEP_SCALAR),
        )

        return json.dumps(formatted_result, indent=4)

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

    def get_order(self, pool_key: str, order_id: str) -> str:
        """
        Get the order information for a specific order in a pool

        :param pool_key: key to identify pool
        :param order_id: Order ID
        :returns: JSON string object containing the order information
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.get_order(pool_key, order_id, tx)

        result = tx.inspect_all().results

        try:
            parsed_bytes = result[0]["returnValues"][0][0]
            order_info = Order.deserialize(bytes(parsed_bytes)).__dict__
            order_info["balance_manager_id"] = order_info["balance_manager_id"].to_sui_address().__dict__["address"]
            order_info["order_deep_price"] = order_info["order_deep_price"].__dict__
            return json.dumps(order_info, indent=4)
        except:
            return None

    def get_orders(self, pool_key: str, order_ids: list[str]) -> List[Order]:
        """
        Retrieves information for multiple specific orders in a pool.

        :param pool_key: key to identify pool
        :param order_ids: list of order IDs to retrieve information for
        :returns: a list with order information.
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.get_orders(pool_key, order_ids, tx)

        result = tx.inspect_all().results

        parsed_bytes = result[0]["returnValues"][0][0]

        # Each order is 99 bytes
        bytes_per_order = 99

        # Process each order
        orders = []

        # Process the first order
        if len(order_ids) >= 1:
            orders.append(Order.deserialize(parsed_bytes[:bytes_per_order]))

        # Process additional orders
        initial_pos = bytes_per_order
        for i in range(1, len(order_ids)):
            next_pos = initial_pos + bytes_per_order

            # Ensure we don't go out of bounds
            if next_pos <= len(parsed_bytes):
                order_bytes = parsed_bytes[initial_pos:next_pos]
                order_info = Order.deserialize(order_bytes)
                orders.append(order_info)
            else:
                print(f"Warning: Not enough bytes for order {i+1}")

            # Update initial_pos for the next iteration
            initial_pos = next_pos

        return orders

    def get_level2_range(
        self, pool_key: str, price_low: int, price_high: int, is_bid: bool
    ) -> str:
        """
        Get level 2 order book specifying range of price

        :param pool_key: key to identify the pool
        :param price_low: lower bound of the price range
        :param price_high: upper bound of the price range
        :param is_bid: whether to get bid or ask orders
        :returns: a JSON string object with arrays of prices and quantities
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_coin = self._config.get_coin(pool["base_coin"])
        quote_coin = self._config.get_coin(pool["quote_coin"])

        self.deepbook.get_level2_range(pool_key, price_low, price_high, is_bid, tx)

        result = tx.inspect_all().results

        prices = result[0]["returnValues"][0][0]
        parsed_prices = RangeInput.deserialize(prices).__dict__
        quantities = result[0]["returnValues"][1][0]
        parsed_quantities = RangeInput.deserialize(quantities).__dict__

        formatted_result = dict(
            prices=[
                round(
                    (float(price) / FLOAT_SCALAR / quote_coin["scalar"])
                    * base_coin["scalar"],
                    9,
                )
                for price in parsed_prices["range"]
            ],
            quantities=[
                round(float(quantity) / base_coin["scalar"], 9)
                for quantity in parsed_quantities["range"]
            ],
        )
    
        return json.dumps(formatted_result, indent=4)

    def get_level2_ticks_from_mid(self, pool_key: str, ticks: int) -> str:
        """
        Get level 2 order book ticks from mid-price for a pool

        :param pool_key: key to identify the pool
        :param ticks: lower bound of the price ranger
        :returns: JSON string object with arrays of prices and quantities
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_coin = self._config.get_coin(pool["base_coin"])
        quote_coin = self._config.get_coin(pool["quote_coin"])

        self.deepbook.get_level2_ticks_from_mid(pool_key, ticks, tx)

        result = tx.inspect_all().results

        bid_prices = result[0]["returnValues"][0][0]
        parsed_bid_prices = RangeInput.deserialize(bid_prices).__dict__

        bid_quantities = result[0]["returnValues"][1][0]
        parsed_bid_quantities = RangeInput.deserialize(bid_quantities).__dict__

        ask_prices = result[0]["returnValues"][2][0]
        parsed_ask_prices = RangeInput.deserialize(ask_prices).__dict__

        ask_quantities = result[0]["returnValues"][3][0]
        parsed_ask_quantities = RangeInput.deserialize(ask_quantities).__dict__

        formatted_result = dict(
            bid_prices=[
                round(
                    (float(price) / FLOAT_SCALAR / quote_coin["scalar"])
                    * base_coin["scalar"],
                    9,
                )
                for price in parsed_bid_prices["range"]
            ],
            bid_quantities=[
                round(float(quantity) / base_coin["scalar"], 9)
                for quantity in parsed_bid_quantities["range"]
            ],
            ask_prices=[
                round(
                    (float(price) / FLOAT_SCALAR / quote_coin["scalar"])
                    * base_coin["scalar"],
                    9,
                )
                for price in parsed_ask_prices["range"]
            ],
            ask_quantities=[
                round(float(quantity) / base_coin["scalar"], 9)
                for quantity in parsed_ask_quantities["range"]
            ],
        )
    
        return json.dumps(formatted_result, indent=4)

    def account(self, pool_key: str, manager_key: str) -> str:
        """
        Get the account information for a given pool and balance manager

        :param pool_key: key of the pool
        :param manager_key: key of the BalanceManager
        :returns: JSON string object containing the account information
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]

        self.deepbook.account(pool_key, manager_key, tx)

        result = tx.inspect_all().results

        final_results = result[0]["returnValues"][0][0]

        account = Account.deserialize(final_results)

        formatted_result = dict(
            epoch=account.epoch,
            open_orders=account.open_orders.__dict__,
            taker_volume=format_value(account.taker_volume / base_scalar),
            maker_volume=format_value(account.maker_volume / base_scalar),
            active_stake=format_value(account.active_stake / DEEP_SCALAR),
            inactive_stake=format_value(account.inactive_stake / DEEP_SCALAR),
            created_proposal=account.created_proposal,
            voted_proposal=dict(account.voted_proposal.__dict__)["value"],
            unclaimed_rebates=dict(
                base=format_value(account.unclaimed_rebates.base / base_scalar),
                quote=format_value(account.unclaimed_rebates.quote / quote_scalar),
                deep=format_value(account.unclaimed_rebates.deep / DEEP_SCALAR),
            ),
            settled_balances=dict(
                base=format_value(account.settled_balances.base / base_scalar),
                quote=format_value(account.settled_balances.quote / quote_scalar),
                deep=format_value(account.settled_balances.deep / DEEP_SCALAR),
            ),
            owed_balances=dict(
                base=format_value(account.owed_balances.base / base_scalar),
                quote=format_value(account.owed_balances.quote / quote_scalar),
                deep=format_value(account.owed_balances.deep / DEEP_SCALAR),
            ),
        )

        return json.dumps(formatted_result, indent=4)

    def get_order_normalized(self, pool_key: str, order_id: str) -> str:
        """
        Get the order information for a specific order in a pool, with normalized price

        :param pool_key: key to identify pool
        :param order_id: Order ID
        :returns: JSON string object containing the order information with normalized price
        """

        tx = SyncTransaction(client=self.client)

        self.deepbook.get_order(pool_key, order_id, tx)

        result = tx.inspect_all().results

        parsed_bytes = result[0]["returnValues"][0][0]

        order = Order.deserialize(bytearray(parsed_bytes))
        order_info = order.__dict__

        order_info["balance_manager_id"] = order_info["balance_manager_id"].to_sui_address().__dict__["address"]

        if not order_info:
            return None

        base_coin = self._config.get_coin(self._config.get_pool(pool_key)["base_coin"])
        quote_coin = self._config.get_coin(self._config.get_pool(pool_key)["base_coin"])

        decoded = self.decode_order_id(int(order_info["order_id"]))
        is_bid = decoded["is_bid"]
        raw_price = decoded["price"]

        normalized_price = format_value(
            (raw_price * base_coin["scalar"]) / quote_coin["scalar"] / FLOAT_SCALAR
        )

        order_info["quantity"] = str(format_value(order_info["quantity"]) / base_coin["scalar"])
        order_info["filled_quantity"] = str(format_value(
            float(order_info["filled_quantity"]) / base_coin["scalar"]
        ))

        order_info["order_deep_price"].__dict__["deep_per_asset"] = str(format_value(
            float(order_info["order_deep_price"].__dict__["deep_per_asset"])
            / DEEP_SCALAR
        ))

        order_info["order_deep_price"] = order_info["order_deep_price"].__dict__
        order_info["is_bid"] = is_bid
        order_info["normalized_price"] = normalized_price

        return json.dumps(order_info, indent=4)
    
    def decode_order_id(self, encoded_order_id: int) -> dict:
        """
        Decode the order ID to get bid/ask status, price, and orderId

        :param encoded_order_id: Encoded order ID
        :returns: dictionary object
        """
        is_bid = (encoded_order_id >> 127) == 0
        price = (encoded_order_id >> 64) & ((1 << 63) - 1)
        order_id = encoded_order_id & ((1 << 64) - 1)

        return dict(is_bid=is_bid, price=price, order_id=order_id)

    def vault_balances(self, pool_key: str) -> str:
        """
        Get the vault balances for a pool

        :param pool_key: key to identify the pool
        :returns: JSON string object with base, quote, and deep balances in the vault
        """
        tx = SyncTransaction(client=self.client)

        pool = self._config.get_pool(pool_key)
        base_coin_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_coin_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]

        self.deepbook.vault_balances(pool_key, tx)

        result = tx.inspect_all().results

        base_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        quote_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        deep_in_vault = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        formatted_result = dict(
            base=format_value(base_in_vault / base_coin_scalar),
            quote=format_value(quote_in_vault / quote_coin_scalar),
            deep=format_value(deep_in_vault),
        )
        
        return json.dumps(formatted_result, indent=4)

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

        base_coin = self._config.get_coin(pool["base_coin"])
        quote_coin = self._config.get_coin(pool["quote_coin"])

        result = tx.inspect_all().results

        parsed_bytes = bytes(result[0]["returnValues"][0][0])

        parsed_mid_price = Uint64.deserialize(parsed_bytes)

        adjusted_mid_price = (
            (parsed_mid_price * base_coin["scalar"])
            / quote_coin["scalar"]
            / FLOAT_SCALAR
        )

        return adjusted_mid_price

    def pool_trade_params(self, pool_key: str) -> str:
        """
        Get the trade parameters for a given pool, including taker fee, maker fee, and stake required

        :param pool_key: key of the pool
        :returns: JSON string object with pool trade results
        """
        tx = SyncTransaction(client=self.client)

        self.deepbook.pool_trade_params(pool_key, tx)

        result = tx.inspect_all().results

        taker_fee = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        maker_fee = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        stake_required = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        formatted_result = dict(
                taker_fee=format_value(taker_fee / FLOAT_SCALAR),
                maker_fee=format_value(maker_fee / FLOAT_SCALAR),
                stake_required=format_value(stake_required / DEEP_SCALAR),
            )

        return json.dumps(formatted_result, indent=4)

    def pool_book_params(self, pool_key: str) -> str:
        """
        Get the trade parameters for a given pool, including tick size, lot size, and min size.

        :param pool_key: key of the pool
        :returns: a JSON string object with pool book results
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]
        self.deepbook.pool_book_params(pool_key, tx)

        result = tx.inspect_all().results

        tick_size = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        lot_size = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        min_size = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        formatted_result = dict(
            tick_size=format_value((tick_size * base_scalar) / quote_scalar / FLOAT_SCALAR),
            lot_size=format_value(lot_size / base_scalar),
            min_size=format_value(min_size / base_scalar),
        )

        return json.dumps(formatted_result, indent=4)

    def locked_balance(
        self, pool_key: str, balance_manager_key: str
    ) -> str:
        """
        Get the locked balances for a pool and balance manager

        :param pool_key: key of the pool
        :param balance_manager_key: key of the BalanceManager
        :returns: JSON string object with base, quote, and deep locked for the balance manager in the pool
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_scalar = self._config.get_coin(pool["base_coin"])["scalar"]
        quote_scalar = self._config.get_coin(pool["quote_coin"])["scalar"]

        self.deepbook.locked_balance(pool_key, balance_manager_key, tx)

        result = tx.inspect_all().results

        base_locked = Uint64.deserialize(bytes(result[0]["returnValues"][0][0]))
        quote_locked = Uint64.deserialize(bytes(result[0]["returnValues"][1][0]))
        deep_locked = Uint64.deserialize(bytes(result[0]["returnValues"][2][0]))

        formatted_result = dict(
            base=format_value(base_locked / base_scalar),
            quote=format_value(quote_locked / quote_scalar),
            deep=format_value(deep_locked / DEEP_SCALAR),
        )

        return json.dumps(formatted_result, indent=4)

    def get_pool_deep_price(self, pool_key: str) -> str:
        """
        Get the DEEP price conversion for a pool

        :param pool_key: key of the pool
        :returns: JSON string object with deep price conversion
        """
        tx = SyncTransaction(client=self.client)
        pool = self._config.get_pool(pool_key)
        base_coin = self._config.get_coin(pool["base_coin"])
        quote_coin = self._config.get_coin(pool["quote_coin"])

        deep_coin = self._config.get_coin("DEEP")

        self.deepbook.get_pool_deep_price(pool_key, tx)

        result = tx.inspect_all().results

        pool_deep_price = OrderDeepPrice.deserialize(
            bytes(result[0]["returnValues"][0][0])
        )

        if pool_deep_price.asset_is_base:
            return json.dumps(dict(
                asset_is_base=pool_deep_price.asset_is_base,
                deep_per_base=(
                    (pool_deep_price.deep_per_asset / FLOAT_SCALAR)
                    * base_coin["scalar"]
                )
                / deep_coin["scalar"],
            ), indent=4)
        else:
            return json.dumps(dict(
                asset_is_base=pool_deep_price.asset_is_base,
                deep_per_quote=(
                    (pool_deep_price.deep_per_asset / FLOAT_SCALAR)
                    * quote_coin["scalar"]
                )
                / deep_coin["scalar"],
            ), indent=4)
