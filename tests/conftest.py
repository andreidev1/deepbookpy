"""Configuration test file"""

import pytest

from pysui.sui.sui_config import SuiConfig


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
def package_id():
    return "0x8da36ef392a7d2b1e7dac2a987767eea5a415d843d3d34cb66bec6434001f931"

