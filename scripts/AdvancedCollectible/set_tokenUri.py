from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, OPENSEA_URL

breedToImageUri = {
    "pug": "https://ipfs.io/ipfs/QmbXhS3YUh646BixjYc76F5Y9Fahvuxm1jzPGoYaKNCs9v?filename=0-pug.json",
    "shiba-inu": "https://ipfs.io/ipfs/QmNkcCfsKLUr9qHGW5wdr2KkKcH47sqZ1L3BWQYQymeqgF?filename=1-shiba-inu.json",
    "st-bernard": "https://ipfs.io/ipfs/QmUFgzNC4ydDQuj4KoX5LzfHYmBK9DaAVzreTeMcdFvVyK?filename=1-st-bernard.json",
}


def main():
    collectible = AdvancedCollectible[-1]
    no_of_collectibles = collectible.tokenCounter()
    for tokenId in range(no_of_collectibles):
        breed = collectible.TokenIdToBreed(tokenId)
        breed_file = breed.replace(" ", "")
        metadata_uri = breedToImageUri[breed_file]
        if not collectible.tokenURI(tokenId).startswith("https://"):
            set_tokenUri(tokenId, collectible, metadata_uri)
            read_data(tokenId)
        else:
            print(
                f"the token URI of {tokenId}-{breed_file} is {collectible.tokenURI(tokenId)}"
            )
        print(
            f"Now You can view your nft on {OPENSEA_URL.format(collectible.address, tokenId)}"
        )


def set_tokenUri(tokenId, tokenContract, tokenUri):
    account = get_account()
    tokenContract.setTokenUri(tokenId, tokenUri, {"from": account})


def read_data(tokenId):
    collectible = AdvancedCollectible[-1]
    print(
        f"The token uri of {tokenId}-{collectible.TokenIdToBreed(tokenId)} is {collectible.tokenURI(tokenId)}"
    )
