from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    add_consumer_contract,
)
from web3 import Web3
import time


def main():
    deploy_and_create_nft()
    read_data()
    ##publish_on_etherscan()
    create_collectible()
    ##get_breed()
    read_data()


def deploy_and_create_nft():
    account = get_account()
    collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link"),
        config["networks"][network.show_active()]["keyhash"],
        686,
        ##config["networks"][network.show_active()]["fee"],
        {"from": account},
        ##publish_source=True,
    )
    ##fund_with_link(collectible.address, Web3.toWei(0.2, "ether"), None, None)
    ##adding the contract as a consumer of vrf v2 to receive randomness
    add_consumer_contract(collectible.address, 686)
    tx = collectible.createCollectible({"from": account})
    tx.wait(1)
    time.sleep(150)
    print("Yeay deployed and created a collectible")
    return collectible, tx


def create_collectible():
    account = get_account()
    collectible = AdvancedCollectible[-1]
    ##fund_with_link(collectible.address, Web3.toWei(0.2, "ether"), None, None)
    tx = collectible.createCollectible({"from": account})
    tx.wait(1)
    time.sleep(150)
    print("Yeay created a collectible!!")


def get_breed():
    account = get_account()
    collectible = AdvancedCollectible[-1]
    tx = collectible.getBreed({"from": account})
    tx.wait(1)


def publish_on_etherscan():
    collectible = AdvancedCollectible[-1]
    AdvancedCollectible.publish_source(collectible)


def read_data():
    ##account = get_account()
    collectible = AdvancedCollectible[-1]
    tokenId = collectible.tokenCounter() - 1
    print(f"the token counter of the former nft is {tokenId}")
    print(f"the recent randomness is {collectible.recent_randomness()}")
    print(f"the token breed of the former nft is {collectible.TokenIdToBreed(tokenId)}")
