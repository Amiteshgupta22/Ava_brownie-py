from brownie import (accounts, network, config)
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
FORK_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork"]
def get_account(index = None , id=None):
    if index:
        # its obvious that index is passed when Im on a development or local network or forked
        return accounts[index]
    if id:
        return accounts.load(id)  

    # print(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS)
    # print(network.show_active() in FORK_BLOCKCHAIN_ENVIRONMENTS)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORK_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])