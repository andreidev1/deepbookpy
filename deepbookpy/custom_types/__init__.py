from dataclasses import dataclass
from typing import Optional, Union, Any
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
    pay_with_deep: Optional[bool] = True


@dataclass
class PlaceMarketOrderParams:
    pool_key: str
    balance_manager_key: str
    client_order_id: str
    quantity: float
    is_bid: bool
    self_matching_option: Optional[SelfMatchingOptions] = None
    pay_with_deep: Optional[bool] = True


@dataclass
class PendingLimitOrderParams:
    client_order_id: str
    price: float
    quantity: float
    is_bid: bool
    order_type: Optional[OrderType] = None
    self_matching_option: Optional[SelfMatchingOptions] = None
    pay_with_deep: Optional[bool] = None
    expire_timestamp: Optional[Union[int, float]] = None


@dataclass
class PendingMarketOrderParams:
    client_order_id: str
    quantity: float
    is_bid: bool
    self_matching_option: Optional[SelfMatchingOptions] = None
    pay_with_deep: Optional[bool] = None


@dataclass
class AddConditionalOrderParams:
    margin_manager_key: str
    conditional_order_id: str
    trigger_below_price: bool
    trigger_price: int | float
    pending_order: Union[PendingLimitOrderParams, PendingMarketOrderParams]


@dataclass
class SwapParams:
    pool_key: str
    amount: float
    deep_amount: float
    min_out: float
    deep_coin: Optional["TransactionObjectArgument"] = None
    base_coin: Optional["TransactionObjectArgument"] = None
    quote_coin: Optional["TransactionObjectArgument"] = None


@dataclass
class CreatePermissionlessPoolParams:
    base_coin_key: str
    quote_coin_key: str
    tick_size: int
    lot_size: int
    min_size: int
    deep_coin: Optional["TransactionObjectArgument"] = None

@dataclass
class MarginManagers:
    address: str
    pool_key: str

@dataclass
class DepositParams:
    """
    Parameters for depositing into a margin manager.
    Either `amount` (int) or `coin` (transaction argument) must be provided, but not both.
    """
    manager_key: str
    amount: Optional[Union[int, float]] = None
    coin: Optional[Any] = None

    def __post_init__(self):
        if self.amount is None and self.coin is None:
            raise ValueError("Either 'amount' or 'coin' must be provided.")
        if self.amount is not None and self.coin is not None:
            raise ValueError("Only one of 'amount' or 'coin' can be provided, not both.")    
        
@dataclass
class DepositDuringInitParams:
    """
    Parameters for depositing during margin manager initialization.
    Either `amount` (int) or `coin` (transaction argument) must be provided, but not both.
    `coin_type` should be a coin key from config (e.g., 'SUI', 'DBUSDC', 'DEEP').
    """
    manager: Any
    pool_key: str
    coin_type: str
    amount: Optional[Union[int, float]] = None
    coin: Optional[Any] = None

    def __post_init__(self):
        if self.amount is None and self.coin is None:
            raise ValueError("Either 'amount' or 'coin' must be provided.")
        if self.amount is not None and self.coin is not None:
            raise ValueError("Only one of 'amount' or 'coin' can be provided, not both.")