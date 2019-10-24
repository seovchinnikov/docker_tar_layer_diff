Tool to create diff of docker images' versions (layer by layer) as a tarball and inflate the original image later.

**Note**. Works only for changes in top layers.

# 3-step process

#### 1. Prepare diff based on new image and hashes of old (existing) layers
`python docker_prepare_update.py --updatesrc <actual tar image to update to> --layers <json with layers' hashes of old image (dict with Layers key and list value)> --output <target tar location (with tar extension) to produce diff>`

#### 2. Transfer diff to target machine

#### 3. Inflate target image's tar based on diff and old image

`python docker_update_image.py --difftar <diff tar previously produced> --oldimg <old img tar> --output <new tar to load to docker>`
