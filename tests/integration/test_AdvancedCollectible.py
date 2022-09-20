from brownie import network
from scripts.AdvancedCollectible.deploy_and_create_nft import deploy_and_create_nft
from scripts.helpful_scripts import LOCAL_DEVELOPMENT_NETWORKS
import pytest


def test_can_deploy_and_create_advanced():
    ##arrange
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip()
    ##act
    collectible, tx = deploy_and_create_nft()
    ##assert
    assert collectible.tokenCounter() == 1
