from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 18
STARTING_ETH_USD = 2000
BLOCKCHAINS_WITH_BUILTIN_ACCOUNTS = [
    "development",
    "ganache-local",
    "kovan-fork-alchemy",
    "rinkeby-fork-alchemy",
    "goerli-fork-alchemy",
    "ropsten-fork-alchemy",
    "mainnet-fork-alchemy",
]
BLOCKCHAINS_WITH_ETHUSD_FEED = [
    "kovan-fork-alchemy",
    "rinkeby-fork-alchemy",
    "mainnet-fork-alchemy",
    "rinkeby",
    "kovan",
    "mainnet",
]


def get_account():
    # 127.0.0.1:8545 first account (Ganache)
    # return accounts[0]

    # Brownie encrypted account
    # return accounts.load("metamask-ropsten-account")

    # From .env private key
    # return accounts.add(os.getenv("PRIVATE_KEY"))

    # From the yaml Brownie config
    # return accounts.add(config["wallets"]["from_key"])

    if network.show_active() in BLOCKCHAINS_WITH_BUILTIN_ACCOUNTS:
        return accounts[0]
    else:
        return accounts.load("metamask-testnet-account")


def deployMocks():
    if len(MockV3Aggregator) <= 0:
        print("Deploying Mock...")
        MockV3Aggregator.deploy(
            DECIMALS,
            Web3.toWei(STARTING_ETH_USD, "ether"),
            {"from": get_account()},
        )
        print("Mock deployed!")


def get_eth_usd_feed_address():
    network_name = network.show_active()
    if network_name in BLOCKCHAINS_WITH_ETHUSD_FEED:
        eth_usd_feed_address = config["networks"][network.show_active()]["eth_usd_feed"]
    else:
        deployMocks()
        eth_usd_feed_address = MockV3Aggregator[-1].address
    return eth_usd_feed_address
