#!/usr/bin/env bash

set -e -o pipefail

echo 'Installing gamesync'
sudo cp gamesync /usr/local/bin/
sudo mkdir /usr/local/share/gamesync
sudo cp share/* /usr/local/share/gamesync/
mkdir -p ~/.local/share/gamesync
echo 'gamesync installed!'
