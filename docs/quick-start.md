## Install deepbookpy

Install deepbookpy by using `` in your terminal

## Set up pysui config
Replace `rpc_url`, `prv_keys`, `ws_url` with your desired data.

```py
from pysui.sui.sui_config import SuiConfig
from pysui.sui.sui_clients.sync_client import SuiClient


def cfg_user():
    """Config user"""
    cfg = SuiConfig.user_config(
        # Required
        rpc_url="https://fullnode.testnet.sui.io:443/",
        # Must be a valid Sui keystring (i.e. 'key_type_flag | private_key_seed' )
        prv_keys=["AIUPxQveY18QggDDdTO0D0OD6PNVvtet50072d1grIyl"],
        # Needed for subscribing
        ws_url="wss://fullnode.testnet.sui.io:443/",
    )
    return cfg

cfg = cfg_user()
client = SuiClient(cfg)
my_sui_address = cfg.addresses[0]
```

## DeepBook Package ID

```py
from deepbookpy.utils import normalize_sui_object_id

deepbook_package_id = normalize_sui_object_id("dee6")

```

## Query DeepBook Package

In order to query the deepbook package you have to instantiate `DeepBookQuery` class

```py
from deepbookpy.deepbook_query import DeepBookQuery


deepbook_query = DeepBookQuery(
    client=client,
    package_id=deepbook_package_id
)
```

Sample of calling `::clob::get_market_price`
```py

deepbook_query.get_market_price(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    pool_id="0xcaee8e1c046b58e55196105f1436a2337dcaa0c340a7a8c8baf65e4afb8823a4"
)

```

## Write to DeepBook Package

In order to write the deepbook package you have to instantiate `DeepBookSDK` class

```py
from deepbookpy.deepbook_sdk import DeepBookSDK


deepbook = DeepBookSDK(
    client=client,
    package_id=deepbook_package_id
)
```

Sample of executing `::clob::create_pool`

```py
from deepbookpy.deepbook_sdk import DeepBookSDK

create_pool = deepbook.create_pool(
    token_1="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::weth::WETH",
    token_2="0x5378a0e7495723f7d942366a125a6556cf56f573fa2bb7171b554a2986c4229a::usdt::USDT",
    ticket_size=10000000,
    lot_size=10000
)

# Execute the transaction
tx_result = create_pool.execute(gas_budget="100000")
if tx_result.is_ok():
    if hasattr(tx_result.result_data, "to_json"):
        print(tx_result.result_data.to_json(indent=2))
    else:
        print(tx_result.result_data)
else:
    print(tx_result.result_string)
```

**_NOTE:_**  At this moment deepbook is under development and you might experience issues with `dee6` package. Additionally you can use this `0x8da36ef392a7d2b1e7dac2a987767eea5a415d843d3d34cb66bec6434001f931` address as package id.