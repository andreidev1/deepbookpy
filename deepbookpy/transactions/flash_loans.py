from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64

from deepbookpy.utils.config import DeepBookConfig

class FlashLoanContract:
    def __init__(self, config: DeepBookConfig):
        """
        FlashLoanContract class for managing flash loans.

       
        :param config: Configuration object for DeepBook
        """
        self.__config = config

    def borrow_base_asset(self, pool_key: str, borrow_amount: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Borrow base asset from the pool

        :param pool_key: key to identify the pool
        :param borrow_amount: the amount to borrow
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(borrow_amount * base_coin["scalar"])

        base_coin_result, flash_loan = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::borrow_flashloan_base",
            arguments=[ObjectID(pool['address']), SuiU64(input_quantity)],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return [base_coin_result, flash_loan]
    
    def return_base_asset(self, pool_key: str, borrow_amount: int, base_coin_input: str, flash_loan: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Return base asset to the pool after a flash loan.

        :param pool_key: key to identify the pool
        :param borrow_amount: the amount of the base asset to return
        :param base_coin_input: the base coin to be queried
        :param flash_loan: flash loan
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        borrow_scalar = base_coin["scalar"]

        base_coin_return = tx.split_coin(coin=base_coin_input, amounts=[round(borrow_amount * borrow_scalar)])
        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::return_flashloan_base",
            arguments=[ObjectID(pool['address']), base_coin_return, flash_loan],
            type_arguments=[base_coin['type'], quote_coin['type']],
        )

        return base_coin_input
    

    def borrow_quote_asset(self, pool_key: str, borrow_amount: int, tx: SuiTransaction) -> SuiTransaction:
        """
        Borrow quote asset from the pool

        :param pool_key: key to identify the pool
        :param borrow_amount: the amount to borrow
        :return: SuiTransaction object
        """
        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        input_quantity = round(borrow_amount * quote_coin["scalar"])

        [quote_coin_result, flash_loan] = tx.move_call(
            target=f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::borrow_flashloan_quote",
            arguments=[ObjectID(pool['address']), SuiU64(input_quantity)],
            type_arguments=[base_coin['type'], quote_coin['type']]
        )

        return [quote_coin_result, flash_loan]
    

    def return_quote_asset(self, pool_key:str, borrow_amount: int, quote_coin_input: str, flash_loan: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Return quote asset to the pool after a flash loan.

        :pool_key: key to identify the pool
        :param borrow_amount: the amount of the quote asset to return
        :parram quote_coin_input: Coin object
        :param flash_loan:  FlashLoan object
        :return: SuiTransaction object
        """

        pool = self.__config.get_pool(pool_key)
        base_coin = self.__config.get_coin(pool['base_coin'])
        quote_coin = self.__config.get_coin(pool['quote_coin'])
        borrow_scalar = quote_coin["scalar"]

        quote_coin_return = tx.split_coin(coin=quote_coin_input, amounts=[round(borrow_amount * borrow_scalar)])

        tx.move_call(
            target=f"{self.__config.DEEPBOOK_PACKAGE_ID}::pool::return_flashloan_quote",
            arguments=[ObjectID(pool['address']), quote_coin_return, flash_loan],
            type_arguments=[base_coin['type'], quote_coin['type']]
        )

        return quote_coin_input