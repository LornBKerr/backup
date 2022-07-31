#! /bin/bash

# ############################
# install the backup program in the bin dirctory, then enable automatic 
# backuo using systemd
# ############################

# copy the backup file to the 'bin' directory
cp ~/development/backup/dist/backup ~/bin/backup

# copy systemd files to systemd config directory
# build directories if they dont exist
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
