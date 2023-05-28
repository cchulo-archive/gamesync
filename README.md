# GameSync

## Introduction
Tired of steam cloud synchronizing graphics settings?

Tired of steam cloud not supporting your favorite games?

Wished non-steam games had cloud save support?

If yes to both questions, then you're in luck! Gamesync is here!

## Description
Gamesync is a script wrapper for launching steam games

It even works outside of steam!

## Requirements
- [Syncthing](https://syncthing.net/)
- Python3

## Instructions
Simply wrap `gamesync` around command you wish to launch with quotes

Example:
- `gamesync "%command%"`
- `gamesync "emulationstation"`
- `gamesync "gamemoderun %command%"`
- `gamesync "gamescope -H 1440 -h 1440 -r 60 -f -- gamemoderun %command%"`

## How does it work?
Most of the heavy lifting is using Syncthing.
The script `gamesync` checks to make sure that the folder where all saves are stored is up-to-date.
When it gets confirmation that synchronization with syncthing is complete, it looks up SteamAppId or the executable
of the application in order to find the save files located under ~/.local/share/gamesync/saves and pulls them into
the games save folder.

The script then waits for the game to exit. When the game exits, gamesync will update gamesync's saves folder with the
updated save files, where Syncthing will automatically pick up the updates and synchronize all other clients automatically.

### Why not just use Syncthing?
There are minor annoyances with Syncthing that I did not appreciate. The syntax for including/excluding directories/files
is confusing, messy, and I can't just make syncthing synchronize all save files within ~/.steam/steam/compatdata folder
without extensive trial and error. There was also the issue where if I deleted a game, this would delete the save game
on all my machines, defeating the purpose.

Nextcloud might make more sense to use in this case, but the other feature I wanted is the ability to sync games upon launch,
much like steam cloud, without the need for third party GUI or the need for a decky plugin.

This is about the most lightweight application I can create without the need for fancy CLI tools.

## Current Limitations
- Obviously you cannot be running the same application on multiple machines with the same user
- Only supports Syncthing (it's what I like using)
  - I may support NextCloud if I ever get around to it, it's unlikely I will support anything else,
  feel free to open a PR if you would like another provider
  - The script needs to be further generalized/modularized to support additional providers easily, this was done in an
  afternoon, and I got it to do what I want it to

## Instructions
- Download/Clone this repo
- Run `./install.sh`
- Configure 