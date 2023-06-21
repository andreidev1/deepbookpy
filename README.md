# Community Sui Deepbook Python SDK

Built with [pysui](https://github.com/FrankC01/pysui/)

## Python Sui DeepBook SDK Parameters
```py
from deepbookpy.utils.normalizer import normalize_sui_object_id

DEEPBOOK_PACKAGE_ID = "https://explorer.sui.io/object/0x000000000000000000000000000000000000000000000000000000000000dee9"

CLOCK = normalize_sui_object_id("0x6")
```
## Quick Start
See [here](https://github.com/andreidev1/deepbookpy/tree/main/docs/quick-start.md) how to get started using deepbookpy 

## DeepBook Sources

[Official Deepbook Sui Website](https://sui-deepbook.com/)

[Official Deepbook Sui Documentation](https://docs.sui-deepbook.com/)

## DeepBook Packages

[DeepBook Mainnet Package](https://suiexplorer.com/object/0x000000000000000000000000000000000000000000000000000000000000dee9)

[DeepBook Testnet Package](https://suiexplorer.com/object/0x000000000000000000000000000000000000000000000000000000000000dee9?network=testnet)

[DeepBook Devnet Package](https://suiexplorer.com/object/0x000000000000000000000000000000000000000000000000000000000000dee9?network=devnet)

## DeepBook Fee Structure

The current default maker rebate fee rate is 0.25%, and the default taker commission rate is 0.5%. 

Creating pool is permissionless, and it will incur a 100 SUI fee for creating a pool.