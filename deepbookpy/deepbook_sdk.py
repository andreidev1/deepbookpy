"""DeepBook Python SDK"""
import math
from typing import List

from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiBoolean

from deepbookpy.utils.normalizer import normalize_sui_object_id


class DeepBookSDK:
    """Write data to DeepBook package"""

    def __init__(self, client: SuiClient, package_id: str):
        
        self.client=client
        self.package_id = package_id

    
    def create_pool(
            self,
            token_1: str,
            token_2: str,
            tick_size: int,
            lot_size: int
    ) -> SuiTransaction:
        """
        Create pool for trading pair - 100 Sui fee

        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of quote asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::usdt::USDT"

        :param tick_size:
            Minimal Price Change Accuracy of this pool, eg: 10000000

        :param lot_size:
            Minimal Lot Change Accuracy of this pool, eg: 10000
        """

        txer = SuiTransaction(self.client)

        splits: list = txer.split_coin(coin=txer.gas, amounts=[100_000_000_000])

        txer.move_call(

            target = f"{self.package_id}::clob::create_pool",

            arguments = [SuiU64(str(tick_size)), SuiU64(str(lot_size)), splits],

            type_arguments = [token_1, token_2]
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
            target = f"{self.package_id}::clob::create_account",

            arguments = [],

            type_arguments = []
        )

        txer.transfer_objects(
            transfers=[cap],
            recipient=SuiAddress(current_address)
        )

        return txer
    
    def deposit_base(self, token_1: str, token_2: str, pool_id: str, coin: str, account_cap: str) -> SuiTransaction:
        """
        Deposit base asset into custodian account
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param coin:
            Object id of coin to deposit, eg: "0x316467544c7e719384579ac5745c75be5984ca9f004d6c09fd7ca24e4d8a3d14"
        
        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """
        
        txer = SuiTransaction(self.client)

        txer.move_call(
            target = f"{self.package_id}::clob::deposit_base",

            arguments = [ObjectID(pool_id), ObjectID(coin), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        return txer
    
    def deposit_quote(self, token_1: str, token_2: str, pool_id: str, coin: str, account_cap: str) -> SuiTransaction:
        """
        Deposit quote asset into custodian account
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param coin:
            Object id of coin to deposit, eg: "0x316467544c7e719384579ac5745c75be5984ca9f004d6c09fd7ca24e4d8a3d14"
        
        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """
        
        txer = SuiTransaction(self.client)

        txer.move_call(
            target = f"{self.package_id}::clob::deposit_quote",

            arguments = [ObjectID(pool_id), ObjectID(coin), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        return txer
    
    
    def withdraw_base(self, token_1: str, token_2: str, pool_id: str, quantity: int, current_address: SuiAddress, account_cap: str) -> SuiTransaction:
        """
        Withdraw base asset from custodian account
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
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
            target = f"{self.package_id}::clob::withdraw_base",

            arguments = [ObjectID(pool_id), SuiU64(quantity), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        txer.transfer_objects(
            transfers=[withdraw],
            recipient=SuiAddress(current_address)
        )

        return txer
    
    def withdraw_quote(self, token_1: str, token_2: str, pool_id: str, quantity: int, current_address: SuiAddress, account_cap: str) -> SuiTransaction:
        """
        Withdraw quote asset from custodian account
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
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
            target = f"{self.package_id}::clob::withdraw_quote",

            arguments = [ObjectID(pool_id), SuiU64(quantity), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        txer.transfer_objects(
            transfers=[withdraw],
            recipient=SuiAddress(current_address)
        )

        return txer
    

    def swap_exact_quote_for_base(self, token_1: str, token_2: str, pool_id: str, token_object_in: str, amount_in: int, current_address: SuiAddress) -> SuiTransaction:
        """
        Swap exact quote for base
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
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
            target = f"{self.package_id}::clob::swap_exact_quote_for_base",

            arguments = [ObjectID(pool_id), SuiU64(amount_in), ObjectID(normalize_sui_object_id('0x6')), ObjectID(token_object_in)],

            type_arguments = [token_1, token_2]
        )

        txer.transfer_objects(
            transfers=[base_coin_ret],
            recipient=SuiAddress(current_address)
        )

        txer.transfer_objects(
            transfers=[quote_coin_ret],
            recipient=SuiAddress(current_address)
        )

        return txer
    
    def swap_exact_base_for_quote(self, token_1: str, token_2: str, pool_id: str, treasury: str, token_object_in: str, amount_in: int, current_address: SuiAddress) -> SuiTransaction:
        """
        Swap exact base for quote
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param treasury:
            treasury of the quote coin, in the selling case, we will mint a zero quote coin to receive the quote coin from the pool. eg: "0x0a11d301013759e79cb5f89a8bb29c3f9a9bb5be6dec2ddba48ea4b39abc5b5a"

        :param token_object_in:
            Object id of the token to swap: eg: "0x6e566fec4c388eeb78a7dab832c9f0212eb2ac7e8699500e203def5b41b9c70d"
        
        :param amount_in:
            Amount of token to buy or sell, eg: 10000000

        :param current_address:
            current user address, eg: "0xbddc9d4961b46a130c2e1f38585bbc6fa8077ce54bcb206b26874ac08d607966"
        """
        
        txer = SuiTransaction(self.client)

        [base_coin_ret, quote_coin_ret, _amount] = txer.move_call(
            target = f"{self.package_id}::clob::swap_exact_base_for_quote",

            arguments = [
                ObjectID(pool_id),
                SuiU64(amount_in),
                ObjectID(token_object_in),
                # mint
                _mint(token_2, 0, treasury, txer),
                ObjectID(normalize_sui_object_id('0x6')),
                ],

            type_arguments = [token_1, token_2]
        )

        txer.transfer_objects(
            transfers=[base_coin_ret],
            recipient=SuiAddress(current_address)
        )

        txer.transfer_objects(
            transfers=[quote_coin_ret],
            recipient=SuiAddress(current_address)
        )

        return txer
    

    def place_limit_order(
            self,
            token_1: str,
            token_2: str,
            pool_id: str,
            price: int,
            quantity: int,
            is_bid: bool,
            expire_timestamp: int,
            restriction: int,
            account_cap: str
        ) -> SuiTransaction:
        """
        Place a limit order
        
        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param pool_id:
            Object id of pool, created after invoking create_pool, eg: "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"

        :param price:
            price of the limit order, eg: 180000000
        
        :param quantity:
            Quantity of the limit order in BASE ASSET, eg: 100000000

        :param is_bid:
            True for buying base with quote, false for selling base for quote
        
        :param expire_timestamp:
            Expire timestamp of the limit order in ms, eg: 1620000000000
        
        :param restriction:
            Restrictions on limit orders, eg: 0

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account(), eg: "0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
        """
        
        txer = SuiTransaction(self.client)

        args = [
                ObjectID(str(pool_id)),
                SuiU64(math.floor(price * 1000000000)),
                SuiU64(quantity),
                SuiBoolean(is_bid),
                SuiU64(expire_timestamp),
                SuiU64(restriction),
                ObjectID(normalize_sui_object_id('0x6')),
                ObjectID(account_cap)
            ]
        txer.move_call(
            target = f"{self.package_id}::clob::place_limit_order",

            arguments = args,

            type_arguments = [token_1, token_2]
        )

        return txer

    def cancel_order(
            self,
            token_1: str,
            token_2: str,
            pool_id: str,
            order_id: str,
            account_cap: str,
            ) -> SuiTransaction:
        """
        Cancel a limit order placed onto the CLOB

        :param token_1:
            Full coin type of the base asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::wbtc::WBTC
        
        :param token_2:
           Full coin type of quote asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param order_id:
            Order id of a limit order, you can find them through function list_open_orders() eg: "0"

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target = f"{self.package_id}::clob::cancel_order",

            arguments = [ObjectID(pool_id), ObjectID(order_id), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        return txer
    
    def cancel_all_orders(
            self,
            token_1: str,
            token_2: str,
            pool_id: str,
            account_cap: str
    ) -> SuiTransaction:
    
        """
        Cancel all limit orders under a certain account capacity

        :param token_1:
            Full coin type of the base asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::wbtc::WBTC
        
        :param token_2:
           Full coin type of quote asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH

        :param pool_id:
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target = f"{self.package_id}::clob::cancel_all_orders",

            arguments = [ObjectID(pool_id), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        return txer
    
    def batch_cancel_order(
            self,
            token_1: str,
            token_2: str,
            pool_id: str,
            order_ids: List[str],
            account_cap: str
    ) -> SuiTransaction:
    
        """
        Cancel multiple limit orders to save gas costs.

        :param token_1:
            Full coin type of the base asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::wbtc::WBTC
        
        :param token_2:
           Full coin type of quote asset, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH

        :param pool_id::
            Object id of pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4

        :param order_ids:
            orderId of a limit order, you can find them through the function list_open_orders, for example: ["0", "1"]

        :param account_cap:
            Object id of Account Capacity under user address, created after invoking create_account()
        """

        txer = SuiTransaction(self.client)

        txer.move_call(
            target = f"{self.package_id}::clob::batch_cancel_order",

            arguments = [ObjectID(pool_id), ObjectID(order_ids), ObjectID(account_cap)],

            type_arguments = [token_1, token_2]
        )

        return txer
    

    def _mint(self, token: str, quantity: int, treasury: str, txer: SuiTransaction):
        """
        
        :param token:
            the token type you want to mint, eg: "0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::wbtc::WBTC"
        
        :param quantity:
            the quantity you want to mint, eg: 2000000000

        :param treasury:
            the treasury object id, eg: "0x765c7040f06527df0f76d5a38ceaae67c70311c90c266acf15e39f17e0e4ed61"
        
        :param txer:
            SuiTransaction instance
        
        """
        return txer.move_call(
            target = "0x2::coin::mint",

            arguments = [
                ObjectID(str(treasury)),
                ObjectID(str(quantity))
                ],

            type_arguments = [token]
        )
