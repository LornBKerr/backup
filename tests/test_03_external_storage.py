"""
Test the ExternalStorage class functionality.

File:       test_03_external_storage.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

import os
import sys
import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from build_filesystem import (
    add_files,
    additional_files,
    build_config_file,
    directories,
    load_directory_set,
    new_filesys,
)
from external_storage import ExternalStorage
from logger import Logger


def test_03_01_init(tmp_path):
    """
    Testing Backup.ExternalStorage.__init__()

    Test the the object is really a ExternalStorage class
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)
    bes = ExternalStorage(test_config, logger, actions)
    assert isinstance(bes, ExternalStorage)
    logger.close_log()


def test_03_02_dir_exclude_list_empty(tmp_path):
    """
    Testing ExternalStorage.dir_exclude_list() with no exclusions.

    Test the results of ExternalStorage.dir_exclude_list() for
    no exclusions. Should be an empty list.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert len(exclusion_list) == 0
    logger.close_log()


def test_03_03_dir_exclude_list_dir_names(tmp_path):
    """
    Testing ExternalStorage.dir_exclude_list() for excluding specific directories.

    Test the results of ExternalStorage.dir_exclude_list() for
    excluding specific directories.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    # check that 'specific_dirs' is picked up
    test_config.write_list("exclude_specific_dirs", ["a dir"])
    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert exclusion_list == test_config.read_list("exclude_specific_dirs")
    assert "a dir" in exclusion_list
    logger.close_log()


def test_03_04_dir_exclude_list_cache(tmp_path):
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'cache' directories.

    Check that 'cache_dir' is handled if requested.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert not "cache" in exclusion_list
    test_config.set_bool_value("exclude_cache_dir", True)
    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert "cache" in exclusion_list
    assert "Cache" in exclusion_list
    assert not "a dir" in exclusion_list
    logger.close_log()


def test_03_05_dir_exclude_list_trash(tmp_path):
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'trash' directories.

    Check that 'trash_dir' is handled if requested. Includes Linux and Windows.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert not "trash" in exclusion_list
    test_config.set_bool_value("exclude_trash_dir", True)
    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert "trash" in exclusion_list
    assert "Trash" in exclusion_list
    assert "$RECYCLE.BIN" in exclusion_list
    logger.close_log()


def test_03_06_dir_exclude_list_download(tmp_path):
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'download' directories.

    Check that 'download_dir' is handled if requested. Includes Linux and Windows
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert not "Downloads" in exclusion_list
    test_config.set_bool_value("exclude_download_dir", True)
    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.dir_exclude_list
    assert "Downloads" in exclusion_list
    logger.close_log()


# HOLD for windows testing
# def test_03_07_dir_exclude_list_SysVolInfo(tmp_path):
#    """
#    Testing ExternalStorage.dir_exclude_list() for excluding 'SysVolInfo' directories.
#
#    Check that 'System Volumn Info' file is handled if requested. Primarily Windows
#    """
#    test_config = get_test_config()
#    actions = {
#        "verbose": True,
#    }
#    source, dest = filesystem
#    log_file = "tests/test_log.db"
#    logger = Logger(str(dest), log_file)
#    bes = ExternalStorage(test_config, logger, actions)
#    exclusion_list = bes.dir_exclude_list
#    assert not "System Volume Information" in exclusion_list
#    test_config["exclude_sysvolinfo_dir"] = True
#    bes = ExternalStorage(test_config, logger, actions)
#    exclusion_list = bes.dir_exclude_list
#    assert "System Volume Information" in exclusion_list
#    logger.close_log()


def test_03_08_dir_include_list(tmp_path):
    """
    Testing ExternalStorage.dir_include_list() for directories.

    Test the results of ExternalStorage.dir_include_list().
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    inclusion_list = bes.dir_include_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(inclusion_list) == 0

    # check that 'specific_dirs' is picked up
    test_config.write_list("include_specific_dirs", ["a dir"])
    bes = ExternalStorage(test_config, logger, actions)
    inclusion_list = bes.dir_include_list
    assert inclusion_list == test_config.read_list("include_specific_dirs")
    assert "a dir" in inclusion_list
    logger.close_log()


def test_03_09_file_exclude_list_empty(tmp_path):
    """
    Testing ExternalStorage.file_exclude_list() for excluding specific files.

    Test the results of ExternalStorage.file_exclude_list() for
    excluding specific directories.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.file_exclude_list
    assert exclusion_list == test_config.read_list("exclude_specific_files")
    assert len(exclusion_list) == 0
    logger.close_log()


def test_03_11_file_exclude_list(tmp_path):
    """
    Testing ExternalStorage.file_exclude_list() for excluding backup files.

    Check that 'backup_files' (*.~ and *.bak) are handled if requested.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.file_exclude_list
    assert not ".bak" in exclusion_list
    test_config.set_bool_value("exclude_backup_files", True)
    bes = ExternalStorage(test_config, logger, actions)
    exclusion_list = bes.file_exclude_list
    assert "~" in exclusion_list
    assert ".bak" in exclusion_list
    assert not "a file" in exclusion_list
    logger.close_log()


def test_03_12_file_include_list(tmp_path):
    """
    Testing the ExternalStorage.file_include_list() method.

    The inclusion list is controlled by the configuration file entry
    ['file_include']['specific_files'].

    1. Test that an empty list is generated for an empty emtry in the
    config file and the list is not a reference to the config file or
    any of the subsets of the the config file['file_include'] section.

    2. Add a file name to the config file section and test that the
    include list contains the file and again is not a reference to the
    config file or any of the subsets of the the
    config file['file_include'] section.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    inclusion_list = bes.file_include_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(inclusion_list) == 0

    # check that 'specific_files' is picked up
    test_config.write_list("include_specific_files", ["a file"])
    bes = ExternalStorage(test_config, logger, actions)
    inclusion_list = bes.file_include_list
    assert inclusion_list == test_config.read_list("include_specific_files")
    assert "a file" in inclusion_list
    logger.close_log()


