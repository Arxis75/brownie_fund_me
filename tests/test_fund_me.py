from brownie import network, accounts, web3, exceptions
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account, BLOCKCHAINS_WITH_BUILTIN_ACCOUNTS
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in BLOCKCHAINS_WITH_BUILTIN_ACCOUNTS:
        pytest.skip("only for local testing")

    fund_me = deploy_fund_me()

    # By default, a network with built-in accounts starts with 10 funded accounts [0..9]; 0 is the legitimate owner, 9 an arbitrary bad actor
    bad_actor = accounts[9]
    with pytest.raises(exceptions.VirtualMachineError):
        block = web3.eth.get_block("latest")
        fund_me.withdraw(
            {
                "from": bad_actor,
                "gas_limit": block.gasLimit,
                "allow_revert": True,
            }
        )


"""
def main():
    test_can_fund_and_withdraw()
    test_only_owner_can_withdraw()


"""
