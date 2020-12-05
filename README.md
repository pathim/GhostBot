# GhostBot
Mumble bot to mirror one channel into another

## Use-Case
Main use-case is Among Us.
One way to communicate during the game ist to have two channels:
 - One for the discussion of the living
 - One for the dead for casual chat

The problem with that concept is that the ghosts also want to listen to the discussion.
This bot solves this by forwarding the discussion into the ghost channel.

## Installation
```bash
#Create a python virtual environment
python3 -m venv venv
#Install required packages
venv/bin/pip install -r requirements.txt -c constraints.txt
#Start the bot
venv/bin/python ghostbot.py --host=localhost --user=GhostBot --password=swordfish --src=AmongUs --dst=Ghosts
```
To start the bot through systemd copy ```ghostbot.service``` to ```/usr/local/lib/systemd/system``` and create a file ```/etc/default/ghostbot``` with the content
```bash
HOST=localhost
USER=GhostBot
PASSWORD=swordfish
SRC=AmongUs
DST=Ghosts
```
The given service-file assumes GhostBot to be installed at ```/usr/local/games/ghostbot```.

Then the bot can be started with ```systemctl start ghostbot```.
To start it automatically at boot use ```systemctl enable ghostbot```.


TODO: Mod Among Us to enable automatic channel switching
