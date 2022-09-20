from brownie import (
    accounts,
    network,
    config,
    VRFCoordinatorMockV2,
    LinkToken,
    interface,
    Contract,
)
from web3 import Web3

LOCAL_DEVELOPMENT_NETWORKS = ["development", "local-ganache"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
pug_uri = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
##"https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png"


def get_account(index=None, account_name=None):
    if index:
        return accounts[index]
    if account_name:
        return accounts.load(account_name)
    if (
        network.show_active() in LOCAL_DEVELOPMENT_NETWORKS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        contract_to_mock = {"vrf_coordinator": VRFCoordinatorMockV2, "link": LinkToken}
        contract_type = contract_to_mock[contract_name]
        if len(contract_type) > 0:
            contract = contract_type[-1]
        else:
            contract = deploy_mocks(contract_type)
        return contract.address
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        ##link_contract = interface.LinkTokenInterface(contract_address)
        ##vrf_contract = interface.VRFCoordinator  ##get vrf coordinator v1 interface
        return contract_address


def deploy_mocks(contract):
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    vrf_mock = VRFCoordinatorMockV2.deploy(
        config["networks"][network.show_active()]["fee"], 250000, {"from": account}
    )
    if contract == LinkToken:
        print("deployed link mock!")
        return link_token
    else:
        print("deployed vrf mock!!")
        return vrf_mock


def fund_with_link(toAddress, amount, link_token, account):
    if account:
        account = account
    else:
        account = get_account()

    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        if len(LinkToken) > 0:
            link_token = LinkToken[-1]
            tx = link_token.transfer(toAddress, amount, {"from": account})
            tx.wait(1)
        else:
            link_token = LinkToken.deploy({"from": account})
            tx1 = link_token.transfer(toAddress, {"from": account})
            tx1.wait(1)
    else:
        if link_token:
            link_token = link_token
        else:
            link_token = interface.LinkTokenInterface(get_contract("link"))
            tx2 = link_token.transfer(toAddress, amount, {"from": account})
            tx2.wait(1)
    print("Yeah funded with link!")


def add_consumer_contract(contract_address, sId):
    account = get_account()
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        coordinator = VRFCoordinatorMockV2[-1]
        ##creating subscription
        tx = coordinator.createSubscription({"from": account})
        subId = tx.events["SubscriptionCreated"]["subId"]
        print(f"Yeah created subscription of id {subId}")
        ##funding the subscription with some link
        amount = Web3.toWei(0.2, "ether")
        coordinator.fundSubscription(subId, amount)
        ##adding the contract as consumer
        coordinator.addConsumer(subId, contract_address, {"from": account})
        print("Yeah contract added as VRF Consumer...")
    else:
        coordinator = interface.VRFCoordinatorV2Interface(
            config["networks"][network.show_active()]["vrf_coordinator"]
        )
        tx = coordinator.addConsumer(sId, contract_address, {"from": account})
        tx.wait(1)
        print("Contract added to Consumers list successfully....")
