from dataclasses import dataclass, Optional


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
