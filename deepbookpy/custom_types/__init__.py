from dataclasses import dataclass
from typing import Optional, Union
from enum import Enum


class SelfMatchingOptions(Enum):
    SELF_MATCHING_ALLOWED = 0
    CANCEL_TAKER = 1
    CANCEL_MAKER = 2


class OrderType(Enum):
    NO_RESTRICTION = 0
    IMMEDIATE_OR_CANCEL = 1
    FILL_OR_KILL = 2
    POST_ONLY = 3


@dataclass
class Coin:
    address: str
    type: str
    scalar: int

@dataclass
class Pool:
    address: str
    base_coin: str
    quote_coin: str

@dataclass
class CreatePoolAdminParams:
    base_coin_key: str
    quote_coin_key: str
    tick_size: int
    lot_size: int
    min_size: int
    whitelisted: bool
    stable_pool: bool
    deep_coin: Optional[object] = None
    base_coin: Optional[object] = None

@dataclass
class ProposalParams:
    pool_key: str
    balance_manager_key: str
    taker_fee: float
    maker_fee: float
    stake_required: int

@dataclass
class PlaceLimitOrderParams:
    pool_key: str
    balance_manager_key: str
    client_order_id: str
    price: float
    quantity: float
    is_bid: bool
    expiration: Optional[Union[int, float]] = None
    order_type: Optional[int] = None
    self_matching_option: Optional[SelfMatchingOptions] = None
    pay_with_deep: Optional[bool] = None

@dataclass
class PlaceMarketOrderParams:
    pool_key: str
    balance_manager_key: str
    client_order_id: str
    quantity: float
    is_bid: bool
    self_matching_option: Optional[SelfMatchingOptions] = None 
    pay_with_deep: Optional[bool] = None

@dataclass
class SwapParams:
    pool_key: str
    amount: float
    deep_amount: float
    min_out: float
    deep_coin: Optional['TransactionObjectArgument'] = None
    base_coin: Optional['TransactionObjectArgument'] = None
    quote_coin: Optional['TransactionObjectArgument'] = None


@dataclass
class CreatePermissionlessPoolParams:
    base_coin_key: str
    quote_coin_key: str
    tick_size: int
    lot_size: int
    min_size: int
    deep_coin: Optional['TransactionObjectArgument'] = None