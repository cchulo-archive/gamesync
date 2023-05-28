#!/usr/bin/env python3

import os
import logging
import argparse
import json
import sys


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


def synchronize_saves(game, download):
    if download:
        logging.info(f'Download for {json.dumps(game, indent=4)}')
    else:
        logging.info(f'Upload for {json.dumps(game, indent=4)}')
    pass


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Synchronize game files for steam or non-steam game")
    parser.add_argument("--steamAppId", required=True, help="The SteamAppId")
    parser.add_argument("--executableName", required=False, help="Used if SteamAppId is 0")
    parser.add_argument("--download", action='store_true', required=False, help="Used to download game saves")
    parser.add_argument("--upload", action='store_true', required=False, help="Used to upload game saves")
    args = parser.parse_args()

    steam_app_id = args.steamAppId
    executable_name = args.executableName
    download = args.download
    upload = args.upload

    logging.info(f'SteamAppId: {steam_app_id}')
    logging.info(f'Executable name: {executable_name}')

    if (download is True and upload is True) or (download is False and upload is False):
        logging.error("Must either specify download or upload, but not both")
        sys.exit(1)

    if steam_app_id is "0" and executable_name is None:
        logging.error("Must specify executableName if steamAppId is 0")
        sys.exit(2)

    gamesync_filepath = os.path.expanduser('~/.local/share/gamesync/gamesync-settings.json')
    with open(gamesync_filepath, 'r') as file:
        file_contents = file.read()
        game_settings = json.loads(file_contents)
        if steam_app_id != "0":
            game = next((game for game in game_settings['games'] if game['steamAppId'] == steam_app_id), None)
        else:
            game = next((game for game in game_settings['games'] if game['executableName'] == executable_name), None)
        if game is None:
            err_msg = f'Game with steam id {steam_app_id}'
            if steam_app_id is "0":
                err_msg += f' and executable name {executable_name}'
            err_msg += f' was not found in {gamesync_filepath}'
            logging.error(err_msg)
            sys.exit(3)
        synchronize_saves(game, download)


if __name__ == "__main__":
    main()
