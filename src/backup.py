"""
File Backup

Backup the selected file system to the backup storage and to cloud
storage.

File:       backup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file LICENSE
 """

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from do_backup import Backup

if __name__ == "__main__":
    # get the command line arguments
    args = sys.argv
    args.pop(0)  # discard the program name
    Backup(args)

