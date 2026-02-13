"""
Provide common support functionality for the test files.

File:       build_file_system.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.1
"""

import os
import sys
import time
from pathlib import Path

from lbk_library.gui import Settings

directories = [
    ".config",
    "test1",
    "test2",
    ".cache",
    "trash",
    "$RECYCLE.BIN",
    "Downloads",
    "System Volume Information",
    "test_links",
]
""" The set of temporary directories, common to Windows and Linux. """

# Additional directories for Linux, Windows is case insensitive by
# default so these are flagged as dupicates.
if sys.platform.startswith("linux"):
    directories.append("Cache")
    directories.append("Trash")

links = ["link_good", "link_bad"]
""" The set of test links, one valid link, one broken link. """

ten_days_previous = time.time() - (10 * 86400)
""" set a timestamp for 10 days before now. """

additional_files = [
    "backup_file_1~",
    "backup_file2.bak",
    "py_file.py",
    "py_file.pyc",
]
"""The set of additional files to be added to one of the directories."""


def load_directory_set(dirs, base_dir, add_files=True):
    """
    Add a set of sub-directories and files to the temperary base
    directory. The file modification dates will be set 10 days previous
    to now.

    Parameters:
       dirs: (list[str] the set of directory names to include in the
            temperary source direcory.
        base_dir: (str) the specific directory path, either 'source' or
            'dest'.
        add_files: (bool) should the directories be loaded with files,
            default is True.
    """
    for a_dir in dirs:
        new_dir = base_dir / a_dir
        new_dir.mkdir()

        if add_files and a_dir != ".config":
            file1 = new_dir / "file1.txt"
            file1.write_text("This is file1 in " + a_dir)
            os.utime(file1, (ten_days_previous, ten_days_previous))
            file2 = new_dir / "file2.txt"
            file2.write_text("This is file2 in " + a_dir)
            os.utime(file2, (ten_days_previous, ten_days_previous))


def load_links(links, ln_src_dir):
    """
    Add a set of links to a directory.

    Parameters:
        links: (list[str] the set of names to include in the
            temperary source direcory.
        ln_src_dir: (str) the specific directory path for the links
    """
    good_link_file = ln_src_dir / "good_link.txt"
    good_link_file.write_text("This is a good link")
    os.symlink(good_link_file, ln_src_dir / "link_good")
    bad_link_file = ln_src_dir / "bad_link.txt"
    bad_link_file.write_text("This is a bad link")
    os.symlink(bad_link_file, ln_src_dir / "link_bad")
    os.remove(bad_link_file)


def add_files(file_list, dir):
    """
    Add a set of files to a directory.

    Parameters:
        file_list: (list[str] the set of file names to include in the
            temperary source direcory.
        dir: (str) the specific directory path for the links
    """
    for filename in file_list:
        add_file = dir / filename
        add_file.write_text("This is " + filename)
        os.utime(add_file, (ten_days_previous, ten_days_previous))


def build_config_file(source: str, dest: str, name: str = "BackupTest") -> Settings:
    """
    Create a custom configuration file for testing purposes.

    Parameters:
        source (str): The source path to be backed up.
        dest (str): The destination for the backup files.
        name (str): The name of the config file to be built. Default is
            'BackupTest';
    """
    config_file = Settings("UnnamedBranch", "BackupTest")
    config_file.setValue("last_backup", 0)
    config_file.setValue("start_dir", str(source))
    config_file.setValue("backup_location", str(dest / "backup_dir"))
    config_file.setValue("log_path", str(dest / "log_dir"))
    config_file.setValue("log_name", str("test_log.log"))
    config_file.set_bool_value("exclude_cache_dir", False)
    config_file.set_bool_value("exclude_trash_dir", False)
    config_file.set_bool_value("exclude_download_dir", False)
    config_file.set_bool_value("exclude_cache_files", False)
    config_file.set_bool_value("exclude_backup_files", False)
    config_file.write_list("exclude_specific_dirs", [])
    config_file.write_list("exclude_specific_files", [])
    config_file.write_list("include_specific_dirs", [])
    config_file.write_list("include_specific_files", [])
    config_file.sync()

    return config_file


def new_filesys(source: Path, dest: Path):
    """
    Set up a temporary filesystem to be discarded after each test is run.

    'source' is the path for a set of files to be backed up. 'dest' is
    the path to the backup location. Source will be loaded with a set of
    directories which will include some which may be ignored and some
    that will always be used. Each directory will be loaded with several
    small sample files. Additionally, a good link and a broken link will
    be included.

    Parameters:
        source (Path)  A path to a temperary location for the source
            directory structure.
        dest (Path)  A path to a temperary location for the dest
            directory structure.
    """
    source.mkdir()
    dest.mkdir()
    # make a set of source directories and files
    load_directory_set(directories, source)
    # only do symlinks for Linux, not Windows
    if sys.platform.startswith("linux"):
        link_source = source / "test_links"
        load_links(links, link_source)
