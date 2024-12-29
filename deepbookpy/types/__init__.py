from dataclasses import dataclass


@dataclass
class LimitOrderType:
    """Type of restriction for a limit order"""

    # Fill as much quantity as possible in the current transaction as taker, and inject the remaining as a maker order.
    NO_RESTRICTION = 0

    # Fill as much quantity as possible in the current transaction as taker, and cancel the rest of the order.
    IMMEDIATE_OR_CANCEL = 1

    # Only fill if the entire order size can be filled as taker in the current transaction. Otherwise, abort the entire transaction.
    FILL_OR_KILL = 2

    # Only proceed if the entire order size can be posted to the order book as maker in the current transaction. Otherwise, abort the entire transaction.
    POST_OR_ABORT = 3


@dataclass
class SelfMatchingPreventionStyle:
    """Matching prevention style"""

    # Cancel older (resting) order in full. Continue to execute the newer taking order.
    CANCEL_OLDEST = 0

@dataclass
class Coin:
    address: str,
    type: str,
    scalar: int

@dataclass
class Pool:
    address: str,
    base_coin: str,
    quote_coin: str