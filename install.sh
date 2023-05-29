#!/usr/bin/env bash

set -e -o pipefail

if [[ "$1" == "local" ]]; then
  echo "Installing scripts in ${HOME}/.local"
  BASE_BIN="${HOME}/.local/bin"
  BASE_LIB="${HOME}/.local/lib/"
  PERMISSION=""

  # paths under ~/.local are not standard
  mkdir -p "${BASE_BIN}"
  mkdir -p "${BASE_LIB}"
else
  echo "Installing scripts in /usr/local"
  BASE_BIN="/usr/local/bin"
  BASE_LIB="/usr/local/lib"
  PERMISSION="sudo"
fi

echo 'Installing gamesync'
${PERMISSION} cp gamesync ${BASE_BIN}
${PERMISSION} cp gamesync-update-settings ${BASE_BIN}

echo "Creating folders in ${BASE_LIB}"
${PERMISSION} mkdir -p ${BASE_LIB}/gamesync
${PERMISSION} cp lib/* ${BASE_LIB}/gamesync/

echo "Creating folders in ~/.local/share/gamesync"
mkdir -p ~/.local/share/gamesync/logs
mkdir -p ~/.local/share/gamesync/saves

if [[ ! -f ~/.local/share/gamesync/gamesync-settings.json ]]; then
  echo "Creating ~/.local/share/gamesync/gamesync-settings.json"
  echo '[]' > ~/.local/share/gamesync/gamesync-settings.json
fi

cp .default-settings.json ~/.local/share/gamesync/

if [[ ! -f ~/.local/share/gamesync/gamesync.env ]]; then
  echo "Creating ~/.local/share/gamesync/gamesync.env, be sure to populate this file!"
  {
    echo 'SYNCTHING_API='
    echo 'SYNCTHING_URL='
    echo 'SYNCTHING_FOLDER='
  } >> ~/.local/share/gamesync/gamesync.env
fi

echo 'gamesync installed!'
