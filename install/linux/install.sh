#! /bin/bash

# ############################
# Install the backup program in the user's bin dirctory, then enable automatic
# backup using systemd
#
# File:       install.sh
# Author:     Lorn B Kerr
# Copyright:  (c) 2022 Lorn B Kerr
# License:    see file LICENSE
#
# ############################

# copy the backup file to the 'bin' directory
cp ~/development/backup/dist/backup ~/bin/backup

# copy systemd files to systemd config directory
# build directories if they don't exist
if [[ ! -d "$HOME/.config/systemd" ]]; then
    mkdir ~/.config/systemd
fi

if [[ ! -d "$HOME/.config/systemd/user" ]]; then
    mkdir ~/.config/systemd/user
fi

# copy the systemd files
cp ~/development/backup/install/linux/lbk_backup.service ~/.config/systemd/user/lbk_backup.service
cp ~/development/backup/install/linux/lbk_backup.timer ~/.config/systemd/user/lbk_backup.timer

# set systemd service and timer for automatic running
systemctl --user enable lbk_backup.timer
systemctl --user daemon-reload
systemctl --user start lbk_backup.timer
