from typing import TypedDict, Dict
from dataclasses import dataclass
from deepbookpy.custom_types import Coin, Pool
from deepbookpy.utils.normalizer import normalize_sui_object_id

"""Sui Constants"""

CLOCK = normalize_sui_object_id("0x6")

@dataclass
class DeepbookPackageIds(TypedDict):
    DEEPBOOK_PACKAGE_ID: str
    REGISTRY_ID: str
    DEEP_TREASURY_ID: str

testnet_package_ids: DeepbookPackageIds = {
    "DEEPBOOK_PACKAGE_ID": "0xcbf4748a965d469ea3a36cf0ccc5743b96c2d0ae6dee0762ed3eca65fac07f7e",
    "REGISTRY_ID": "0x98dace830ebebd44b7a3331c00750bf758f8a4b17a27380f5bb3fbe68cb984a7",
    "DEEP_TREASURY_ID": "0x69fffdae0075f8f71f4fa793549c11079266910e8905169845af1f5d00e09dcb",
}

mainnet_package_ids: DeepbookPackageIds = {
    "DEEPBOOK_PACKAGE_ID": "0x2c8d603bc51326b8c13cef9dd07031a408a48dddb541963357661df5d3204809",
    "REGISTRY_ID": "0xaf16199a2dff736e9f07a845f23c5da6df6f756eddb631aed9d24a93efc4549d",
    "DEEP_TREASURY_ID": "0x032abf8948dda67a271bcc18e776dbbcfb0d58c8d288a700ff0d5521e57a1ffe",
}

testnet_coins: Dict[str, Coin] = {
    "DEEP": {
        "address": "0x36dbef866a1d62bf7328989a10fb2f07d769f4ee587c0de4a0a256e57e0a58a8",
        "type": "0x36dbef866a1d62bf7328989a10fb2f07d769f4ee587c0de4a0a256e57e0a58a8::deep::DEEP",
        "scalar": 1000000,
    },
    "SUI": {
        "address": "0x0000000000000000000000000000000000000000000000000000000000000002",
        "type": "0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI",
        "scalar": 1000000000,
    },
    "DBUSDC": {
        "address": "0xf7152c05930480cd740d7311b5b8b45c6f488e3a53a11c3f74a6fac36a52e0d7",
        "type": "0xf7152c05930480cd740d7311b5b8b45c6f488e3a53a11c3f74a6fac36a52e0d7::DBUSDC::DBUSDC",
        "scalar": 1000000,
    },
    "DBUSDT": {
        "address": "0xf7152c05930480cd740d7311b5b8b45c6f488e3a53a11c3f74a6fac36a52e0d7",
        "type": "0xf7152c05930480cd740d7311b5b8b45c6f488e3a53a11c3f74a6fac36a52e0d7::DBUSDT::DBUSDT",
        "scalar": 1000000,
    },
}


mainnet_coins: Dict[str, Coin] = {
    "DEEP": {
        "address": "0xdeeb7a4662eec9f2f3def03fb937a663dddaa2e215b8078a284d026b7946c270",
        "type": "0xdeeb7a4662eec9f2f3def03fb937a663dddaa2e215b8078a284d026b7946c270::deep::DEEP",
        "scalar": 1000000,
    },
    "SUI": {
        "address": "0x0000000000000000000000000000000000000000000000000000000000000002",
        "type": "0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI",
        "scalar": 1000000000,
    },
    "USDC": {
        "address": "0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7",
        "type": "0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC",
        "scalar": 1000000,
    },
    "WUSDC": {
        "address": "0x5d4b302506645c37ff133b98c4b50a5ae14841659738d6d733d59d0d217a93bf",
        "type": "0x5d4b302506645c37ff133b98c4b50a5ae14841659738d6d733d59d0d217a93bf::coin::COIN",
        "scalar": 1000000,
    },
    "WETH": {
        "address": "0xaf8cd5edc19c4512f4259f0bee101a40d41ebed738ade5874359610ef8eeced5",
        "type": "0xaf8cd5edc19c4512f4259f0bee101a40d41ebed738ade5874359610ef8eeced5::coin::COIN",
        "scalar": 100000000,
    },
    "BETH": {
        "address": "0xd0e89b2af5e4910726fbcd8b8dd37bb79b29e5f83f7491bca830e94f7f226d29",
        "type": "0xd0e89b2af5e4910726fbcd8b8dd37bb79b29e5f83f7491bca830e94f7f226d29::eth::ETH",
        "scalar": 100000000,
    },
    "WBTC": {
        "address": "0x027792d9fed7f9844eb4839566001bb6f6cb4804f66aa2da6fe1ee242d896881",
        "type": "0x027792d9fed7f9844eb4839566001bb6f6cb4804f66aa2da6fe1ee242d896881::coin::COIN",
        "scalar": 100000000,
    },
    "WUSDT": {
        "address": "0xc060006111016b8a020ad5b33834984a437aaa7d3c74c18e09a95d48aceab08c",
        "type": "0xc060006111016b8a020ad5b33834984a437aaa7d3c74c18e09a95d48aceab08c::coin::COIN",
        "scalar": 1000000,
    },
    "NS": {
        "address": "0x5145494a5f5100e645e4b0aa950fa6b68f614e8c59e17bc5ded3495123a79178",
        "type": "0x5145494a5f5100e645e4b0aa950fa6b68f614e8c59e17bc5ded3495123a79178::ns::NS",
        "scalar": 1000000,
    },
    "TYPUS": {
        "address": "0xf82dc05634970553615eef6112a1ac4fb7bf10272bf6cbe0f80ef44a6c489385",
        "type": "0xf82dc05634970553615eef6112a1ac4fb7bf10272bf6cbe0f80ef44a6c489385::typus::TYPUS",
        "scalar": 1000000000,
    },
    "AUSD": {
        "address": "0x2053d08c1e2bd02791056171aab0fd12bd7cd7efad2ab8f6b9c8902f14df2ff2",
        "type": "0x2053d08c1e2bd02791056171aab0fd12bd7cd7efad2ab8f6b9c8902f14df2ff2::ausd::AUSD",
        "scalar": 1000000,
    },
    "DRF": {
        "address": "0x294de7579d55c110a00a7c4946e09a1b5cbeca2592fbb83fd7bfacba3cfeaf0e",
        "type": "0x294de7579d55c110a00a7c4946e09a1b5cbeca2592fbb83fd7bfacba3cfeaf0e::drf::DRF",
        "scalar": 1000000,
    },
}

