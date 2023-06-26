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


def dee9_data():
    return dict(main=dict(),
                test=dict(
                        token_1="0x1c3e542f90547ee5b5638c15d3105746740058d20a5f1b4b7c39db5e7dd70acf::wsui::WSUI", 
                        token_2="0x1c3e542f90547ee5b5638c15d3105746740058d20a5f1b4b7c39db5e7dd70acf::usd::USD",
                        pool_id="0xdb4ec5cdc7b98f085ffc8d3e6d7bfaeff5fafe6fb928e2617be9ea501ce1036c"
                        ),
                dev=dict()
                )


@pytest.fixture(scope='module')
def package_id():
    return "0x8da36ef392a7d2b1e7dac2a987767eea5a415d843d3d34cb66bec6434001f931"

