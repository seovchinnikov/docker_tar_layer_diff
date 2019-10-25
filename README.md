Tool to create diff of docker images' versions (layer by layer) as a tarball and inflate the original image later.

**Note**. Works only for changes in top layers.

**Requirements**: python 2.6+/3.5+


# 4-step process

#### 0. docker inspect <old image> -> make json with old layers' hashes as a json file:
 ` {"Layers": [
                "sha256:41c002c8a6fd36397892dc6dc36813aaa1be3298be4de93e4fe1f40b9c358d99",
                "sha256:647265b9d8bc572a858ab25a300c07c0567c9124390fd91935430bf947ee5c2a",
                ...
            ]
}
`
#### 1. Prepare diff based on new image and hashes of old (existing) layers
`python docker_prepare_update.py --updatesrc <actual (new) tar image to update to> --layers <json with layers' hashes of old image (dict with Layers key and list value)> --output <target tar location (with tar extension) to produce diff>`

#### 2. Transfer diff to target machine

#### 3. Inflate target image's tar based on diff and old image

`python docker_update_image.py --difftar <diff tar previously produced> --oldimg <old img tar> --output <new tar to load to docker>`
