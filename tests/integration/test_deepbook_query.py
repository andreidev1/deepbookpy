"""Test Query DeepBook API"""
from pysui.sui.sui_clients.sync_client import SuiClient
from deepbookpy.deepbook_query import DeepBookQuery
from tests.conftest import dee9_data

token_1 = dee9_data()['test']["token_1"]
token_2 = dee9_data()["test"]["token_2"]
pool_id = dee9_data()["test"]["pool_id"]


def test_get_market_price(init_client, dee9_package_id):
    """Test market price query"""

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.get_market_price(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id
    ).__dict__['effects'].__dict__['status'].__dict__['status']
    
    assert status == 'success'