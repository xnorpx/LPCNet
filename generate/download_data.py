from pathlib import Path
from typing import AnyStr
from urllib.parse import urlparse
import logging
import os
import shutil
import sys
import urllib.request
import zipfile


def download(url: AnyStr, download_path: AnyStr) -> None:
    file_name = os.path.join(download_path, os.path.basename(urlparse(url).path))

    if not os.path.exists(file_name):
        logging.info("Start download url: {} to {}".format(url, file_name))
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        logging.info("Completed the download of url: {} to {}".format(url, file_name))
    else:
        logging.info("{} already downloaded".format(file_name))

    if ".zip" in file_name:
        extract_path = os.path.join(download_path, Path(file_name).stem)
        if not os.path.exists(extract_path):
            logging.info("Start extracting {}".format(file_name))
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(download_path)
            logging.info("Completed extracting {}".format(file_name))
        else:
            logging.info("{} already extracted".format(file_name))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Concatenate wavfiles, assume same format')
    parser.add_argument('--url', type=str,
                        default='http://www-mmsp.ece.mcgill.ca/Documents/Data/TSP-Speech-Database/16k-LP7.zip',
                        help='url to download data')
    parser.add_argument('--download_path', nargs='?', default=os.getcwd(), help='target directory to download to')
    parser.add_argument('--log-level', dest='log_level', default='info', help='logging level',
                        choices=['debug', 'info', 'warning', 'error', 'critical'], required=False)

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(pathname)s,%(lineno)d] %(message)s',
                        level=getattr(logging, args.log_level.upper()),
                        stream=sys.stdout)

    logging.info("Start downloading data")
    download(args.url, args.download_path)
    logging.info("Stop downloading data")


if __name__ == '__main__':
    main()
