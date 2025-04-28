from deepbookpy.transactions.balance_manager import BalanceManagerContract
from .constants import mainnet_coins, mainnet_pools, mainnet_package_ids, testnet_coins, testnet_pools, testnet_package_ids
from deepbookpy.utils.normalizer import normalize_sui_address
from dataclasses import dataclass

FLOAT_SCALAR = 1000000000
MAX_TIMESTAMP = 1844674407370955161 
GAS_BUDGET = 0.5 * 500000000  
DEEP_SCALAR = 1000000
POOL_CREATION_FEE = 500 * 1_000_000;  # 500 DEEP

@dataclass
class DeepBookConfig:
    def __init__(
        self,
        env,
        address,
        admin_cap=None,
        balance_managers=None,
        coins=None,
        pools=None,
    ):
        self._coins = None
        self._pools = None
        self.balance_managers = balance_managers or {}
        self.address = self.normalize_sui_address(address)
        self.admin_cap = admin_cap

        if env == "mainnet":
            self._coins = coins or mainnet_coins
            self._pools = pools or mainnet_pools
            self.DEEPBOOK_PACKAGE_ID = mainnet_package_ids["DEEPBOOK_PACKAGE_ID"]
            self.REGISTRY_ID = mainnet_package_ids["REGISTRY_ID"]
            self.DEEP_TREASURY_ID = mainnet_package_ids["DEEP_TREASURY_ID"]
        else:
            self._coins = coins or testnet_coins
            self._pools = pools or testnet_pools
            self.DEEPBOOK_PACKAGE_ID = testnet_package_ids["DEEPBOOK_PACKAGE_ID"]
            self.REGISTRY_ID = testnet_package_ids["REGISTRY_ID"]
            self.DEEP_TREASURY_ID = testnet_package_ids["DEEP_TREASURY_ID"]

        self.balance_manager = BalanceManagerContract(self)

    @staticmethod
    def normalize_sui_address(address):
        return normalize_sui_address(address)

    # Getters
    def get_coin(self, key):
        coin = self._coins.get(key)
        if not coin:
            raise KeyError(f"Coin not found for key: {key}")
        return coin

    def get_pool(self, key):
        pool = self._pools.get(key)
        if not pool:
            raise KeyError(f"Pool not found for key: {key}")
        return pool

    def get_balance_manager(self, manager_key):
        if manager_key not in self.balance_managers:
            raise KeyError(f"Balance manager with key {manager_key} not found.")
        return self.balance_managers[manager_key]

