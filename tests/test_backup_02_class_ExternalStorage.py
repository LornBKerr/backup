# command --> pytest --cov-report term-missing --cov=backup ./tests/
#   run from parent directory for 'src' and 'tests'.

import os
import sys
import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

# import pytest
from build_filesystem import (
    add_files,
    additional_files,
    directories,
    filesystem,
    get_test_config,
    load_directory_set,
)
from external_storage import ExternalStorage

# from lbk_library import IniFileParser


def test_01():
    """
    Testing Backup.ExternalStorage.__init__()

    Test the the object object is really a ExternalStorage class
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    assert isinstance(bes, ExternalStorage)
    # end test_01()


def test_02():
    """
    Testing ExternalStorage.dir_exclude_list() with no exclusions.

    Test the results of ExternalStorage.dir_exclude_list() for
    no exclusions. Should be an empty list.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(exclusion_list) == 0
    assert not exclusion_list is test_config["dir_exclude"]["specific_dirs"]
    assert not exclusion_list is test_config["dir_exclude"]
    assert not exclusion_list is test_config
    # end test_02()


def test_03():
    """
    Testing ExternalStorage.dir_exclude_list() for excluding specific directories.

    Test the results of ExternalStorage.dir_exclude_list() for
    excluding specific directories.
    """
    # check that 'specific_dirs' is picked up
    test_config = get_test_config()
    test_config["dir_exclude"]["specific_dirs"].append("a dir")
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert exclusion_list == test_config["dir_exclude"]["specific_dirs"]
    assert not exclusion_list is test_config["dir_exclude"]["specific_dirs"]
    assert "a dir" in exclusion_list
    # end test_03()


