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
${PERMISSION} mkdir -p ${BASE_LIB}/gamesync
${PERMISSION} cp lib/* ${BASE_LIB}/gamesync/
mkdir -p ~/.local/share/gamesync/logs
mkdir -p ~/.local/share/gamesync/saves
cp gamesync-settings.json ~/.local/share/gamesync/
touch ~/.local/share/gamesync/gamesync.env
echo 'gamesync installed!'
