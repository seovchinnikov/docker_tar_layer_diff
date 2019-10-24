from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import

import tarfile
import argparse
import json
import shutil

from utils.logging_utils import get_logger
from utils.sha_utils import get_digest_sha256

logger = get_logger(__name__)


def arg_parse():
    parser = argparse.ArgumentParser(description='Make resulting update docker image')
    parser.add_argument('--difftar', help='diff tar previously produced', type=str,
                        required=True)
    parser.add_argument('--oldimg', help='old img tar', type=str,
                        required=True)
    parser.add_argument('--output', help='new tar to load to docker', type=str,
                        required=True)
    return parser.parse_args()


def prepate_target_tar(diff_tar, old_img, output_tar):
    with tarfile.open(old_img) as tar:
        all_files = tar.getmembers()

        with open(diff_tar + '.json', "r") as f:
            layers_json_to_remain = set(json.load(f))

        files_to_add_to_update = []
        used_shas = set()
        filenames_to_add_to_update = set()
        logger.info('start to analyze old tar')

        for file_tar in all_files:
            if file_tar.isdir() and '/' not in file_tar.name:
                f = tar.extractfile(file_tar.name + "/layer.tar")
                sha256 = str(get_digest_sha256(f))
                logger.info(sha256)
                if sha256 in layers_json_to_remain:
                    filenames_to_add_to_update.add(file_tar.name)
                    used_shas.add(sha256)

            subfiles = file_tar.name.split('/')
            root_dir = subfiles[0]
            if root_dir in filenames_to_add_to_update:
                files_to_add_to_update.append(file_tar)

        if not layers_json_to_remain == used_shas:
            raise Exception('it seems like layers info do not match with actual tar image')

        logger.info('start to inflate tar')
        shutil.copy(diff_tar, output_tar)
        with tarfile.open(name=output_tar, mode='a') as tar_new:
            for tarinfo in files_to_add_to_update:
                f = tar.extractfile(tarinfo.name)
                tar_new.addfile(tarinfo, f)

        logger.info('image is ready at %s ' % output_tar)


if __name__ == "__main__":
    args = arg_parse()
    prepate_target_tar(args.difftar, args.oldimg, args.output)
