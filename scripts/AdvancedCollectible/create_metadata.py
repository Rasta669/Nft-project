from brownie import AdvancedCollectible, network
from metadata.sample_metadata import sample_metadata_template
from pathlib import Path
import requests
from scripts.upload_to_pinata import upload_to_pinata
import json
import os

breed_to_image_uri = {
    "pug": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "shiba-inu": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "st-bernard": "",
}

breed_to_metadata_uri = {
    "pug": "https://ipfs.io/ipfs/QmbXhS3YUh646BixjYc76F5Y9Fahvuxm1jzPGoYaKNCs9v?filename=1-pug",
    "shiba-inu": "https://ipfs.io/ipfs/Qme7fE9obmiAKkrx84LCpcdyfyySoDdT2uJCFTwUufhjkp?filename=0-shiba-inu",
    "st-bernard": "",
}


def main():
    creata_metadata()


def creata_metadata():
    collectible = AdvancedCollectible[-1]
    no_of_collectibles = collectible.tokenCounter()
    for tokenId in range(no_of_collectibles):
        breed = collectible.TokenIdToBreed(tokenId)
        breed_file = breed.replace(" ", "")
        metadata_file_name = f"./metadata/{network.show_active()}/{tokenId}-{breed_file}.json"  ##'./metadata/goerli/0-pug'
        if Path(metadata_file_name).exists() == True:
            print(
                f"{metadata_file_name} file exists, delete the current one to override it!!"
            )
        else:
            print(f"Creating {metadata_file_name} file...")
            breed_metadata = sample_metadata_template
            breed_metadata["name"] = breed_file
            breed_metadata["description"] = f"A cute little {breed_file} pup!"
            image_file_path = "./img/" + f"{breed_file}" + ".png"  ##'./img/pug.png'
            print(image_file_path)
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                image_uri = upload_to_ipfs(image_file_path)
                ##upload_to_pinata(image_file_path)
            else:
                if image_uri:
                    image_uri = image_uri
                else:
                    image_uri = breed_to_image_uri[breed_file]
            print(image_uri)
            breed_metadata["image"] = image_uri
            print(breed_metadata)
            with open(metadata_file_name, "w") as file:
                json.dump(breed_metadata, file)
                ##file.close()
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
            else:
                metadata_uri = breed_to_metadata_uri[breed_file]
                print(f"the metadata uri of the {breed_file} is {metadata_uri}")


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_file = fp.read()
        end_point = "/api/v0/add"
        ipfs_node = "http://127.0.0.1:5001"
        response = requests.post(ipfs_node + end_point, files={"file": image_file})
        ipfs_hash = response.json()["Hash"]
        image_file_name = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={image_file_name}"
        print(image_uri)
        return image_uri
