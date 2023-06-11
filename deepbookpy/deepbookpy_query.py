"""Query Sui DeepBook"""
from dataclasses import dataclass

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID
# from pysui.sui.sui.builders.exec_builders import InspectTransaction

from utils.config import client


class DeepBookQuery:

    provider: SuiClient
    current_address: SuiClient

    def __init__(self, provider: SuiClient, current_address: str):
        self.provider = provider
        self.current_address = current_address


    async def get_order_status(
        token_1: str,
        token_2: str,
        pool_id: str,
        order_id: int,
        account_cap: str
    ):
        """
        Get the order status 
        
        :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param poolId: 
            the pool id, eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param orderId:
            the order id, eg: 1

        :param accountCap: 
            the accountCap, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3
        
        """

        txer = SuiTransaction(client)

        txer.move_call(

            target="dee9::clob::get_order_status",

            arguments= [
                ObjectID(pool_id),
                ObjectID(str(order_id)),
                ObjectID(account_cap)
                ],

            type_arguments = [token_1, token_2]
    )
        
        return txer.inspect_all()