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

If Syncthing is not running, the script will still launch the game, and sync game saves to/from ~/.local/share/gamesync/saves

### Why not just use Syncthing by itself? Or heck, NextCloud?
There are minor annoyances with Syncthing that I did not appreciate. The syntax for including/excluding directories/files
is confusing, messy, and I can't just make syncthing synchronize all save files within ~/.steam/steam/compatdata folder
without extensive trial and error. There was also the issue where if I deleted a game, this would delete the save game
on all my machines, defeating the purpose.

Nextcloud might make more sense to use in this case, but the other feature I wanted is the ability to sync games upon launch,
much like steam cloud, without the need for third party GUI or the need for a decky plugin.

This is about the most lightweight application I can create without the need for fancy CLI tools.

This may very well be NextCloud with extra steps, but ah well, it's a learning experience!

## Current Limitations
- Obviously you cannot be running the same application on multiple machines with the same user
- Only supports Syncthing (it's what I like using)
  - I may support NextCloud if I ever get around to it, it's unlikely I will support anything else,
  feel free to open a PR if you would like another provider
  - The script needs to be further generalized/modularized to support additional providers easily, this was done in an
  afternoon, and I got it to do what I want it to
- The way its designed means that you will have two copies of a save game on your computer

## Instructions
- Download/Clone this repo
- Run `./install.sh`
- Configure `~/.local/share/gamesync/gamesync.env`
  - This is an environment variables file that will be loaded every time gamesync is launched
  - At the minimum you need to set 3 variables:
  ```
  SYNCTHING_API=<SYNCTHING_API_KEY>
  SYNCTHING_URL=<URL_TO_YOUR_SYNCTHING_INSTANCE>
  SYNCTHING_FOLDER_ID=<SYNCTHING_FOLDER_ID>
  ```
  - `SYNCTHING_URL` is most likely `http://localhost:8384` (the default) unless you configured it on another endpoint
    - This may be different on each machine you setup, depends how you have it configured
  - `SYNCTHING_API` is an API key that is generated from within Syncthing web UI
    - `Actions > Settings > General > API Key`, either copy and paste the one that is already there, or generate a new key
    - This will be different on each machine you set up
  - `SYNCTHING_FOLDER_ID` is the folder you create within Syncthing web UI, create folder and point it to 
  ~/.local/share/gamesync/saves, and note the `Folder ID` that Syncthing generates.
    - This will be the same on all machines you share this folder with.
  - There are two additional environment variables you can set in `gamesync.env`:
    - `GAMESYNC_DEBUG` if set to `true` will make `gamesync` log debug data to ~/.local/share/gamesync/logs
    - `GAMESYNC_LOG_LEVEL` can be set to `NOTSET`, `DEBUG`, `INFO`, `WARN`, `ERROR`, or `FATAL`. If not specified it
    defaults to `INFO`. Ignored if `GAMESYNC_DEBUG` is not defined.
- Configure your games in `~/.local/share/gamesync/gamesync-settings.json`
  - example:

  ```json
  {
    "games": [
      {
        "steamAppId": 0,
        "executableName": "emulationstation",
        "saveLocations": [
          {
            "name": "retroarch",
            "sourceDirectory": "~/.config/retroarch/saves"
          }
        ]
      },
      {
        "steamAppId": 2310,
        "saveLocations": [
          {
            "name": "quake",
            "sourceDirectory": "~/.steam/steam/steamapps/compatdata/2310/pfx/drive_c/users/steamuser/Saved Games/Nightdive Studios/Quake",
            "include": [
              "*.sav"
            ]
          }
        ]
      },
      {
        "steamAppId": 524220,
        "saveLocations": [
          {
            "name": "nier",
            "sourceDirectory": "~/.steam/steam/steamapps/compatdata/524220/pfx/drive_c/users/steamuser/Documents/My Games/NieR_Automata",
            "include": [
              "SlotData_*.dat"
            ]
          }
        ]
      }
    ]
  }
  ```
  - `games` array holds the list of all game definitions
    - Each game has `steamAppId` and/or `executableName`
    - `steamAppId` is what Steam uses to identify what game is running. It will be non-zero for steam games, 0 for
    non-steam games. For non-steam games it is necessary to specify `steamAppId` to be 0.
    - use `executableName` for non-steam games. It could be used for steam games, but executable names tend to be long
    as steam will always feed the fully qualified name into %command%.
    - `saveLocations` is an array can be used to detail what directories you would like to synchronize across different
    computers
      - `name`: alias that identifies the `saveLocation`. Must be the same across machines
      - `sourceDirectory`: location of the save directory, this may vary from machine to machine
      - `include`: an array of strings that can be used to pattern match files that should be included
        - file names and paths are always relative to `sourceDirectory`
        - syntax is the same as python's [fnmatch](https://docs.python.org/3/library/fnmatch.html)
      - `exclude`: an array of strings that can be used to pattern match files that should be excluded
        - file names and paths are always relative to `sourceDirectory`
        - syntax is the same as python's [fnmatch](https://docs.python.org/3/library/fnmatch.html)

## Planned Features
- Package this project for distribution across different distros
- Windows support
- Modularize script to support other providers
- Additional automation for setting up syncthing
