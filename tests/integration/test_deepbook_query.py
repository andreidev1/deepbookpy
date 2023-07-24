"""Test Query DeepBook API"""
import flaky
from pysui.sui.sui_clients.sync_client import SuiClient

from deepbookpy.deepbook_query import DeepBookQuery
from tests.conftest import dee9_data_v2

token_1 = dee9_data_v2()['test']["token_1"]
token_2 = dee9_data_v2()["test"]["token_2"]
pool_id = dee9_data_v2()["test"]["pool_id"]
account_cap = dee9_data_v2()["test"]["account_cap"]


@flaky.flaky()
def test_get_market_price(init_client, dee9_package_id):
    """Test market price query function"""

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.get_market_price(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id
    ).__dict__['effects'].__dict__['status'].__dict__['status']
    
    assert status == 'success'


@flaky.flaky()
def test_get_usr_position(init_client, dee9_package_id):

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.get_usr_position(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id,
    account_cap=account_cap
    ).__dict__['effects'].__dict__['status'].__dict__['status']

    assert status == 'success'


@flaky.flaky()
def test_list_open_orders(init_client, dee9_package_id):

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.list_open_orders(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id,
    account_cap=account_cap
    ).__dict__['effects'].__dict__['status'].__dict__['status']

    assert status == 'success'


@flaky.flaky()
def test_get_level2_book_status_true_bid(init_client, dee9_package_id):

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.get_level2_book_status(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id,
    lower_price=18000000000,
    higher_price=20000000000,
    is_bid_side=True
    ).__dict__['effects'].__dict__['status'].__dict__['status']

    assert status == 'success'


@flaky.flaky()
def test_get_level2_book_status_false_bid(init_client, dee9_package_id):

    client = SuiClient(init_client)
    deepbook_query = DeepBookQuery(client, dee9_package_id)

    status = deepbook_query.get_level2_book_status(
    token_1=token_1,
    token_2=token_2,
    pool_id=pool_id,
    lower_price=18000000000,
    higher_price=20000000000,
    is_bid_side=False
    ).__dict__['effects'].__dict__['status'].__dict__['status']

    assert status == 'success'
