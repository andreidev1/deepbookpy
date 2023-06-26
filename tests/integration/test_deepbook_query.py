"""Test Query DeepBook API"""
from pysui.sui.sui_clients.sync_client import SuiClient
from deepbookpy.deepbook_query import DeepBookQuery

   

def test_get_market_price(init_client, package_id):
    """Test get market price query"""

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, package_id)

    status = deepbook_query.get_market_price(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"
    ).__dict__['effects'].__dict__['status'].__dict__['status']
    
    assert status == 'success'