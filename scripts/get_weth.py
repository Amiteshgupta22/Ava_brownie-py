from brownie import interface,network,config
from scripts.helpful_script import get_account
def get_weth():
    account = get_account()
    # in python youa are not required to declare type 
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1*10**18 })
    tx.wait(1)
    print("Recieved WETH")
    return tx


def main():
    get_weth()