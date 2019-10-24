import hashlib


def get_digest_sha256(file):
    h = hashlib.sha256()

    while True:
        # Reading is buffered, so we can read smaller chunks.
        chunk = file.read(h.block_size)
        if not chunk:
            break
        h.update(chunk)

    return h.hexdigest()
