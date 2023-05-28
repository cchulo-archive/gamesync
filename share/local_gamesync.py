#!/usr/bin/env python3

import os
import logging
import argparse


def setup_logging():
    debug = os.getenv('GAMESYNC_DEBUG')
    log_file = None
    if debug == 'true':
        log_file = '~/.local/share/gamesync/logs/log.log'

    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s | PYTHON | %(message)s',
        level=logging.NOTSET,
        datefmt='%Y-%m-%d %H:%M:%S')


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Synchronize game files for steam or non-steam game")
    parser.add_argument("--steamAppId", required=True, help="The SteamAppId")
    parser.add_argument("--executableName", required=True, help="Used if SteamAppId is 0")
    parser.add_argument("--download", required=False, help="Used to download game saves")
    parser.add_argument("--upload", required=False, help="Used to upload game saves")
    args = parser.parse_args()

    steam_app_id = args.steamAppId
    executable_name = args.executableName
    download = args.download
    upload = args.upload

    logging.info(f'SteamAppId: {steam_app_id}')
    logging.info(f'Executable name: {executable_name}')
    logging.info(f'Downloading save: {download}')
    logging.info(f'Uploading save: {upload}')


if __name__ == "__main__":
    main()