def test_03_13_process_file_1(tmp_path):
    """
    Test the results of the ExternalStorage.process_file() method.

    Test for regular files. Backup a file from the source directory to
    the destination directory. Make sure the copied file exists and the
    modification time is the same as the source file time. Update the
    source file (change the modification time) and back up the file.
    Ensure the destination file has the new modification time.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    load_directory_set(directories, dest, False)
    # Test for regular files
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    bes = ExternalStorage(test_config, logger, actions)
    bes.process_file(current_dir, destination_dir, "file1.txt")
    assert os.path.getmtime(current_dir / "file1.txt") == os.path.getmtime(
        destination_dir / "file1.txt"
    )
    # check updating files based on newer date
    new_time = time.time()
    os.utime(current_dir / "file1.txt", (new_time, new_time))
    bes.process_file(current_dir, destination_dir, "file1.txt")
    assert new_time == os.path.getmtime(destination_dir / "file1.txt")
    logger.close_log()


def test_03_14_process_file_2(tmp_path):
    """
    Test the results of the ExternalStorage.process_file() method.

    Test for both good and broken symbolic links in linux only, Windows just
    returns an assert = true.
    """
    if sys.platform.startswith("linux"):
        # set filesystem
        source = tmp_path / "source"
        dest = tmp_path / "dest"
        new_filesys(source, dest)
        test_config = build_config_file(source, dest)
        actions = {"verbose": True}
        log_file = "tests/test_log.db"
        logger = Logger(str(dest), log_file)

        load_directory_set(directories, dest, False)
        bes = ExternalStorage(test_config, logger, actions)
        # good link is copied and bad link is not
        current_dir = source / "test_links"
        destination_dir = dest / "test_links"
        # put linked-to files in destination dir, general file copy
        bes.process_file(current_dir, destination_dir, "good_link.txt")
        assert os.path.isfile(destination_dir / "good_link.txt")
        # now copy good link
        bes.process_file(current_dir, destination_dir, "link_good")
        assert os.path.islink(current_dir / "link_good")
        # Check bad link
        bes.process_file(current_dir, destination_dir, "link_bad")
        assert not os.path.islink(current_dir / "bad_link")
    else:  # Windows doesn't do symlinks well, probably should look at shortcuts
        assert 0
    logger.close_log()


def test_03_15_process_dir_files_1(tmp_path):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir.
    """
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    load_directory_set(directories, dest, False)
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    add_files(additional_files, source / "test1")

    bes = ExternalStorage(test_config, logger, actions)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    for filename in additional_files:
        assert os.path.isfile(destination_dir / filename)
    logger.close_log()


def test_03_16_process_dir_files_2(tmp_path):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except backup files.
    """
    # set filesystem
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    load_directory_set(directories, dest, False)
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    add_files(additional_files, source / "test1")
    # exclude backup files
    test_config.set_bool_value("exclude_backup_files", True)

    bes = ExternalStorage(test_config, logger, actions)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert not os.path.isfile(destination_dir / "backup_file_1~")
    assert not os.path.isfile(destination_dir / "backup_file2.bak")
    assert os.path.isfile(destination_dir / "py_file.py")
    assert os.path.isfile(destination_dir / "py_file.pyc")
    logger.close_log()


def test_03_17_process_dir_files_3(tmp_path):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except cache files.
    """
    # set filesystem
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    test_config = build_config_file(source, dest)
    actions = {"verbose": True}
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    load_directory_set(directories, dest, False)
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    add_files(additional_files, source / "test1")
    # exclude backup files
    test_config.set_bool_value("exclude_cache_files", True)

    bes = ExternalStorage(test_config, logger, actions)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert not os.path.isfile(destination_dir / "cache/file_1.txt")
    assert not os.path.isfile(destination_dir / "cachefile2.txt")
    logger.close_log()


def test_03_18_process_dir_file_4(tmp_path):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except files listed in the config
    setting ['file_exclude']['specific_files'].
    """
    # set filesystem
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    new_filesys(source, dest)
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    load_directory_set(directories, dest, False)
    add_files(additional_files, source / "test1")
    # exclude specific files
    test_config = build_config_file(source, dest)
    test_config.write_list("exclude_specific_files", [".pyc"])
    actions = {
        "verbose": True,
    }
    log_file = "tests/test_log.db"
    logger = Logger(str(dest), log_file)

    bes = ExternalStorage(test_config, logger, actions)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert os.path.isfile(destination_dir / "backup_file_1~")
    assert os.path.isfile(destination_dir / "backup_file2.bak")
    assert os.path.isfile(destination_dir / "py_file.py")
    assert not os.path.isfile(destination_dir / "py_file.pyc")
    logger.close_log()