def test_04():
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'cache' directories.

    Check that 'cache_dir' is handled if requested.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert not "cache" in exclusion_list
    test_config["dir_exclude"]["cache_dir"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert "cache" in exclusion_list
    assert "Cache" in exclusion_list
    assert not "a dir" in exclusion_list
    # end test_04()


def test_05_dir_exclude_trash_dirs():
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'trash' directories.

    Check that 'trash_dir' is handled if requested. Includes Linux and Windows.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert not "trash" in exclusion_list
    test_config["dir_exclude"]["trash_dir"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert "trash" in exclusion_list
    assert "Trash" in exclusion_list
    assert "$RECYCLE.BIN" in exclusion_list
    # end test_05()


def test_06():
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'download' directories.

    Check that 'download_dir' is handled if requested. Includes Linux and Windows
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert not "Downloads" in exclusion_list
    test_config["dir_exclude"]["download_dir"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert "Downloads" in exclusion_list
    # end test_06()


def test_07_dir():
    """
    Testing ExternalStorage.dir_exclude_list() for excluding 'SysVolInfo' directories.

    Check that 'System Volumn Info' file is handled if requested. Primarily Windows
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert not "System Volume Information" in exclusion_list
    test_config["dir_exclude"]["sysVolInfo_dir"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.dir_exclude_list
    assert "System Volume Information" in exclusion_list
    # end test_07()


def test_08():
    """
    Testing ExternalStorage.dir_include_list() for directories.

    Test the results of ExternalStorage.dir_include_list().
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    inclusion_list = bes.dir_include_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(inclusion_list) == 0
    assert not inclusion_list is test_config["dir_include"]["specific_dirs"]
    assert not inclusion_list is test_config["dir_include"]
    assert not inclusion_list is test_config
    # check that 'specific_dirs' is picked up
    test_config["dir_include"]["specific_dirs"].append("a dir")
    bes = ExternalStorage(test_config)
    inclusion_list = bes.dir_include_list
    assert inclusion_list == test_config["dir_include"]["specific_dirs"]
    assert not inclusion_list is test_config["dir_include"]["specific_dirs"]
    assert "a dir" in inclusion_list
    # end test_08()


def test_09():
    """
    Testing ExternalStorage.file_exclude_list() for not excluding any files.

    Test the results of ExternalStorage.file_exclude_list() for
    no exclusions. Should be an empty list.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(exclusion_list) == 0
    assert not exclusion_list is test_config["file_exclude"]["specific_files"]
    assert not exclusion_list is test_config["file_exclude"]
    assert not exclusion_list is test_config
    # end test_09()


def test_10():
    """
    Testing ExternalStorage.file_exclude_list() for excluding specific files.

    Test the results of ExternalStorage.file_exclude_list() for
    excluding specific directories.
    """
    # check that 'specific_files' is picked up
    test_config = get_test_config()
    test_config["file_exclude"]["specific_files"].append("a file")
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    assert exclusion_list == test_config["file_exclude"]["specific_files"]
    assert not exclusion_list is test_config["file_exclude"]["specific_files"]
    assert "a file" in exclusion_list
    # end test_10()


def test_11():
    """
    Testing ExternalStorage.file_exclude_list() for excluding backup files.

    Check that 'backup_files' (*.~ and *.bak) are handled if requested.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    assert not ".bak" in exclusion_list
    test_config["file_exclude"]["backup_files"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    assert "~" in exclusion_list
    assert ".bak" in exclusion_list
    assert not "a file" in exclusion_list
    # end test_11()


def test_12():
    """
    Testing ExternalStorage.file_exclude_list() for excluding 'cache' files.

    Check that files containing 'cache' in the name is handled if requested.
    """
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    assert not "cache" in exclusion_list
    test_config["file_exclude"]["cache_files"] = True
    bes = ExternalStorage(test_config)
    exclusion_list = bes.file_exclude_list
    assert "cache" in exclusion_list
    assert "Cache" in exclusion_list
    assert not "a file" in exclusion_list
    # end test_12()


def test_13():
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
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    inclusion_list = bes.file_include_list
    # empty list and not a empty subset of any of the pieces of test_config.
    assert len(inclusion_list) == 0
    assert not inclusion_list is test_config["file_include"]["specific_files"]
    assert not inclusion_list is test_config["file_include"]
    assert not inclusion_list is test_config
    # check that 'specific_files' is picked up
    test_config["file_include"]["specific_files"].append("a file")
    bes = ExternalStorage(test_config)
    inclusion_list = bes.file_include_list
    assert inclusion_list == test_config["file_include"]["specific_files"]
    assert not inclusion_list is test_config["file_include"]["specific_files"]
    assert "a file" in inclusion_list
    # end test_13()


def test_14(filesystem):
    """
    Test the results of the ExternalStorage.process_file() method.

    Test for regular files. Backup a file from the source directory to
    the destination directory. Make sure the copied file exists and the
    modification time is the same as the source file time. Update the
    source file (change the modification time) and back up the file.
    Ensure the destination file has the new modification time.
    """
    # set filesystem
    source, dest = filesystem
    test_config = get_test_config()
    bes = ExternalStorage(test_config)
    load_directory_set(directories, dest, False)
    # Test for regular files
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    bes.process_file(current_dir, destination_dir, "file1.txt")
    assert os.path.getmtime(current_dir / "file1.txt") == os.path.getmtime(
        destination_dir / "file1.txt"
    )
    # check updating files based on newer date
    new_time = time.time()
    os.utime(current_dir / "file1.txt", (new_time, new_time))
    bes.process_file(current_dir, destination_dir, "file1.txt")
    assert new_time == os.path.getmtime(destination_dir / "file1.txt")
    # end test_14()


def test_15(filesystem):
    """
    Test the results of the ExternalStorage.process_file() method.

    Test for both good and broken symbolic links in linux only, Windows just returns an assert = true.
    """
    if sys.platform.startswith("linux"):
        # set filesystem
        source, dest = filesystem
        test_config = get_test_config()
        bes = ExternalStorage(test_config)
        load_directory_set(directories, dest, False)
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
    else:  # Windows doesn't do symlinks well probably should look at shortcuts
        assert 1
    # test_15()


def test_16_process_dir_files(filesystem):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir.
    """
    # set filesystem
    source, dest = filesystem
    load_directory_set(directories, dest, False)
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    add_files(additional_files, source / "test1")
    # All files should be present in dir 'test1'
    test_config = get_test_config(source, dest)
    bes = ExternalStorage(test_config)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    for filename in additional_files:
        assert os.path.isfile(destination_dir / filename)
    # end test_16_process_dir_file()


def test_17_process_dir_file_exclude_backup_files(filesystem):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except backup files.
    """
    # set filesystem
    source, dest = filesystem
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    load_directory_set(directories, dest, False)
    add_files(additional_files, source / "test1")
    # exclude backup files
    test_config = get_test_config(source, dest)
    test_config["file_exclude"]["backup_files"] = True
    bes = ExternalStorage(test_config)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert not os.path.isfile(destination_dir / "backup_file_1~")
    assert not os.path.isfile(destination_dir / "backup_file2.bak")
    assert os.path.isfile(destination_dir / "file_is_cache_file")
    assert os.path.isfile(destination_dir / "py_file.py")
    assert os.path.isfile(destination_dir / "py_file.pyc")
    # end test_17()


def test_18(filesystem):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except cache files.
    """
    # set filesystem
    source, dest = filesystem
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    load_directory_set(directories, dest, False)
    add_files(additional_files, source / "test1")
    # exclude backup files
    source, dest = filesystem
    test_config = get_test_config(source, dest)
    test_config["file_exclude"]["cache_files"] = True
    bes = ExternalStorage(test_config)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert os.path.isfile(destination_dir / "backup_file_1~")
    assert os.path.isfile(destination_dir / "backup_file2.bak")
    assert not os.path.isfile(destination_dir / "file_is_cache_file")
    assert os.path.isfile(destination_dir / "py_file.py")
    assert os.path.isfile(destination_dir / "py_file.pyc")
    # end test_18()


def test_19(filesystem):
    """
    Test the results of the ExternalStorage.process_dir_files() method.

    Include all files in test1 dir except files listed in the config
    setting ['file_exclude']['specific_files'].
    """
    # set filesystem
    source, dest = filesystem
    current_dir = source / "test1"
    destination_dir = dest / "test1"
    load_directory_set(directories, dest, False)
    add_files(additional_files, source / "test1")
    # exclude specific files
    test_config = get_test_config(source, dest)
    test_config["file_exclude"]["specific_files"] = [".pyc"]
    bes = ExternalStorage(test_config)
    bes.process_dir_files(current_dir, destination_dir, additional_files)
    assert os.path.isfile(destination_dir / "backup_file_1~")
    assert os.path.isfile(destination_dir / "backup_file2.bak")
    assert os.path.isfile(destination_dir / "file_is_cache_file")
    assert os.path.isfile(destination_dir / "py_file.py")
    assert not os.path.isfile(destination_dir / "py_file.pyc")
    # end test_19()


def test_20(filesystem):
    """
    Test the overall program with a base config file.

    All exclusion and inclusion choices are off. The base dir and backup
    locations are set to temparary locations. All files and directories
    should be copied except for broken links wich are always ignored.
    """
    # set filesystem
    source, dest = filesystem
    destination_dir = dest / "backup"
    add_files(additional_files, source / "test1")
    test_config = get_test_config(source, destination_dir)
    bes = ExternalStorage(test_config)
    for a_dir in directories:
        for filename in os.listdir(source / a_dir):
            if not os.path.islink(source / a_dir / filename):
                assert os.path.exists(destination_dir / a_dir / filename)
            else:
                if os.path.isfile(source / a_dir / filename):
                    assert os.path.isfile(destination_dir / a_dir / filename)
                else:
                    assert not os.path.isfile(destination_dir / a_dir / filename)
    # end test_20()


def test_21(filesystem):
    """
    Test the overall program excluding cache directories.

    Exclude 'cache' is turned on, all other exclusion and inclusion
    choices are off. The base dir and backup locations are set to
    temparary locations. Cache files should not be copied.
    """
    # set filesystem
    source, dest = filesystem
    destination_dir = dest / "backup"
    add_files(additional_files, source / "test1")
    test_config = get_test_config(source, destination_dir)
    test_config["dir_exclude"]["cache_dir"] = True
    bes = ExternalStorage(test_config)
    exclusions = bes.dir_exclude_list
    for a_dir in directories:
        if a_dir == "Cache" or a_dir == "cache":
            assert not os.path.exists(destination_dir / a_dir)
        else:
            assert os.path.exists(destination_dir / a_dir)
    # end test_21()


# end test_backup_02_clss_ExternalStorage.py
