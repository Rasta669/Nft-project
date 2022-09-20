// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract nftDogie is ERC721 {
    uint256 counter;
    uint256 public NftId;

    constructor() public ERC721("DOGIE", "DG") {
        counter = 0;
    }

    function createNft(string memory _tokenURI) public returns (uint256) {
        NftId = counter;
        //minting an nft to the sender of this fx
        _safeMint(msg.sender, NftId);
        //setting the tokenuri containing the metadata of the nft
        _setTokenURI(NftId, _tokenURI);
        return NftId;
        counter++;
    }
}
