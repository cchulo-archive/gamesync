# GameSync

## Description

Steam cloud unfortunately synchronizes graphics settings for some games, making it awkward to switch from 
my steam deck to my desktop, and having to reset the settings. every. single. time.

Worst yet, some of my favorite games are not supported.

To top it off, non-steam games already lack cloud saves for the most part unless the dev supports it through some
third party launcher or service.

So here's my solution.

Gamesync is a script wrapper for launching steam games and ensuring that the saves that get loaded are the latest.

It even works outside of steam!

Note: It's not perfect. It works for me but may not work for you. See the limitations below.

## Requirements
- [Syncthing](https://syncthing.net/) is running on your machine
  - If you need help with this, read their docs
- Python3
- Only linux is supported for now
  - This may work on MacOS, all you really need is bash and python3
  - It was originally going to all be written in python 3, but could not get LD libraries to load properly
- Only use this with single player games. *I am not responsible if this tool gets you banned!*

## Instructions
```
Usage:
    gamesync [options] -- <command>

  Options:
    -h | --help  )    Displays this dialog
    -a | --alias )    Used to identify a non-steam game. Useful in case the executable name is not useful
                      or the command is in a format that is not easily parsable by gamesync
```

Example:
```bash
gamesync --help

# for steam games
gamesync -- %command%
gamesync -- gamemoderun %command%

# for non-steam games
gamesync --alias emu -- emulationstation
gamesync --alias my-alias -- gamescope -H 1440 -h 1440 -r 60 -f -- gamemoderun %command%
```


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
There are minor annoyances with Syncthing:

The syntax for including/excluding directories/files is confusing, messy, and error-prone. As a result I couldn't
just make syncthing synchronize all save files within `~/.steam/steam/compatdata` folder without extensive trial and 
error. It is unfortunate that not all steam games share a single Wine prefix, but this is the state of how things are 
right now on steam linux gaming.

There was also the issue where if I deleted a game, the uninstaller would delete the save, which would make syncthing 
delete the save everywhere.

Nextcloud might make more sense to use in this case, but the other feature I wanted is the ability to sync games upon 
launch, much like steam cloud, without the need for third party GUI or the need for a decky plugin.

This may very well be NextCloud with extra steps, but meh, it works for me.

## Current Limitations
- Obviously you cannot be running the same application on multiple machines with the same user, steam helps with this
by disallowing two computers to run the same game on two computers while online, but can be an issue if offline and
for non-steam games.
- Only supports Syncthing (it's what I like using)
  - I may support NextCloud if I ever get around to it, it's unlikely I will support anything else,
  feel free to open a PR if you would like another provider
    - The script needs to be further generalized/modularized to support additional providers easily.
    This script was done in an afternoon after all.
- The way gamesync is designed means that you will have two copies of a save game on your computer, though I see this as
a pro rather than a con personally.
- If you're offline syncthing might not be able to grab the latest saves, and therefore gamesync will be grabbing out
of date saves. Saving/exiting again, while syncthing is still offline, will cause syncthing to overwrite saves across
all machines. It's just the way syncthing works. To help with this you should enable simple file versioning.
See the Syncthing docs for how to enable this in the web UI.
- (currently) only supports saves for a single player
- (currently) only supports saves that are hosted on the home folder (~/.steam/steam/...)

## How to install
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
    - This may be different on each machine you set up, depends on how you have it configured
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
  This is currently not configurable. You will need to override these game definitions in `gamesync-settings.json`
  - example:

  ```json
  {
    "games": [
      {
        "steamAppId": 0,
        "directoryName": "emu-dir",
        "alias": "emu",
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
        "directoryName": "nier",
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
    - Each game has `steamAppId` and/or `alias`
    - `steamAppId` is what Steam uses to identify what game is running. It will be non-zero for steam games, 0 for
    non-steam games. For non-steam games it is necessary to specify `steamAppId` to be 0.
    - use `alias` for non-steam games
    - use `directoryName` if you wish to store saves in a directory that is not named after the steamAppId or the executable name
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

## List of out-of-the box supported steam games

- [Alan Wake](https://store.steampowered.com/app/108710/Alan_Wake/)
  - not recommended to use gamesync with this title, as Alan Wake on steam has tight integration with steam cloud,
  using gamesync can lead to corrupted saves. The reason this was implemented is that graphics settings are
  synchronized across machines.
- [Alice Madness Returns](https://store.steampowered.com/app/19680/Alice_Madness_Returns/)
- [Fallout 3 GOTY Edition](https://store.steampowered.com/app/22370/Fallout_3_Game_of_the_Year_Edition/)
- [Fallout New Vegas](https://store.steampowered.com/app/22380/Fallout_New_Vegas/)
- [Quake](https://store.steampowered.com/app/2310/Quake/)
  - Only the 2021 Nightdive studios, ~~the OG release supports steam cloud~~ this has been fixed in the latest
  update to Quake, so gamesync is optional now for this title
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
- support multiple steam users on a single account
- support saves stored on separate `SteamLibrary` directories not located under ~/.steam/steam
