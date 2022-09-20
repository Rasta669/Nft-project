from brownie import nftDogie, config
from scripts.helpful_scripts import get_account, OPENSEA_URL, pug_uri


def deploy_and_create_nft():
    account = get_account()
    dogg = nftDogie.deploy({"from": account})
    tx = dogg.createNft(pug_uri)
    tx.wait(1)
    ##publishing our nft on opensea testnet
    print(
        f"awesome!!now you can view your nft at {OPENSEA_URL.format(dogg.address, dogg.NftId())}"
    )
    print(f"the nft balance of {account} is {dogg.balanceOf(account)}")
    print(f"{account} owns nft of id {dogg.NftId()}")


def main():
    deploy_and_create_nft()