testnet_pools = {
    "DEEP_SUI": {
        "address": "0x0d1b1746d220bd5ebac5231c7685480a16f1c707a46306095a4c67dc7ce4dcae",
        "base_coin": "DEEP",
        "quote_coin": "SUI",
    },
    "SUI_DBUSDC": {
        "address": "0x520c89c6c78c566eed0ebf24f854a8c22d8fdd06a6f16ad01f108dad7f1baaea",
        "base_coin": "SUI",
        "quote_coin": "DBUSDC",
    },
    "DEEP_DBUSDC": {
        "address": "0xee4bb0db95dc571b960354713388449f0158317e278ee8cda59ccf3dcd4b5288",
        "base_coin": "DEEP",
        "quote_coin": "DBUSDC",
    },
    "DBUSDT_DBUSDC": {
        "address": "0x69cbb39a3821d681648469ff2a32b4872739d2294d30253ab958f85ace9e0491",
        "base_coin": "DBUSDT",
        "quote_coin": "DBUSDC",
    },
}

mainnet_pools = {
    "DEEP_SUI": {
        "address": "0xb663828d6217467c8a1838a03793da896cbe745b150ebd57d82f814ca579fc22",
        "base_coin": "DEEP",
        "quote_coin": "SUI",
    },
    "SUI_USDC": {
        "address": "0xe05dafb5133bcffb8d59f4e12465dc0e9faeaa05e3e342a08fe135800e3e4407",
        "base_coin": "SUI",
        "quote_coin": "USDC",
    },
    "DEEP_USDC": {
        "address": "0xf948981b806057580f91622417534f491da5f61aeaf33d0ed8e69fd5691c95ce",
        "base_coin": "DEEP",
        "quote_coin": "USDC",
    },
    "WUSDT_USDC": {
        "address": "0x4e2ca3988246e1d50b9bf209abb9c1cbfec65bd95afdacc620a36c67bdb8452f",
        "base_coin": "WUSDT",
        "quote_coin": "USDC",
    },
    "WUSDC_USDC": {
        "address": "0xa0b9ebefb38c963fd115f52d71fa64501b79d1adcb5270563f92ce0442376545",
        "base_coin": "WUSDC",
        "quote_coin": "USDC",
    },
    "BETH_USDC": {
        "address": "0x1109352b9112717bd2a7c3eb9a416fff1ba6951760f5bdd5424cf5e4e5b3e65c",
        "base_coin": "BETH",
        "quote_coin": "USDC",
    },
    "NS_USDC": {
        "address": "0x0c0fdd4008740d81a8a7d4281322aee71a1b62c449eb5b142656753d89ebc060",
        "base_coin": "NS",
        "quote_coin": "USDC",
    },
    "NS_SUI": {
        "address": "0x27c4fdb3b846aa3ae4a65ef5127a309aa3c1f466671471a806d8912a18b253e8",
        "base_coin": "NS",
        "quote_coin": "SUI",
    },
    "TYPUS_SUI": {
        "address": "0xe8e56f377ab5a261449b92ac42c8ddaacd5671e9fec2179d7933dd1a91200eec",
        "base_coin": "TYPUS",
        "quote_coin": "SUI",
    },
    "SUI_AUSD": {
        "address": "0x183df694ebc852a5f90a959f0f563b82ac9691e42357e9a9fe961d71a1b809c8",
        "base_coin": "SUI",
        "quote_coin": "AUSD",
    },
    "AUSD_USDC": {
        "address": "0x5661fc7f88fbeb8cb881150a810758cf13700bb4e1f31274a244581b37c303c3",
        "base_coin": "AUSD",
        "quote_coin": "USDC",
    },
    "DRF_SUI": {
        "address": "0x126865a0197d6ab44bfd15fd052da6db92fd2eb831ff9663451bbfa1219e2af2",
        "base_coin": "DRF",
        "quote_coin": "SUI",
    },
}
