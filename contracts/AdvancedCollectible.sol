// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

//import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    bytes32 keyHash;
    //v2 shit
    VRFCoordinatorV2Interface COORDINATOR;
    uint64 s_subscriptionId;
    uint32 callbackGasLimit = 2500000;
    uint16 requestConfirmations = 3;
    uint32 numWords = 2;
    uint256[] public s_randomWords;
    uint256 fee; //v1 shit
    uint256 public recent_randomness;
    uint256 public requestId;
    mapping(uint256 => address) requestIdtoTokenOwner;
    event requestedNft(uint256 indexed requestId, address requester);
    string[] public breed = ["pug", "shiba - inu", "st - bernard"];
    mapping(uint256 => string) public TokenIdToBreed;
    event breedAssigned(string indexed breed, uint256);

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint64 sId //uint256 _fee
    ) public ERC721("DG", "DOGIE") VRFConsumerBaseV2(_vrfCoordinator) {
        tokenCounter = 0;
        keyHash = _keyHash;
        s_subscriptionId = sId;
        //fee = _fee;
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
    }

    function createCollectible() public returns (uint256) {
        address owner = msg.sender;
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        //requestId = requestRandomness(keyHash, fee);
        requestIdtoTokenOwner[requestId] = owner;
        emit requestedNft(requestId, owner);
        return requestId;
    }

    //function fulfillRandomness(uint256 requestId, uint256 randomness) internal virtual override {
    //recent_randomness = randomness;
    //} vi shit

    function fulfillRandomWords(
        uint256, /* requestId */
        uint256[] memory randomWords
    ) internal override {
        s_randomWords = randomWords;
        recent_randomness = s_randomWords[0];
        string memory chosenBreed = breed[recent_randomness % 3];
        uint256 tokenId = tokenCounter;
        address owner = requestIdtoTokenOwner[requestId];
        _safeMint(owner, tokenId);
        tokenCounter++;
        TokenIdToBreed[tokenId] = chosenBreed;
        emit breedAssigned(chosenBreed, tokenId);
    }

    // should be onlyowner fx- require statements
    //function getBreed() public {}

    function setTokenUri(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(msg.sender, tokenId) == true,
            "Sorry you aint the onwer of this tokenId.."
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
