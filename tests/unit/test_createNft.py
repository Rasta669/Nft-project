from brownie import nftDogie, network, accounts
from scripts.helpful_scripts import LOCAL_DEVELOPMENT_NETWORKS, get_account, pug_uri
import pytest


def test_createNft():
    if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip()
    ##arrange
    account2 = accounts[1]
    account = get_account()
    dogg = nftDogie.deploy({"from": account})
    ##act
    tx = dogg.createNft(pug_uri, {"from": account})
    tx.wait(1)
    ##assert to fail @dev you may comment any for the other assert test to take place, no 2 asserts can be implemented on the same test fx
    with pytest.raises(AssertionError):
        assert dogg.ownerOf(dogg.NftId()) == account2
    ##assert to pass
    assert dogg.ownerOf(dogg.NftId()) == account
