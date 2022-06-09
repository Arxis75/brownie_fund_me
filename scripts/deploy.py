from brownie import FundMe, network, config
from scripts.helpful_scripts import get_account, get_eth_usd_feed_address


def deploy_fund_me():
    if len(FundMe) <= 0:
        fund_me = FundMe.deploy(
            get_eth_usd_feed_address(),
            {"from": get_account()},
            publish_source=config["networks"][network.show_active()]["publish"],
        )
    else:
        fund_me = FundMe[-1]
    return fund_me


def main():
    deploy_fund_me()
