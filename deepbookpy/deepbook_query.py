"""Query Sui DeepBook"""

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64
from pysui.sui.sui_builders.exec_builders import InspectTransaction
from pysui.sui.sui_types.event_filter import MoveEventTypeQuery
from pysui.sui.sui_builders.get_builders import QueryEvents
from pysui.sui.sui_clients.common import handle_result

from deepbookpy.utils.normalizer import normalize_sui_object_id
from deepbookpy.utils.constants import CLOB
from deepbookpy.utils.helpers import parse_struct


class DeepBookQuery:
    """Query DeepBook Package"""

    def __init__(self, client: SuiClient, package_id: str):
        self.client = client
        self.package_id = package_id

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
