"""
Provide common support functionality for several test files.
"""
import os
import pathlib
import sys
import time

import pytest
from lbk_library import IniFileParser

#
# if "/home/larry/development/backup/src" not in sys.path:
#    sys.path.append("/home/larry/development/backup/src")

# Directories for Windows and Linux
directories = [
    ".config",
    "test1",
    "test2",
    "cache",
    "trash",
    "$RECYCLE.BIN",
    "Downloads",
    "System Volume Information",
    "test_links",
]
""" The set of temporary directories. """

# additional directories for Linux, Windows is case insensitive by
# default so these are flagged as dupicates.
if sys.platform.startswith("linux"):
    directories.append("Cache")
    directories.append("Trash")


links = ["link_good", "link_bad"]
""" The set of test links, one valid link, one broken link. """

ten_days_previous = time.time() - (10 * 86400)
""" set a timestamp for 10 days before now. """

additional_files = [
    "file_is_cache_file",
    "backup_file_1~",
    "backup_file2.bak",
    "py_file.py",
    "py_file.pyc",
]
"""
The set of additional files to be added to one of the directories to
test the file exclusion config settings.
"""


def get_test_config(source: pathlib.Path = "", dest: pathlib.Path = ""):
    """
    A basic, do nothing  config file with the base_dir set to source, the
    basckup_dir set to dest and the config file set to 'source/.config'. All
    other selections are set to the False or empty settings.

    Parameters:
        source: (pathlib.Path) the file path to be backed up, default is
            blank string.
        dest: (pathlib.Path) the destination for the backup, default is
            blank string.

    Returns:
        (dict[str, Any]) a do nothing config file.
    """
    return {
        "general": {
            "last_backup": 0,
            "base_dir": source,
            "backup_dir": dest,
            #            "config_file": os.path.join(source, ".config"),
            "external_storage": False,
            "cloud_storage": False,
        },
        "dir_exclude": {
            "cache_dir": False,
            "trash_dir": False,
            "download_dir": False,
            "sysVolInfo_dir": False,
            "specific_dirs": [],
        },
        "dir_include": {
            "specific_dirs": [],
        },
        "file_exclude": {
            "backup_files": False,
            "cache_files": False,
            "specific_files": [],
        },
        "file_include": {
            "specific_files": [],
        },
    }
    # end get_test_config()


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
    # end load_directory_set()


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
    # end load_links()


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
    # end add_files()


@pytest.fixture
def filesystem(tmp_path):
    """
    Setup a temporary filesystem in a temperary location which will be
    discarded after the test sequence is run.

    'source' is the path for a set of files to be backed up. 'dest' is
    the path to the backup location. Source will be loaded with a set of
    directories which will include some which may be ignored and some
    that will always be used. Each directory will be loaded with several
    small sample files. Additionally, a good link and a broken link will
    be included.

    Parameters:
        tmp_path: pytest fixture to setup a path to a temperary location

    Returns:
        tuple(source, dest) The temparary file paths to use.
    """
    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()

    # make a set of source directories and files
    load_directory_set(directories, source)
    # only do symlinks for Linux, not Windows
    if sys.platform.startswith("linux"):
        link_source_dir = source / "test_links"
        load_links(links, link_source_dir)

    # set the config file
    config_handler = IniFileParser("backup.ini", "LBKBackup", source / ".config")
    config_handler.write_config(get_test_config(source, dest))

    return source, dest
    # end filesystem()


# end build_file_system.py
