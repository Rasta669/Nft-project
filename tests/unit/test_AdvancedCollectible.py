from brownie import network, VRFCoordinatorV2Mock
from scripts.AdvancedCollectible import deploy_and_create_nft
from scripts.helpful_scripts import (
    LOCAL_DEVELOPMENT_NETWORKS,
    get_account,
    get_contract,
)
import pytest


def test_can_create_and_deploy():
    ##arrange
    account = get_account()
    if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip()
    ##act
    (collectible, tx) = deploy_and_create_nft()
    request_id = tx.events["requestedNft"]["requestId"]
    coordinator = VRFCoordinatorV2Mock(get_contract("vrf_coordinator"))

    tx1 = coordinator.callBackWithRandomness(
        request_id, 777, collectible.address, {"from": account}
    )
    tx1.wait(1)
    ##assert
    assert collectible.tokenCounter == 1
    assert collectible.ownerToBreed(0) == "pug"
