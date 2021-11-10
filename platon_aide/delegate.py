from platon import Web3

from economic import gas
from main import Module
from utils import contract_transaction
from staking import Staking


class Delegate(Module):

    def __init__(self, web3: Web3):
        super().__init__(web3)
        self._get_node_info()

    @property
    def _staking_block_number(self):
        staking = Staking(self.web3)
        return staking.staking_info.StakingBlockNum

    @contract_transaction
    def delegate(self,
                 amount=None,
                 balance_type=0,
                 node_id=None,
                 txn=None,
                 private_key=None,
                 ):
        """ 委托节点，以获取节点的奖励分红
        """
        amount = amount or gas.Delegate_limit
        node_id = node_id or self.node_id
        return self.web3.ppos.delegate.delegate(node_id, balance_type, amount)

    @contract_transaction
    def withdrew_delegate(self,
                          amount=0,
                          staking_block_identifier=None,
                          node_id=None,
                          txn=None,
                          private_key=None,
                          ):
        """
        撤回对节点的委托，可以撤回部分委托
        注意：因为节点可能进行过多次质押/撤销质押，会使得委托信息遗留，因此撤回委托时必须指定节点质押区块
        """
        node_id = node_id or self.node_id
        amount = amount or gas.Delegate_limit
        staking_block_identifier = staking_block_identifier or self._staking_block_number

        return self.web3.ppos.delegate.withdrew_delegate(node_id,
                                                         staking_block_identifier,
                                                         amount,
                                                         )

    def get_delegate_info(self,
                          address=None,
                          node_id=None,
                          staking_block_identifier=None,
                          ):
        """ 获取地址对某个节点的某次质押的委托信息
        注意：因为节点可能进行过多次质押/撤销质押，会使得委托信息遗留，因此获取委托信息时必须指定节点质押区块
        """
        if self.default_account:
            address = address or self.default_account.address
        node_id = node_id or self.node_id
        staking_block_identifier = staking_block_identifier or self._staking_block_number

        return self.web3.ppos.delegate.get_delegate_info(address, node_id, staking_block_identifier)

    def get_delegate_list(self, address=None):
        """ 获取地址的全部委托信息
        """
        if self.default_account:
            address = address or self.default_account.address
        return self.web3.ppos.delegate.get_delegate_list(address)

    @contract_transaction
    def withdraw_delegate_reward(self,
                                 txn=None,
                                 private_key=None,
                                 ):
        """ 提取委托奖励，会提取委托了的所有节点的委托奖励
        """
        return self.web3.ppos.delegate.withdraw_delegate_reward()

    def get_delegate_reward(self,
                            address=None,
                            node_ids=None
                            ):
        """ 获取委托奖励信息，可以根据节点id过滤
        """
        if self.default_account:
            address = address or self.default_account.address
        return self.web3.ppos.delegate.get_delegate_reward(address, node_ids)
