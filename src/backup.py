"""
File Backup.

Backup the selected file system to the backup storage and to cloud
storage.

Backup any new and/or changed files in the global home directory to the
backup directory on an external disk drive. A new file is one that has
been added or renamed since the last backup. A changed file is one
where the modification time stamp is greater than the backed up file
time stamp.

Any new directories are created in the backup store and changed files
are copied to the store.

File:       backup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import sys

from main import Backup

if __name__ == "__main__":
    # get the command line arguments
    args = sys.argv
    args.pop(0)  # discard the program name
    Backup(args)
