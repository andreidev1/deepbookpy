"""Query Sui DeepBook"""

from pysui.sui.sui_clients.sync_client import SuiClient
from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_builders.exec_builders import InspectTransaction


from utils.config import cfg, client
from utils.normalizer import normalize_sui_object_id



class DeepBookQuery:
    """Deepbook query"""

    def __init__(self, provider: SuiClient, current_address: SuiAddress, package_id: str):
        self.provider = provider
        self.current_address = current_address
        self.package_id = package_id

    def get_order_status(
        self,
        token_1: str,
        token_2: str,
        pool_id: str,
        order_id: int,
        account_cap: str
    ) -> InspectTransaction:
        """
        Get the order status 
        
        :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param pool_id: 
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param order_id:
            the order id, eg: 1

        :param account_cap: 
            objectId of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3
        
        """

        txer = SuiTransaction(client)

        txer.move_call(

            target=f"{self.package_id}::clob::get_order_status",

            arguments= [
                ObjectID(pool_id),
                SuiU64(str(order_id)),
                ObjectID(account_cap)
                ],

            type_arguments = [token_1, token_2]
    )
        
        return txer.inspect_all()

    
    def get_market_price(
            self,
            token_1: str,
            token_2: str,
            pool_id: str
    ) -> InspectTransaction:
        """
       Get Market Price

       :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param pool_id: 
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        """
        txer = SuiTransaction(client)
       
        txer.move_call(

            target=f"{self.package_id}::clob::get_market_price",

            arguments= [
                ObjectID(pool_id),
                ],

            type_arguments = [token_1, token_2]
    )
        

        return txer.inspect_all()
    

    def get_usr_position(self, token_1: str, token_2: str, pool_id: str, account_cap: str) -> InspectTransaction :
        """
        Get the base and quote token in custodian account
        
        :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param pool_id: 
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param account_cap: 
            object id of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3

        """

        txer = SuiTransaction(client)

        txer.move_call(

            target=f"{self.package_id}::clob::account_balance",

            arguments= [
                ObjectID(pool_id),
                ObjectID(account_cap)
                ],

            type_arguments = [token_1, token_2]
    )
        

        return txer.inspect_all()
    

    def list_open_orders(self, token_1: str, token_2: str, pool_id: str, account_cap: str) -> InspectTransaction:
        """
        Get the open orders of the current user
        
        :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param pool_id: 
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param account_cap: 
            object id of the accountCap, created by invoking create_account, eg: 0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3
        """
        
        txer = SuiTransaction(client)

        txer.move_call(

            target=f"{self.package_id}::clob::list_open_orders",

            arguments= [
                ObjectID(pool_id),
                ObjectID(account_cap)
                ],

            type_arguments = [token_1, token_2]
    )
        

        return txer.inspect_all()
    
    
    def get_level2_book_status(self, token_1: str, token_2: str, pool_id: str, lower_price: int, higher_price: int, is_bide_size: bool) -> InspectTransaction:
        """
        Get level2 book status

        :param token_1:
            token_1 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH
        
        :param token_2:
            token_2 of a certain pair, eg: 0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT

        :param pool_id: 
            object id of the pool, created after invoking create_pool(), eg: 0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4
        
        :param lower_price:
            lower price you want to query in the level2 book, eg: 18000000000

        :param higher_price:
            higher price you want to query in the level2 book, eg: 20000000000
        
        :param is_bid_side:
            is_bid_side true: query bid side, false: query ask side
        
        """

        txer = SuiTransaction(client)

        txer.move_call(
    
            target=f"{self.package_id}::clob::get_level2_book_status_bid_side" if is_bide_size else f"{self.package_id}::clob::get_level2_book_status_ask_side",
            
            arguments= [
                ObjectID(pool_id),
                SuiU64(str(lower_price)),
                SuiU64(str(higher_price)),
                ObjectID(normalize_sui_object_id('0x6'))
                ],

            type_arguments = [token_1, token_2]
    )
        

        return txer.inspect_all()
    

deep = DeepBookQuery(provider= cfg.rpc_url,
                     current_address = SuiAddress(cfg.addresses[0]),
                     package_id="0x8da36ef392a7d2b1e7dac2a987767eea5a415d843d3d34cb66bec6434001f931"
                     )
'''
deep.get_order_status(
    token_1 = "0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a",
    token_2 = "0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a",
    pool_id = "0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4",
    order_id = 1,
    account_cap="0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"

)
'''

print(deep.get_market_price(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"
))


print('----')

print(deep.get_usr_position(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4",
    account_cap="0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
))


print('----')
print(deep.list_open_orders(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4",
    account_cap="0x6f699fef193723277559c8f499ca3706121a65ac96d273151b8e52deb29135d3"
))


print('----')
print(deep.get_level2_book_status(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4",
    lower_price=18000000000,
    higher_price=20000000000,
    is_bide_size=False

))
print('----')
''''''