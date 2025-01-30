from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.scalars import ObjectID, SuiU64, SuiU8, SuiBoolean
from pysui.sui.sui_types.address import SuiAddress


from deepbookpy.utils.config import DeepBookConfig, DEEP_SCALAR, FLOAT_SCALAR
from deepbookpy.custom_types import ProposalParams

class GovernanceContract:
    def __init__(self, config: DeepBookConfig):
        """
        GovernanceContract class for managing governance operations in DeepBook

       
        :param config: Configuration for GovernanceContract
        """
        self.__config = config

    def stake(self, tx: SuiTransaction, pool_key:str, balance_manager_key: str, stake_amount: int) -> SuiTransaction:
        """
        Stake a specified amount in the pool

        :pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager
        :param stake_amount: amount to stake
        """

        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        
        #TO DO
        trade_proof = ""


        base_coin = self.__config.get_coin(pool.base_coin)
        quote_coin = self.__config.get_coin(pool.quote_coin)
        stake_input = round(stake_amount * DEEP_SCALAR)


        tx.move_call(
            target=f"{self._config.DEEPBOOK_PACKAGE_ID}::pool::stake",
            arguments=
            [
                ObjectID(pool.address), 
                ObjectID(balance_manager.address),
                trade_proof,
                SuiU64(stake_input)
            ],
            type_arguments=[base_coin.type, quote_coin.type]
        )

        return tx
    
    def unstake(self, tx: SuiTransaction, pool_key:str, balance_manager_key: str) -> SuiTransaction:
        """
        Unstake a specified amount from the pool

        :pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManager

        """

        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        
        #TO DO
        trade_proof = ""


        base_coin = self.__config.get_coin(pool.base_coin)
        quote_coin = self.__config.get_coin(pool.quote_coin)


        tx.move_call(
            target=f"{self._config.DEEPBOOK_PACKAGE_ID}::pool::unstake",
            arguments=
            [
                ObjectID(pool.address), 
                ObjectID(balance_manager.address),
                trade_proof,
            ],
            type_arguments=[base_coin.type, quote_coin.type]
        )

        return tx
    
    def submit_proposal(self, tx: SuiTransaction, params: ProposalParams) -> SuiTransaction:
        """
        Submit a governance proposal

        :param params: Parameters for the proposal

        """
        pool_key = params.pool_key
        balance_manager_key = params.balance_manager_key
        taker_fee = params.taker_fee
        maker_fee = params.maker_fee
        stake_required = params.stake_required

        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        
        #TO DO
        trade_proof = ""


        base_coin = self.__config.get_coin(pool.base_coin)
        quote_coin = self.__config.get_coin(pool.quote_coin)


        tx.move_call(
            target=f"{self._config.DEEPBOOK_PACKAGE_ID}::pool::submit_proposal",
            arguments=
            [
                ObjectID(pool.address), 
                ObjectID(balance_manager.address),
                trade_proof,
                SuiU64(round(taker_fee * FLOAT_SCALAR)),
                SuiU64(round(maker_fee * FLOAT_SCALAR)),
                SuiU64(round(stake_required * DEEP_SCALAR)),
            ],
            type_arguments=[base_coin.type, quote_coin.type]
        )

        return tx
    

    def vote(self, tx: SuiTransaction, pool_key: str, balance_manager_key: str, proposal_id: str) -> SuiTransaction:
        """
        Vote on a proposal


        :param pool_key: key to identify the pool
        :param balance_manager_key: key to identify the BalanceManger
        :param proposal_id: ID of the proposal to vote on

        """
        pool = self.__config.get_pool(pool_key)
        balance_manager = self.__config.get_balance_manager(balance_manager_key)
        

        #TO DO
        trade_proof = ""


        base_coin = self.__config.get_coin(pool.base_coin)
        quote_coin = self.__config.get_coin(pool.quote_coin)


        tx.move_call(
            target=f"{self._config.DEEPBOOK_PACKAGE_ID}::pool::vote",
            arguments=
            [
                ObjectID(pool.address), 
                ObjectID(balance_manager.address),
                trade_proof,
                ObjectID(proposal_id)
            ],
            type_arguments=[base_coin.type, quote_coin.type]
        )

        return tx
    