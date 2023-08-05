"""Configuration test file"""

import pytest

from pysui.sui.sui_config import SuiConfig

from deepbookpy.utils.normalizer import normalize_sui_object_id


def network_client():
    return dict(main=dict(rpc_url="https://fullnode.mainnet.sui.io:443/", ws_url="wss://fullnode.mainnet.sui.io:443/"),
                test=dict(rpc_url="https://fullnode.testnet.sui.io:443/", ws_url="wss://fullnode.testnet.sui.io:443/"),
                dev=dict(rpc_url="https://fullnode.devnet.sui.io:443/", ws_url="wss://fullnode.devnet.sui.io:443/")
                )
                

@pytest.fixture(scope='module')
def init_client():
    """Init client"""
    cfg = SuiConfig.user_config(
        # Required
        rpc_url=network_client()["test"]["rpc_url"],
        # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
        prv_keys=["AIUPxQveY18QggDDdTO0D0OD6PNVvtet50072d1grIyl"],
        # Needed for subscribing
        ws_url=network_client()["test"]["ws_url"]
    )
    return cfg


@pytest.fixture(scope='module')
def dee9_package_id():
    return normalize_sui_object_id("dee9")


def dee9_data_v2():
    """Clob v2 data"""
    return dict(main=dict(),
                test=dict(
                        base_asset_type="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::wbtc::WBTC", 
                        quote_asset_type="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
                        pool_id="0xe3c2a6adf92d4652335387534225240828e918f5a834b466c3842bae4f99ce0f",
                        account_cap="0x0a433217916d38142ada900114cf3c73f50f11ad7bc1279e0ba6644868fc8d89"
                        ),
                dev=dict()
                )

