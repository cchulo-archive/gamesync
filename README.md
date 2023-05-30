# GameSync

## Description

Got tired of steam cloud synchronizing graphics settings, was getting annoying to switch from 
my steam deck to my desktop. Worst yet, some of my favorite games are not supported. To top it off, non-steam games
already lack cloud saves if they don't have their own third party launcher.

It's 2023, so here's my solution.

Gamesync is a script wrapper for launching steam games and ensuring that the save files that are loaded are the latest
it was able to grab from the cloud.

It even works outside of steam!

It's not perfect, there's the chance that if you're offline syncthing might not be able to grab the latest saves, and
you could inadvertently overwrite save game on your other PC. Make sure to setup syncthing to backup all files with at
least simple file versioning (see syncthing docs for how to do that).

## Requirements
- [Syncthing](https://syncthing.net/) is running on your machine
  - If you need help with this, read their docs
- Python3
- Only linux is supported for now
  - This may work on MacOS, all you really need is bash and python3
  - It was originally going to all be written in python 3, but could not get LD libraries to load properly
- Only use this with single player games. *I am not responsible if this tool gets you banned!*

## Instructions
Simply wrap `gamesync` around command you wish to launch with quotes

Example:
- `gamesync "%command%"`
- `gamesync "emulationstation"`
- `gamesync "gamemoderun %command%"`
- `gamesync "gamescope -H 1440 -h 1440 -r 60 -f -- gamemoderun %command%"`

### Note for the Steam Deck
Even though ~/.local/bin is in the PATH, in gamemode it is unable to find `gamesync`, so please add launch options for
the steam deck as: `~/.local/bin/gamesync "%command%"`

## How does it work?
Most of the heavy lifting is done by Syncthing for network synchronization, all it does is it synchronizes
`~/.local/share/gamesync/saves` across all machines. That's it, no need for any special configuration.
Upon launching `gamesync`, the script checks:
- to make sure Syncthing is done synchronizing `~/.local/share/gamesync/saves`
- When it gets confirmation that synchronization with syncthing is complete, it looks up SteamAppId or the executable
of the application in order to find the save files located under `~/.local/share/gamesync/saves` and pulls them into
the games' save folder.
- The script then waits for the game to exit.
- When the game exits, gamesync will push the updated saves back up to `~/.local/share/gamesync/saves`
- Syncthing will once again take care of the cross-machine synchronization

If Syncthing is not running, the script will still launch the game, and sync game saves to/from 
`~/.local/share/gamesync/saves`

### Why not just use Syncthing by itself? Or heck, NextCloud?
There are minor annoyances with Syncthing that I did not appreciate. The syntax for including/excluding 
directories/files is confusing, messy, and I can't just make syncthing synchronize all save files within 
`~/.steam/steam/compatdata` folder without extensive trial and error. It is unfortunate that not all steam games
share a single Wine prefix, but this is the state of how things are right now on steam linux gaming.

There was also the issue where if I deleted a game, the uninstaller would delete the save, which would make syncthing 
delete the save everywhere.

Nextcloud might make more sense to use in this case, but the other feature I wanted is the ability to sync games upon 
launch, much like steam cloud, without the need for third party GUI or the need for a decky plugin.

This is about the most lightweight application I can create without the need for fancy GUI or anything unnecessary polling
in the background

This may very well be NextCloud with extra steps, but meh, it works for me.

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
- Execute `./install.sh` with the following options
  - If you are using Steam on desktop, just execute `./install.sh`
  - On steam deck, please use `./install.sh local`, this will install gamesync scripts into
  `~/.local/bin` and `~/.local/share`, I was not sure if /usr/local/ was safe on SteamOS 3 (since the OS is immutable) 
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
  - Note that some games are already configured out of the box via `.default-settings.json`, a list will be provided
  below. The only caveat is that gamesync assumes your saves are all under ~/.local/steam/steam/.
  This is currently not configurable. You will need to override these game defintions in `gamesync-settings.json`
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

## Updating
`git pull` or re-download the latest version of main branch and re-execute `./install.sh` or `./install.sh local`

If you would like to only upgrade `.default-settings.json` simply execute `gamesync-update-settings` from the CLI

## List of supported steam games

- [Alan Wake](https://store.steampowered.com/app/108710/Alan_Wake/)
- [Alice Madness Returns](https://store.steampowered.com/app/19680/Alice_Madness_Returns/)
- [Fallout 3 GOTY Edition](https://store.steampowered.com/app/22370/Fallout_3_Game_of_the_Year_Edition/)
- [Fallout New Vegas](https://store.steampowered.com/app/22380/Fallout_New_Vegas/)
- [Quake](https://store.steampowered.com/app/2310/Quake/)
  - Only the 2021 Nightdive studios, the OG release supports steam cloud
- [Nier Automata](https://store.steampowered.com/app/524220/NieRAutomata/)
- [Hi-Fi Rush](https://store.steampowered.com/app/1817230/HiFi_RUSH/)

Will add more games, depending on which ones I am playing, but feel free to open a PR fi you want out-of-the-box 
support for your favorite titles

## Planned Features
- Package this project for distribution across different distros
- Windows support
  - Confirm MacOS support
- Modularize script to support other providers
- Additional automation for setting up syncthing
