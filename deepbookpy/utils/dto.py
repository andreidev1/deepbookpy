from dataclasses import dataclass
from typing import List


@dataclass
class Pool:
    clob: str 
    type: str
    price_decimals: int
    amount_decimals: int
    ticket_size: int


@dataclass
class PoolInfo:
    need_change: bool
    clob: str
    type: str
    ticket_size: int

@dataclass
class Token:
    symbol: str
    type: str
    decimals: int


@dataclass
class Cap:
    owner: str
    cap: str


@dataclass
class Records:
    pools: Pool[List]
    tokens: Token[List]
    caps: Cap[List]
