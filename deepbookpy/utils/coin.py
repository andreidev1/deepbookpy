"""
A basic helper module implementation that aims to replicate CoinWithBalance intent functionality for making easy to get a coin object ID with highest balance.
If SUI is passed as coin_type then automatically will use txn.gas

TO DO : If the set of coins found have equal balance : use MergeCoins command and then SplitCoins command to create desired coin.
"""

from dataclasses import dataclass
import json
from typing import Union, List
import sys

from pysui import SuiRpcResult
from pysui.sui.sui_types import bcs, ObjectID
from pysui.sui.sui_txn.sync_transaction import SuiTransaction


SUI_COIN_TYPE = "0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI"

class InsufficientCoinsError(Exception):
    pass

@dataclass
class BalanceObject:
    object_id: str
    type: str
    balance: int


def wrap_coin_type(coin_type: str) -> str:
    """
    Util function to wrap coin type object
    :param coin_type: coin type
    :returns: wrapped coin type
    """
    return "0x2::coin::Coin<" + coin_type + ">"

def get_coin_object(sender_with_result: Union[SuiRpcResult, Exception], coin_type: str) -> Union[List[BalanceObject], InsufficientCoinsError]:
    """
    Get coin object

    :param sender_with_result: list of owned objects
    :param coin_type: coin type
    :returns: list of BalanceObject
    """
    filtered_objects = []

    try:
        if sender_with_result.is_ok():
            for owned_object in sender_with_result.result_data.data:
                r = json.loads(owned_object.to_json())

                wrapped_coin_type = wrap_coin_type(coin_type)

                if r["type"] == wrapped_coin_type and int(r["content"]["fields"]["balance"]) > 0:
                    filtered = {
                        "objectId": r["objectId"],
                        "type": r["type"],
                        "balance": int(r["content"]["fields"]["balance"])
                    }
                    filtered_objects.append(filtered)
        else:
            print(sender_with_result.result_string)
            sys.exit(1)

        if len(filtered_objects) == 0:
            raise InsufficientCoinsError(f"Not enough coins of type to satisfy {coin_type} requested balance")

        return filtered_objects

    except InsufficientCoinsError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        sys.exit(1)


def get_highest_object_balance(sender_with_result: Union[SuiRpcResult, Exception], coin_type: str) -> ObjectID:
    """
    Get coin object ID with highest balance that sender owns in his SUI wallet.
    
    :param sender_with_result: list of owned objects
    :param coin_type: coin type
    :returns: Object ID

    """
    highest_balance_object_id = max(get_coin_object(sender_with_result, coin_type), key=lambda x: x["balance"])

    return highest_balance_object_id


def coin_with_balance(sender_with_result: Union[SuiRpcResult, Exception], coin_type: str, amount: int, txn: SuiTransaction) -> Union[bcs.Argument, list[bcs.Argument]] :
    """
    A helper function that simulate basic functionality of coinsWithBalance() intent method from Transaction Plugin

    :param sender_with_result: list of owned objects
    :param coin_type: coin type
    :param txn: SuiTransaction object
    :returns: A result or list of results types to use in subsequent commands
    :rtype: Union[list[bcs.Argument],bcs.Argument]
    """

    # If coin_type is SUI, immediately split using txn.gas
    if coin_type == SUI_COIN_TYPE:
        return txn.split_coin(coin=txn.gas, amounts=amount)

    highest_balance_object_id = get_highest_object_balance(sender_with_result, coin_type)["objectId"]

    result = txn.split_coin(coin=highest_balance_object_id, amounts=amount)

    return result
