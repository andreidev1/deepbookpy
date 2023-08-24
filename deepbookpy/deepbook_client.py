"""DeepBook Python SDK"""
import math
from typing import List

from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.event_filter import MoveEventTypeQuery
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui.sui.sui_builders.exec_builders import InspectTransaction
from pysui.sui.sui_builders.get_builders import QueryEvents
from pysui.sui.sui_clients.common import handle_result


from deepbookpy.utils.normalizer import normalize_sui_object_id
from deepbookpy.utils.constants import CLOB, CREATION_FEE
from deepbookpy.utils.helpers import parse_struct


class DeepBookClient:
    """Write data to DeepBook package"""

    def __init__(self, client: SuiClient, package_id: str):
        self.client = client
        self.package_id = package_id

    def create_pool(
        self, base_asset: str, quote_asset: str, tick_size: int, lot_size: int
    ) -> SuiTransaction:
        """
        Create pool for trading pair - 100 Sui fee

        :param base_asset:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"

        :param quote_asset:
            Full coin type of quote asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::usdt::USDT"

        :param tick_size:
            Minimal Price Change Accuracy of this pool, eg: 10000000

        :param lot_size:
            Minimal Lot Change Accuracy of this pool, eg: 10000
        """

        txer = SuiTransaction(self.client)

        splits: list = txer.split_coin(coin=txer.gas, amounts=[CREATION_FEE])

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::create_pool",
            arguments=[SuiU64(str(tick_size)), SuiU64(str(lot_size)), splits],
            type_arguments=[base_asset, quote_asset],
        )
        return txer
    
    def create_customized_pool(
        self, base_asset: str, quote_asset: str, tick_size: int, lot_size: int, taker_fee_rate: int, maker_rebate_rate: int
    ) -> SuiTransaction:
        """
        Create customized pool

        :param base_asset:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"

        :param quote_asset:
            Full coin type of quote asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::usdt::USDT"

        :param tick_size:
            Minimal Price Change Accuracy of this pool, eg: 10000000

        :param lot_size:
            Minimal Lot Change Accuracy of this pool, eg: 10000
        
        :param taker_fee_rate:
            Customized taker fee rate, float scaled by `FLOAT_SCALING_FACTOR`, Taker_fee_rate of 0.25% should be 2_500_000 for example
        
        :param maker_rebate_rate:
            Customized Customized maker rebate rate, float scaled by `FLOAT_SCALING_FACTOR`,  should be less than or equal to the taker_rebate_rate
        """

        txer = SuiTransaction(self.client)

        splits: list = txer.split_coin(coin=txer.gas, amounts=[CREATION_FEE])

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::create_customized_pool",
            arguments=[SuiU64(str(tick_size)), SuiU64(str(lot_size)), SuiU64(str(taker_fee_rate)), SuiU64(str(maker_rebate_rate)), splits],
            type_arguments=[base_asset, quote_asset],
        )
        return txer

    def create_account(self, current_address: SuiAddress) -> SuiTransaction:
        """
        Create and Transfer custodian account to user

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"
        """

        txer = SuiTransaction(self.client)

        cap: list = txer.move_call(
            target=f"{self.package_id}::{CLOB}::create_account",
            arguments=[],
            type_arguments=[],
        )

        txer.transfer_objects(transfers=[cap], recipient=SuiAddress(current_address))

        return txer

    def create_child_account_cap(self, current_address: SuiAddress) -> SuiTransaction:
        """
        Create and Transfer child custodian account to user

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"
        """

        txer = SuiTransaction(self.client)

        child_cap: list = txer.move_call(
            target=f"{self.package_id}::{CLOB}::create_child_account_cap",
            arguments=[],
            type_arguments=[ObjectID(current_address)],
        )

        txer.transfer_objects(transfers=[child_cap], recipient=SuiAddress(current_address))

        return txer

    def deposit_base(self, pool_id: str, coin: str, account_cap: str) -> SuiTransaction:
        """
        Deposit base asset into custodian account

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param coin:
            Object id of coin to deposit, eg: "0x316467544c7e719384579ac5745c75be5984ca9f004d6c09fd7ca24e4d8a3d14"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::deposit_base",
            arguments=[ObjectID(pool_id), ObjectID(coin), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer

    def deposit_quote(
        self, pool_id: str, coin: str, account_cap: str
    ) -> SuiTransaction:
        """
        Deposit quote asset into custodian account

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param coin:
            Object id of coin to deposit, eg: "0x316467544c7e719384579ac5745c75be5984ca9f004d6c09fd7ca24e4d8a3d14"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::deposit_quote",
            arguments=[ObjectID(pool_id), ObjectID(coin), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer

    def withdraw_base(
        self,
        pool_id: str,
        quantity: int,
        current_address: SuiAddress,
        account_cap: str,
    ) -> SuiTransaction:
        """
        Withdraw base asset from custodian account

        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param quantity:
            Amount of base asset to withdraw, eg: 10000000

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """

        txer = SuiTransaction(self.client)

        withdraw = txer.move_call(
            target=f"{self.package_id}::{CLOB}::withdraw_base",
            arguments=[ObjectID(pool_id), SuiU64(quantity), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        txer.transfer_objects(
            transfers=[withdraw], recipient=SuiAddress(current_address)
        )

        return txer

    def withdraw_quote(
        self,
        pool_id: str,
        quantity: int,
        current_address: SuiAddress,
        account_cap: str,
    ) -> SuiTransaction:
        """
        Withdraw quote asset from custodian account

        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param quantity:
            Amount of base asset to withdraw, eg: 10000000

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """

        txer = SuiTransaction(self.client)

        withdraw = txer.move_call(
            target=f"{self.package_id}::{CLOB}::withdraw_quote",
            arguments=[ObjectID(pool_id), SuiU64(quantity), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        txer.transfer_objects(
            transfers=[withdraw], recipient=SuiAddress(current_address)
        )

        return txer

    def swap_exact_quote_for_base(
        self,
        pool_id: str,
        token_object_in: str,
        amount_in: int,
        current_address: SuiAddress,
        client_order_id: str,
    ) -> SuiTransaction:
        """
        Swap exact quote for base

        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param token_object_in:
            Object id of the token to swap: eg: "0x6e566fec4c388eeb78a7dab832c9f0212eb2ac7e8699500e203def5b41b9c70d"

        :param amount_in:
            Amount of token to buy or sell, eg: 10000000

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"
        """

        txer = SuiTransaction(self.client)

        [base_coin_ret, quote_coin_ret, _amount] = txer.move_call(
            target=f"{self.package_id}::{CLOB}::swap_exact_quote_for_base",
            arguments=[
                ObjectID(pool_id),
                SuiU64(client_order_id),
                SuiU64(amount_in),
                ObjectID(normalize_sui_object_id("0x6")),
                ObjectID(token_object_in),
            ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        txer.transfer_objects(
            transfers=[base_coin_ret], recipient=SuiAddress(current_address)
        )

        txer.transfer_objects(
            transfers=[quote_coin_ret], recipient=SuiAddress(current_address)
        )

        return txer

    def swap_exact_base_for_quote(
        self,
        quote_asset: str,
        pool_id: str,
        token_object_in: str,
        amount_in: int,
        current_address: SuiAddress,
        client_order_id: str,
    ) -> SuiTransaction:
        """
        Swap exact base for quote

        :param quote_asset:
            Full coin type of the quote asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"

        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param token_object_in:
            Object id of the token to swap: eg: "0x6e566fec4c388eeb78a7dab832c9f0212eb2ac7e8699500e203def5b41b9c70d"

        :param amount_in:
            Amount of token to buy or sell, eg: 10000000

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"
        """

        txer = SuiTransaction(self.client)

        [base_coin_ret, quote_coin_ret, _amount] = txer.move_call(
            target=f"{self.package_id}::{CLOB}::swap_exact_base_for_quote",
            arguments=[
                ObjectID(pool_id),
                SuiU64(client_order_id),
                SuiU64(str(amount_in)),
                ObjectID(token_object_in),
                txer.move_call(
                    type_arguments=[quote_asset],  # quoteasset
                    target="0x2::coin::zero",
                    arguments=[],
                ),
                ObjectID(normalize_sui_object_id("0x6")),
            ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        txer.transfer_objects(
            transfers=[base_coin_ret], recipient=SuiAddress(current_address)
        )

        txer.transfer_objects(
            transfers=[quote_coin_ret], recipient=SuiAddress(current_address)
        )

        return txer

    def place_market_order(
        self,
        client_order_id: str,
        pool_id: str,
        quantity: int,
        is_bid: bool,
        base_coin: str,
        quote_coin: str,
        current_address: str,
        account_cap: str,
    ):
        txer = SuiTransaction(self.client)
        [base_coin_ret, quote_coin_ret] = txer.move_call(
            target=f"{self.package_id}::{CLOB}::place_market_order",
            arguments=[
                ObjectID(pool_id),
                ObjectID(account_cap),
                SuiU64(client_order_id),
                SuiU64(quantity),
                SuiBoolean(is_bid),
                ObjectID(base_coin),
                ObjectID(quote_coin),
                ObjectID(normalize_sui_object_id("0x6")),
            ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        txer.transfer_objects(
            transfers=[base_coin_ret], recipient=SuiAddress(current_address)
        )

        txer.transfer_objects(
            transfers=[quote_coin_ret], recipient=SuiAddress(current_address)
        )
        return txer

    def place_limit_order(
        self,
        client_order_id: str,
        pool_id: str,
        price: int,
        quantity: int,
        self_matching_prevention: bool,
        is_bid: bool,
        expire_timestamp: int,
        restriction: int,
        account_cap: str,
    ) -> SuiTransaction:
        """
        Place a limit order

        :param client_order_id:
            client side defined order number, eg "1", "2" etc

        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param price:
            price of the limit order, eg: 180000000

        :param self_matching_prevention:
            True for self matching prevention, false for not, eg: true

        :param quantity:
            Quantity of the limit order in BASE ASSET, eg: 100000000

        :param is_bid:
            True for buying base with quote, false for selling base for quote

        :param expire_timestamp:
            Expire timestamp of the limit order in ms, eg: 1620000000000.
            Alternative you can call deepbookpy.deepbook.helpers.order_expiration() for 24 hours timestamp

        :param restriction:
            Restrictions on limit orders, eg: 0

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """

        txer = SuiTransaction(self.client)

        args = [
            ObjectID(pool_id),
            SuiU64(client_order_id),
            SuiU64(math.floor(price * 1000000000)),
            SuiU64(quantity),
            SuiU8(self_matching_prevention),
            SuiBoolean(is_bid),
            SuiU64(expire_timestamp),
            SuiU8(restriction),
            ObjectID(normalize_sui_object_id("0x6")),
            ObjectID(account_cap),
        ]
        txer.move_call(
            type_arguments=self.get_pool_type_args(pool_id),
            target=f"{self.package_id}::{CLOB}::place_limit_order",
            arguments=args,
        )

        return txer

    def cancel_order(
        self,
        pool_id: str,
        order_id: int,
        account_cap: str,
    ) -> SuiTransaction:
        """
        Cancel a limit order placed onto the CLOB

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param order_id:
            Order id of a limit order, you can find them through function list_open_orders() eg: "0"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::cancel_order",
            arguments=[ObjectID(pool_id), SuiU64(order_id), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer

    def cancel_all_orders(self, pool_id: str, account_cap: str) -> SuiTransaction:
        """
        Cancel all limit orders under a certain account capacity

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::cancel_all_orders",
            arguments=[ObjectID(pool_id), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer

    def batch_cancel_order(
        self,
        pool_id: str,
        order_ids: List[str],
        account_cap: str,
    ) -> SuiTransaction:
        """
        Cancel multiple limit orders to save gas costs.

        :param pool_id::
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param order_ids:
            Order id of a limit order, you can find them through the list_open_orders() function, for example: ["0", "1"]

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::batch_cancel_order",
            arguments=[ObjectID(pool_id), SuiArray(order_ids), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer
    
    def clean_up_expired_orders(
        self,
        pool_id: str,
        order_ids: List[str],
        order_owners: List[str]
    ) -> SuiTransaction:
        """
        Clean up expired orders

        :param pool_id::
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param order_ids:
            Order id of a limit order, you can find them through the list_open_orders() function, for example: ["0", "1"]

        :param order_owners:
            Array of Order owners, should be the owner addresses from the account capacities which placed the orders
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::clean_up_expired_orders",
            arguments=[
                ObjectID(pool_id),
                ObjectID(normalize_sui_object_id("0x6")),
                SuiArray(order_ids),
                SuiArray(order_owners)
                ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer

    def get_order_status(
        self, pool_id: str, order_id: int, account_cap: str
    ) -> InspectTransaction:
        """
        Get the order status

        :param pool_id:
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param order_id:
            the order id, eg: 1

        :param account_cap:
            objectId of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3

        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::get_order_status",
            arguments=[ObjectID(pool_id), SuiU64(str(order_id)), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer.inspect_all()

    def get_market_price(self, pool_id: str) -> InspectTransaction:
        """
        Get Market Price

         :param pool_id:
             object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        """
        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::get_market_price",
            arguments=[
                ObjectID(pool_id),
            ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer.inspect_all()

    def get_user_position(self, pool_id: str, account_cap: str) -> InspectTransaction:
        """
        Get the base and quote token in custodian account

        :param pool_id:
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param account_cap:
            object id of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3

        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::account_balance",
            arguments=[ObjectID(pool_id), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer.inspect_all()

    def list_open_orders(self, pool_id: str, account_cap: str) -> InspectTransaction:
        """
        Get the open orders of the current user

        :param pool_id:
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param account_cap:
            object id of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::list_open_orders",
            arguments=[ObjectID(pool_id), ObjectID(account_cap)],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer.inspect_all()

    def get_level2_book_status(
        self, pool_id: str, lower_price: int, higher_price: int, is_bid_side: bool
    ) -> InspectTransaction:
        """
        Get level2 book status

        :param pool_id:
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param lower_price:
            lower price you want to query in the level2 book, eg: 18000000000

        :param higher_price:
            higher price you want to query in the level2 book, eg: 20000000000

        :param is_bid_side:
            is_bid_side true: query bid side, false: query ask side

        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target=f"{self.package_id}::{CLOB}::get_level2_book_status_bid_side"
            if is_bid_side
            else f"{self.package_id}::{CLOB}::get_level2_book_status_ask_side",
            arguments=[
                ObjectID(pool_id),
                SuiU64(str(lower_price)),
                SuiU64(str(higher_price)),
                ObjectID(normalize_sui_object_id("0x6")),
            ],
            type_arguments=self.get_pool_type_args(pool_id),
        )

        return txer.inspect_all()

    def get_all_pools(self) -> list[str]:
        """Get all deepbook pools"""

        response = self.client.execute(
            QueryEvents(
                query=MoveEventTypeQuery(f"{self.package_id}::{CLOB}::PoolCreated")
            )
        )

        return response._data.__dict__

    def get_pool_info(self, pool_id: ObjectID) -> dict:
        """
        Get pool id, base asset type & quote asset type

        :param pool_id:
            Object ID of pool, e.g "0x417a1101ea707f69826faa51902b0e6b374097c3ae142d8f7e0ba883dae5bfc3".
        """

        response = handle_result(self.client.get_object(pool_id))

        if response.content.data_type != "moveObject":
            return f"Pool {pool_id} does not exist"

        parsed_response = parse_struct(response.content.type_)

        return dict(
            pool_id=pool_id,
            base_asset=parsed_response[0],
            quote_asset=parsed_response[1],
        )

    def get_pool_type_args(self, pool_id: ObjectID) -> list:
        """
        Get pool type arguments -> base asset type and quote asset type

        :param pool_id:
            Object ID of pool, e.g "0x417a1101ea707f69826faa51902b0e6b374097c3ae142d8f7e0ba883dae5bfc3".
        """
        response = self.get_pool_info(pool_id)

        [base_asset_type, quote_asset_type] = (
            response["base_asset"],
            response["quote_asset"],
        )

        return [base_asset_type, quote_asset_type]
