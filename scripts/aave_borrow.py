zfrom brownie import config, network,interface
from scripts.helpful_script import get_account
from scripts.get_weth import get_weth
from web3 import Web3

def main():
    amount= Web3.toWei(0.1,"ether")
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()
    print("lending pool deployed !")
    approve(erc20_address,lending_pool.address, account,amount)
    print("Transaction is approved")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address,0, {"from": account}
    )
    
    tx.wait(1)
    print("Deposited !")
    borrow_data,collatoral_data,debt_data = get_borrowable_data(lending_pool,account)
    print("borrowable data is:", borrow_data)
    print("collatoral data is:", collatoral_data)
    print("let's borrow some dai!")
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["price_feed"])
    # in eth
    tx = lending_pool.borrow(config["networks"][network.show_active()]["dai_token"],
    borrow_data*(0.95),1,
    0,
    account, {"from":account})
    tx.wait(1)
    print("Hurrah! you have borrowed some eth")

 
    borrow_data_new,collatoral_data_new,debt_data_new = get_borrowable_data(lending_pool,account)
    print(f"Your can borrow {borrow_data_new} amount")
    print(f"Your collatoral is {collatoral_data_new}")
    
    repay_all(lending_pool,config["networks"][network.show_active()]["dai_token"],Web3.toWei(dai_eth_price,"ether"),account)




def get_asset_price(pricefeed):
    diapricefeed = interface.AggregatorV3Interface(pricefeed)
    price = diapricefeed.latestRoundData()[1]
    price_dai = price/(10**18)
    return float(price_dai)

def repay_all(lending_pool,asset, amount,account):
    approve(asset,lending_pool,account,amount)
    tx.wait(1)
    print("You have approved for repay !")
    tx = lending_pool.repay(asset,amount,account, {"from": account})
    tx.wait(1)
    print("You have repaied all teh loan !")


def get_borrowable_data(lending_pool , account):
    (totalCollateralETH,totalDebtETH,availableBorrowsETH,current_liquidation_threshold,
        ltv,
        health_factor) = lending_pool.getUserAccountData(account)
    borrow_data = Web3.fromWei(availableBorrowsETH,"ether")
    collatoral_data = Web3.fromWei(totalCollateralETH,"ether")
    debt_data = Web3.fromWei(totalDebtETH,"ether")

    # float is because when you will multiply it with 0.95 then it wont get if not float
    return float(borrow_data),float(collatoral_data),float(debt_data)



def approve(erc_token_address, lending_pool_address, account, amount):
    # ammount= Web3.fromWei(0.1,"ether")
    erca_20 = interface.IERC20(erc_token_address)
    tx = erca_20.approve(lending_pool_address, amount,  {"from": account})
    tx.wait(1)
    


def get_lending_pool():
    lending_pool_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]
    ["lending_pool_addresses_provider"])
    # it will give you the LendingPooladdressContract
    lending_pool_address = lending_pool_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    