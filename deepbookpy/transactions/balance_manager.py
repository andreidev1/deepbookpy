
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64
from pysui.sui.sui_types.address import SuiAddress

class BalanceManagerContract:
    def __init__(self, config):
        """
        BalanceManagerContract class for managing BalanceManager operations

        :param config: Configuration for BalanceManagerContract
        """
        self.__config = config

    def create_and_share_balance_manager(self, tx: SuiTransaction) -> SuiTransaction:
        """
        Create and share a new BalanceManager
        
        :return: SuiTransaction object
        """
        
        manager = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::new",
            arguments=[]
        )

        tx.move_call(
            target = "0x2::transfer::public_share_object",
            arguments=[manager],
            type_arguments=[f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::BalanceManager"]
        )


        return tx
    
    def deposit_into_manager(self, manager_key: str, coin_key: str, amount_to_deposit: int, coin_object: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Deposit funds into the BalanceManager

        :param manager_key: key of the BalanceManager
        :param coin_key: key of the coin to deposit
        :param amount_to_deposit: amount to deposit
        :param coin_object: coin object ID
        :return: SuiTransaction object
        """

        manager_id = self.__config.get_balance_manager(manager_key)['address']
        coin = self.__config.get_coin(coin_key)
        deposit_input = round(amount_to_deposit * coin["scalar"])

        deposit = tx.split_coin(coin=coin_object, amounts=[deposit_input])

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::deposit",
            arguments=[ObjectID(manager_id), deposit],
            type_arguments=[coin["type"]]
        )

        return tx
    
    def withdraw_from_manager(self, manager_key: str, coin_key: str, amount_to_withdraw: int | float, recipient: SuiAddress, tx) -> SuiTransaction:
        """
        Withdraw funds from BalanceManager

        :param manager_key: key of the BalanceManger
        :param coin_key: key of the coin to withdraw
        :param amount_to_withdraw: amount to withdraw
        :param recipient: recipient of the withdrawn funds
        :return: SuiTransaction object
        """

        manager_id = self.__config.get_balance_manager(manager_key)['address']
        coin = self.__config.get_coin(coin_key)
        withdraw_input = round(amount_to_withdraw * coin["scalar"])

        coin_object = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::withdraw",
            arguments=[ObjectID(manager_id), SuiU64(withdraw_input)],
            type_arguments=[coin["type"]]
        )
     
        tx.transfer_objects(transfers=[coin_object], recipient=SuiAddress(recipient))

        return tx
    

    def withdraw_all_from_manager(self, manager_key: str, coin_key: str, recipient: str, tx: SuiTransaction,) -> SuiTransaction:
        """
        Withdraw all funds from BalanceManager

        :param manager_key: key of the BalanceManger
        :param coin_key: key of the coin to withdraw
        :param recipient: recipient of the withdrawn funds
        :return: SuiTransaction object
        """

        manager_id = self.__config.get_balance_manager(manager_key)['address']
        coin = self.__config.get_coin(coin_key)
        
        coin_object = tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::withdraw_all",
            arguments=[ObjectID(manager_id)],
            type_arguments=[coin["type"]]
        )

        tx.transfer_objects(transfers=[coin_object], recipient=SuiAddress(recipient))

        return tx
    
    def check_manager_balance(self, manager_key: str, coin_key: str, tx : SuiTransaction) -> SuiTransaction:
        """
        Check the balance of the BalanceManager

        :param manager_key: key of the BalanceManger
        :param coin_key: key of the coin to check the balance of
        :return: SuiTransaction object
        """
        
        manager_id = self.__config.get_balance_manager(manager_key)["address"]
        coin = self.__config.get_coin(coin_key)

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::balance",
            arguments=[ObjectID(manager_id)],
            type_arguments=[coin["type"]]
        )

    def generate_proof(self, manager_key: str) -> SuiTransaction:
        """
        Generate a trade proof for the BalanceManager. Calls the appropriate function based on whether trade_cap is set.

        :param manager_key: key of the BalanceManager
        :return: SuiTransaction object
        """

        balance_manager = self.__config.get_balance_manager(manager_key)

        def generate_proof_as_trader(trade_cap_id, tx):
            return self.generate_proof_as_trader(balance_manager["address"], trade_cap_id)(tx)

        def generate_proof_as_owner(tx):
            return self.generate_proof_as_owner(balance_manager["address"])(tx)
        
        if balance_manager["trade_cap"]:
            return generate_proof_as_trader
        else:
            return generate_proof_as_owner

    
    def generate_proof_as_owner(self, manager_id: str) -> SuiTransaction:
        """
        Generate a trade proof as the owner

        :param manager_id: ID of the BalanceManager
        :return: SuiTransaction object
        """
        def generate_proof_as_owner(tx):
            return tx.move_call(
                target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::generate_proof_as_owner",
                arguments=[ObjectID(manager_id)]
        )

        return generate_proof_as_owner
    
    def generate_proof_as_trader(self, manager_id: str, trade_cap_id: str) -> SuiTransaction:
        """
        Generate a trade proof as a trader

        :param manager_id: ID of the BalanceManger
        :param trade_cap_id: ID of the TradeCap
        :return: SuiTransaction object
        """
        
        def generate_proof_as_trader(tx):
            tx.move_call(
                target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::generate_proof_as_trader",
                arguments=[ObjectID(manager_id), ObjectID(trade_cap_id)]
            )

        return generate_proof_as_trader
    
    def owner(self, manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the owner of the BalanceManager

        :param manager_id: key of the BalanceManager
        :return: SuiTransaction object
        """

        manager_id = self.__config.get_balance_manager(manager_key)['address']

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::owner",
            arguments=[ObjectID(manager_id)]
        )

        return tx
    
    def id(self, manager_key: str, tx: SuiTransaction) -> SuiTransaction:
        """
        Get the ID of the BalanceManager

        :param manager_id: key of the BalanceManager
        :return: SuiTransaction object
        """

        manager_id = self.__config.get_balance_manager(manager_key)['address']

        tx.move_call(
            target = f"{self.__config.DEEPBOOK_PACKAGE_ID}::balance_manager::id",
            arguments=[ObjectID(manager_id)]
        )

        return tx