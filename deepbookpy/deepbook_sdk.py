"""DeepBook Python SDK"""
from dataclasses import dataclass

from pysui.sui.sui_clients.transaction import SuiTransaction
from pysui.sui.sui_clients.sync_client import SuiClient

from utils.dto import Records
from utils.config import client


@dataclass
class SmartRouteResult:
    max_swap_tokens: int
    smart_route: str

@dataclass
class SmartRouteResultWithExactPath:
    txb: SuiTransaction
    amount: int


class DeepBookSDK:

    provider: SuiClient
    current_address: str #SuiClient
    gas_budget: int
    records: Records

    def __init__(
            self,
            provider: SuiClient,
            current_address: str, # SuiClient, # SuiAddress
            gas_budget: int,
            records: Records
            ):
        
        self.provider = provider
        self.current_address = current_address
        self.gas_budget = gas_budget
        self.records = records
    
    def create_pool(
            self,
            token_1: str,
            token_2: str,
            ticket_size: int,
            lot_size: int
    ):
        """
        Create pool for trading pair - 100 Sui fee

        :param token_1:
            Full coin type of the base asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::wbtc::WBTC"
        
        :param token_2:
            Full coin type of quote asset, eg: "0x3d0d0ce17dcd3b40c2d839d96ce66871ffb40e1154a8dd99af72292b3d10d7fc::usdt::USDT"

        :param ticket_size:
            Minimal Price Change Accuracy of this pool, eg: 10000000

        :param lot_size:
            Minimal Lot Change Accuracy of this pool, eg: 10000
        """

        txer = SuiTransaction(client)

        splits:list = txer.split_coin(coin=txer.gas, amounts=[100000000000])

        txer.move_call(

            target = "dee9::clob::create_pool",

            arguments = [ticket_size, lot_size, splits],

            type_arguments = [token_1, token_2]
    )
        return txer
    
    async def create_account(self, current_address) -> SuiTransaction:
        
        txer = SuiTransaction(client)

        cap: list = txer.move_call(

            target = "dee9::clob::create_account",

            arguments = [],

            type_arguments = []

        )

        txer.transfer_objects(
            transfers=[cap],
            recipient=current_address

        )

        return txer