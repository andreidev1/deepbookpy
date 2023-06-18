"""Query Sui DeepBook"""
from dataclasses import dataclass

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_builders.exec_builders import InspectTransaction

from utils.config import client, address, cfg



class DeepBookQuery:

    provider: SuiClient
    current_address: SuiAddress

    def __init__(self, provider: SuiClient, current_address: SuiAddress):
        self.provider = provider
        self.current_address = current_address


    def get_order_status(
        self,
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

        :param pool_id: 
            the pool id, eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param order_id:
            the order id, eg: 1

        :param account_cap: 
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
        
        tx_result = txer.execute(gas_budget="100000")
        if tx_result.is_ok():
            if hasattr(tx_result.result_data, "to_json"):
                print(tx_result.result_data.to_json(indent=2))
            else:
                print(tx_result.result_data)
        else:
            print(tx_result.result_string)


        #return txer.inspect_all()
        return print(txer)
    
    def get_market_price(
            self,
            token_1,
            token_2,
            pool_id
    ):


        txer = SuiTransaction(client)

        txer.move_call(

            target="0x8da36ef392a7d2b1e7dac2a987767eea5a415d843d3d34cb66bec6434001f931::clob::get_market_price",

            arguments= [
                ObjectID(pool_id),
                ],

            type_arguments = [token_1, token_2]
    )
        
        #return InspectTransaction(sender_address=self.current_address, tx_bytes=txer)
        return txer.inspect_all()
    
deep = DeepBookQuery(cfg.rpc_url, SuiAddress("0xffd8243510abac793771d998950d08d7a3ec6ad8f39d8e06b7b73687a93de2b9"))

print(deep.get_market_price(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"
))
'''
deep.get_order_status(
    token_1 = "0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a",
    token_2 = "0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a",
    pool_id = "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4",
    order_id = 1,
    account_cap="0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"

)
'''
# ValueError: Unable to find target: dee9::clob::get_order_status
