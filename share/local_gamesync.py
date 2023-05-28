#!/usr/bin/env python3

import os
import logging
import argparse
import json
import sys
import fnmatch
import shutil
from datetime import date

'''
This script is used to stage directories specified in ~/.local/share/gamesync/gamesync-settings.json to
~/.local/share/gamesync/saves in order for syncthing to properly synchronize them

IMPORTANT NOTE: This script does not check if syncthing is currently synchronizing! 

This script is not meant to be used directly, instead the bash script gamesync will invoke this python script
when appropriate.
'''


debug = os.getenv('GAMESYNC_DEBUG', None)
log_file = None
if debug == 'true':
    current_date = date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")
    log_file = os.path.expanduser(f'~/.local/share/gamesync/logs/log.{formatted_date}.log')

gamesync_log_level = os.getenv('GAMESYNC_LOG_LEVEL', None)

if gamesync_log_level == "NOTSET":
    log_level = logging.NOTSET
elif gamesync_log_level == "DEBUG":
    log_level = logging.DEBUG
elif gamesync_log_level == "INFO":
    log_level = logging.INFO
elif gamesync_log_level == "WARN":
    log_level = logging.WARN
elif gamesync_log_level == "ERROR":
    log_level = logging.ERROR
elif gamesync_log_level == "FATAL":
    log_level = logging.FATAL
else:
    log_level = logging.INFO

log_format = '%(asctime)s | %(levelname)s | local_gamesync.py | %(message)s'

logging.basicConfig(
    format=log_format,
    level=log_level,
    datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger('')
logger.addHandler(file_handler)


def synchronize_directories(source_dir, dest_dir, include_patterns=None, exclude_patterns=None):
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            source_path = os.path.join(root, filename)
            relative_path = os.path.relpath(source_path, source_dir)
            dest_path = os.path.join(dest_dir, relative_path)

            if include_patterns:
                logger.debug(f'Testing if {relative_path} is in include_patterns: {include_patterns}')
                matched_include = any(fnmatch.fnmatch(relative_path, pattern) for pattern in include_patterns)
                if not matched_include:
                    continue

            if exclude_patterns:
                logger.debug(f'Testing if {relative_path} is in exclude_patterns: {include_patterns}')
                matched_exclude = any(fnmatch.fnmatch(relative_path, pattern) for pattern in exclude_patterns)
                if matched_exclude:
                    continue

            if not os.path.exists(dest_path) or os.path.getmtime(source_path) > os.path.getmtime(dest_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Create missing directories
                shutil.copy2(source_path, dest_path)
                logger.info(f"Copied {source_path} to {dest_path}")
            else:
                logger.debug(f'file {dest_path} already up to date')


def synchronize_saves(game, gamesync_folder_name, download):
    gamesync_directory = os.path.expanduser(f'~/.local/share/gamesync/saves/{gamesync_folder_name}')
    save_locations = game['saveLocations']
    for saveLocation in save_locations:
        save_location_name = saveLocation['name']
        source_directory = os.path.expanduser(saveLocation['sourceDirectory'])
        include = None if 'include' not in saveLocation else saveLocation['include']
        exclude = None if 'exclude' not in saveLocation else saveLocation['exclude']

        logger.debug(f'Save location name {save_location_name}')
        logger.debug(f'Source directory {source_directory}')
        logger.debug(f'Include {include}')
        logger.debug(f'Exclude {exclude}')

        gamesync_save_path = os.path.join(gamesync_directory, save_location_name)
        if not os.path.exists(gamesync_save_path):
            os.makedirs(gamesync_save_path)

        if download:
            source = gamesync_save_path
            destination = source_directory
        else:
            source = source_directory
            destination = gamesync_save_path

        logger.info(f'Synchronizing from {source} to {destination}')
        synchronize_directories(source, destination, include, exclude)


def main():
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

    logger.info(f'SteamAppId: {steam_app_id}')
    logger.info(f'Executable name: {executable_name}')

    if (download is True and upload is True) or (download is False and upload is False):
        logger.error("Must either specify download or upload, but not both")
        sys.exit(1)

    if steam_app_id == "0" and executable_name is None:
        logger.error("Must specify executableName if steamAppId is 0")
        sys.exit(2)

    gamesync_filepath = os.path.expanduser('~/.local/share/gamesync/gamesync-settings.json')
    logger.info(f'Synchronizing saves using entries in {gamesync_filepath}')
    with open(gamesync_filepath, 'r') as file:
        file_contents = file.read()
        game_settings = json.loads(file_contents)
        if steam_app_id != "0":
            game = next((game for game in game_settings['games'] if f"{game['steamAppId']}" == steam_app_id), None)
            name = steam_app_id
        else:
            game = next((game for game in game_settings['games'] if ('executableName' in game) and
                         game['executableName'] == executable_name), None)
            name = executable_name
        if game is None:
            err_msg = f'Game with steam id {steam_app_id}'
            if steam_app_id == "0":
                err_msg += f' and executable name {executable_name}'
            err_msg += f' was not found in {gamesync_filepath}'
            logger.error(err_msg)
            sys.exit(3)
        synchronize_saves(game, name, download)


if __name__ == "__main__":
    main()
