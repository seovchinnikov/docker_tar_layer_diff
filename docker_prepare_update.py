from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import

import tarfile
import argparse
import json
import os

from utils.logging_utils import get_logger
from utils.sha_utils import get_digest_sha256

logger = get_logger(__name__)


def arg_parse():
    parser = argparse.ArgumentParser(description='Prepare to update docker image (produce diff)')
    parser.add_argument('--updatesrc', help='actual tar image to update to', type=str,
                        required=True)
    parser.add_argument('--layers', help='json with layers\' hashes of old image (dict with Layers key and list value)',
                        type=str,
                        required=True)
    parser.add_argument('--output', help='target tar location (with tar extension) to produce diff', type=str,
                        required=True)
    return parser.parse_args()


def prepare_diff_tar(update_src, layers_json_file, output_diff_tar):
    with tarfile.open(update_src) as tar:
        all_files = tar.getmembers()

        with open(layers_json_file, "r") as f:
            layers_json = json.load(f)
        layers = layers_json['Layers']
        layers = set([layer.replace('sha256:', '') for layer in layers])

        files_to_add_to_update = []
        filenames_to_add_to_update = set()
        old_layers_to_maintain = []
        total_size = 0

        logger.info('start to analyze new tar')
        for file_tar in all_files:
            # print(file_tar)
            if file_tar.isdir() and '/' not in file_tar.name:
                f = tar.extractfile(file_tar.name + "/layer.tar")
                sha256 = str(get_digest_sha256(f))
                logger.info(sha256)
                if sha256 not in layers:
                    filenames_to_add_to_update.add(file_tar.name)
                else:
                    old_layers_to_maintain.append(sha256)

            subfiles = file_tar.name.split('/')
            root_dir = subfiles[0]
            if root_dir in filenames_to_add_to_update or (len(subfiles) == 1 and not file_tar.isdir()):
                files_to_add_to_update.append(file_tar)
                total_size += file_tar.size / 1e6

        if os.path.exists(output_diff_tar):
            os.remove(output_diff_tar)

        with tarfile.open(name=output_diff_tar, mode='w') as tar_new:
            for tarinfo in files_to_add_to_update:
                f = tar.extractfile(tarinfo.name)
                tar_new.addfile(tarinfo, f)

        with open(output_diff_tar + '.json', 'w') as f:
            json.dump(old_layers_to_maintain, f)

        logger.info('total %s mb to transfer' % total_size)
        logger.info('kept old layers number: %s' % len(old_layers_to_maintain))
        logger.info('new layers number: %s' % len(filenames_to_add_to_update))


if __name__ == "__main__":
    args = arg_parse()
    prepare_diff_tar(args.updatesrc, args.layers, args.output)
