def convert_quantity(value: int | float, scalar: int) -> int:
    """
    Convert a quantity value (amount, deposit, etc.) to on-chain u64.
    If int: use as raw on-chain value.
    If float: scale with round.
    """
    return value if isinstance(value, int) else int(round(value * scalar))


def convert_price(
    value: int | float,
    float_scalar: int,
    quote_scalar: int,
    base_scalar: int,
) -> int:
    """
    Convert a price value to on-chain u64.
    If int: use as raw on-chain value.
    If float: scale with cross-scalar formula.
    """
    return (
        value
        if isinstance(value, int)
        else int(round((value * float_scalar * quote_scalar) / base_scalar))
    )


def convert_rate(value: int | float, float_scalar: int) -> int:
    """
    Convert a rate/fee value to on-chain u64.
    If int: use as raw on-chain value.
    If float: scale with float_scalar.
    """
    return value if isinstance(value, int) else int(round(value * float_scalar))