"""
Test the Setup class functionality.

#File:       test_01_setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library.gui import Settings
from lbk_library.testing_support import filesystem
from PySide6.QtCore import QCoreApplication, QSettings, Qt
from PySide6.QtWidgets import QDialog, QFileDialog, QTableWidgetItem

from default_config import default_config
from setup import Setup

filename = "test_01_setup.py"
file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Revised to test new Setup class.",
}


def build_window(qtbot, tmp_path):
    test_dir = filesystem(tmp_path)
    starting_dir = test_dir + "/start"
    os.mkdir(starting_dir)
    dest_dir = test_dir + "/dest"
    os.mkdir(dest_dir)

    QCoreApplication.setOrganizationName("LBK Software")
    QCoreApplication.setApplicationName("Backup")
    filename = starting_dir + "/.config/test.conf"
    config = Settings(filename, QSettings.IniFormat)
    setup = Setup(config)
    return (setup, starting_dir, dest_dir)


def close_window(window):
    window.config.remove("")
    window.close()


def load_test_config(window):
    window.config.setValue("starting_dir", "a_dir")
    window.config.setValue("backup_location", "a_dir")
    window.config.setValue("last_backup", "100")

    window.config.setValue("exclude_cache_dir", False)
    window.config.setValue("exclude_trash_dir", True)
    window.config.setValue("exclude_download_dir", False)
    window.config.setValue("exclude_cache_files", True)
    window.config.setValue("exclude_backup_files", True)

    window.config.write_list("exclude_specific_dirs", ["a", "b", "c"])
    window.config.write_list("exclude_specific_files", ["d", "e", "f", "z"])
    window.config.write_list("include_specific_dirs", ["h", "i", "j", "y", "x"])
    window.config.write_list("include_specific_files", ["k", "l", "m", "x", "y", "z"])


def test_01_01_Setup(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    assert isinstance(setup, Setup)
    assert isinstance(setup, QDialog)
    close_window(setup)


def test_01_02_initial_setup(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    active_config = setup.config
    assert (len(active_config.allKeys())) == 0

    initial_config = setup.initial_setup()
    for key in initial_config.keys():
        assert initial_config[key] == default_config[key]

    setup.config.setValue("last_backup", "10000")
    setup.config.write_list("exclude_specific_dirs", ["x", "y", "z"])
    initial_config = setup.initial_setup()
    for key in initial_config.keys():
        if key == "last_backup":
            assert initial_config[key] == "10000"
        elif key == "exclude_specific_dirs":
            assert initial_config[key] == ["x", "y", "z"]
    close_window(setup)


def test_01_03_set_tooltips(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.set_tooltips()
    assert setup.start_dir.toolTip() == setup.TOOLTIPS["start_dir"]
    assert setup.backup_location.toolTip() == setup.TOOLTIPS["backup_location"]
    assert setup.last_backup.toolTip() == setup.TOOLTIPS["last_backup"]
#    assert setup.log_file.toolTip() == setup.TOOLTIPS["log_file"]
    assert setup.common_next_button.toolTip() == setup.TOOLTIPS["common_next_button"]

    assert setup.exclude_cache_dir.toolTip() == setup.TOOLTIPS["exclude_cache_dir"]
    assert setup.exclude_trash_dir.toolTip() == setup.TOOLTIPS["exclude_trash_dir"]
    assert (
        setup.exclude_download_dir.toolTip() == setup.TOOLTIPS["exclude_download_dir"]
    )
    assert (
        setup.exclude_specific_dirs.toolTip() == setup.TOOLTIPS["exclude_specific_dirs"]
    )
    assert (
        setup.exclude_backup_files.toolTip() == setup.TOOLTIPS["exclude_backup_files"]
    )
    assert (
        setup.exclude_specific_files.toolTip()
        == setup.TOOLTIPS["exclude_specific_files"]
    )
    assert (
        setup.exclude_previous_button.toolTip()
        == setup.TOOLTIPS["exclude_previous_button"]
    )
    assert setup.exclude_next_button.toolTip() == setup.TOOLTIPS["exclude_next_button"]
    assert (
        setup.include_specific_dirs.toolTip() == setup.TOOLTIPS["include_specific_dirs"]
    )
    assert (
        setup.include_specific_files.toolTip()
        == setup.TOOLTIPS["include_specific_files"]
    )
    assert (
        setup.include_previous_button.toolTip()
        == setup.TOOLTIPS["include_previous_button"]
    )
    assert setup.cancel_button.toolTip() == setup.TOOLTIPS["cancel_button"]
    assert (
        setup.save_continue_button.toolTip() == setup.TOOLTIPS["save_continue_button"]
    )
    assert setup.save_exit_button.toolTip() == setup.TOOLTIPS["save_exit_button"]
    close_window(setup)


def test_01_04_set_start_dir(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.change_made = 0
    setup.set_start_directory()
    assert setup.start_dir.text() == default_config["start_dir"]
    assert setup.change_made == setup.entry_changed["start_dir"]

    setup.config.setValue("start_dir", default_config["start_dir"])
    setup.set_start_directory()
    assert setup.start_dir.text() == default_config["start_dir"]
    assert setup.change_made == 0
    close_window(setup)


def test_01_05_set_backup_Location(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.change_made = 0
    setup.set_backup_location()
    assert setup.backup_location.text() == default_config["backup_location"]
    assert setup.change_made == setup.entry_changed["backup_location"]

    setup.config.setValue("backup_location", default_config["backup_location"])
    setup.set_backup_location()
    assert setup.backup_location.text() == default_config["backup_location"]
    assert setup.change_made == 0
    close_window(setup)


def test_01_06_set_info_values(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.set_info_values()
    assert setup.last_backup.text() == default_config["last_backup"]
    close_window(setup)


def test_01_07_fill_common_tab(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.fill_common_tab()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(setup.common_tab)
    assert setup.start_dir.text() == default_config["start_dir"]
    assert setup.backup_location.text() == default_config["backup_location"]
    assert setup.last_backup.text() == default_config["last_backup"]
    close_window(setup)


def test_01_08_initialize_checkboxes(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.change_made = 0xF000
    setup.initialize_checkboxes()
    assert (
        setup.exclude_cache_dir.isChecked() == setup.initial_config["exclude_cache_dir"]
    )
    assert (
        setup.exclude_trash_dir.isChecked() == setup.initial_config["exclude_trash_dir"]
    )
    assert (
        setup.exclude_download_dir.isChecked()
        == setup.initial_config["exclude_download_dir"]
    )
    assert (
        setup.exclude_backup_files.isChecked()
        == setup.initial_config["exclude_backup_files"]
    )

    test_mask = (
        setup.entry_changed["exclude_cache_dir"]
        + setup.entry_changed["exclude_trash_dir"]
        + setup.entry_changed["exclude_download_dir"]
        + setup.entry_changed["exclude_backup_files"]
    )

    assert setup.change_made & test_mask == test_mask
    setup.config.setValue("exclude_download_dir", True)
    setup.initialize_checkboxes()
    assert (
        setup.change_made & test_mask
        == test_mask & ~setup.entry_changed["exclude_download_dir"]
    )


def test_01_09_fill_table(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.fill_table(setup.exclude_specific_dirs, [])
    assert setup.exclude_specific_dirs.rowCount() == 1

    new_list = ["A", "B", "c"]
    setup.fill_table(setup.exclude_specific_dirs, new_list)
    assert setup.exclude_specific_dirs.rowCount() == 4
    assert (
        setup.exclude_specific_dirs.item(0, 0).data(Qt.ItemDataRole.EditRole)
        == new_list[0]
    )
    assert (
        setup.exclude_specific_dirs.item(1, 0).data(Qt.ItemDataRole.EditRole)
        == new_list[1]
    )
    assert (
        setup.exclude_specific_dirs.item(2, 0).data(Qt.ItemDataRole.EditRole)
        == new_list[2]
    )
    assert setup.exclude_specific_dirs.item(3, 0) == None
    close_window(setup)


def test_01_10_fill_exclude_dirs_table(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.initial_config["exclude_specific_dirs"] = []
    setup.fill_exclude_dirs_table()
    assert (
        setup.exclude_specific_dirs.rowCount()
        == len(setup.initial_config["exclude_specific_dirs"]) + 1
    )

    new_list = ["A", "B", "C"]
    setup.initial_config["exclude_specific_dirs"] = new_list
    setup.fill_exclude_dirs_table()
    assert setup.exclude_specific_dirs.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.exclude_specific_dirs.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_11_fill_exclude_files_table(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.initial_config["exclude_specific_files"] = []
    setup.fill_exclude_files_table()
    assert (
        setup.exclude_specific_files.rowCount()
        == len(setup.initial_config["exclude_specific_files"]) + 1
    )

    new_list = ["A", "B", "C"]
    setup.initial_config["exclude_specific_files"] = new_list
    setup.fill_exclude_files_table()
    assert setup.exclude_specific_files.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.exclude_specific_files.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_12_fill_exclude_items_tab(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    new_list = ["A", "B", "C"]
    setup.initial_config["exclude_specific_dirs"] = new_list
    setup.initial_config["exclude_specific_files"] = new_list

    setup.fill_exclude_items_tab()
    assert setup.exclude_cache_dir.isChecked()
    assert setup.exclude_trash_dir.isChecked()
    assert setup.exclude_download_dir.isChecked()
    assert setup.exclude_backup_files.isChecked()
    assert setup.exclude_specific_dirs.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.exclude_specific_dirs.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    assert setup.exclude_specific_files.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.exclude_specific_files.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_13_fill_include_dirs_table(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.initial_config["include_specific_dirs"] = []
    setup.fill_include_dirs_table()
    assert (
        setup.include_specific_dirs.rowCount()
        == len(setup.initial_config["include_specific_dirs"]) + 1
    )

    new_list = ["A", "B", "C"]
    setup.initial_config["include_specific_dirs"] = new_list
    setup.fill_include_dirs_table()
    assert setup.include_specific_dirs.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.include_specific_dirs.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_14_fill_include_files_table(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.initial_config["include_specific_files"] = []
    setup.fill_include_files_table()
    assert (
        setup.include_specific_files.rowCount()
        == len(setup.initial_config["include_specific_files"]) + 1
    )

    new_list = ["A", "B", "C"]
    setup.initial_config["include_specific_files"] = new_list
    setup.fill_include_files_table()
    assert setup.include_specific_files.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.include_specific_files.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_15_fill_include_items_tab(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.fill_include_items_tab()
    assert (
        setup.include_specific_dirs.rowCount()
        == len(setup.initial_config["include_specific_dirs"]) + 1
    )
    assert (
        setup.include_specific_files.rowCount()
        == len(setup.initial_config["include_specific_files"]) + 1
    )

    new_list = ["A", "B", "C"]
    setup.initial_config["include_specific_dirs"] = new_list
    setup.initial_config["include_specific_files"] = new_list
    setup.fill_include_items_tab()
    assert setup.include_specific_dirs.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.include_specific_dirs.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    assert setup.include_specific_files.rowCount() == len(new_list) + 1
    for i in range(len(new_list)):
        assert (
            setup.include_specific_files.item(i, 0).data(Qt.ItemDataRole.EditRole)
            == new_list[i]
        )
    close_window(setup)


def test_01_16_fill_dialog_fields(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.fill_dialog_fields()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(setup.common_tab)
    assert setup.start_dir.text() == default_config["start_dir"]
    assert setup.backup_location.text() == default_config["backup_location"]
    assert setup.last_backup.text() == default_config["last_backup"]

    assert setup.exclude_cache_dir.isChecked()
    assert setup.exclude_trash_dir.isChecked()
    assert setup.exclude_download_dir.isChecked()
    assert setup.exclude_backup_files.isChecked()
    assert (
        setup.exclude_specific_dirs.rowCount()
        == len(default_config["exclude_specific_dirs"]) + 1
    )
    assert (
        setup.exclude_specific_files.rowCount()
        == len(default_config["exclude_specific_files"]) + 1
    )
    assert (
        setup.exclude_specific_files.rowCount()
        == len(setup.initial_config["exclude_specific_files"]) + 1
    )
    assert (
        setup.include_specific_dirs.rowCount()
        == len(setup.initial_config["include_specific_dirs"]) + 1
    )
    assert (
        setup.include_specific_files.rowCount()
        == len(setup.initial_config["include_specific_files"]) + 1
    )
    close_window(setup)


def test_01_17_open_dir_dialog(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.start_dir.setText(None)
    mocker.patch.object(QFileDialog, "getExistingDirectory")
    QFileDialog.getExistingDirectory.return_value = os.path.expanduser("~")
    setup.open_dir_dialog(setup.start_dir)
    assert setup.start_dir.text() == os.path.expanduser("~")

    setup.start_dir.setText("")
    QFileDialog.getExistingDirectory.return_value = ""
    setup.open_dir_dialog(setup.start_dir)
    assert setup.start_dir.text() == ""

    setup.start_dir.setText(os.path.expanduser("~"))
    QFileDialog.getExistingDirectory.return_value = (
        os.path.expanduser("~") + "/Pictures"
    )
    setup.open_dir_dialog(setup.start_dir)
    assert setup.start_dir.text() == os.path.expanduser("~") + "/Pictures"
    close_window(setup)


def test_01_18_action_start_dir(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.change_made = 0
    setup.start_dir.setText(setup.initial_config["start_dir"])
    mocker.patch.object(QFileDialog, "getExistingDirectory")
    QFileDialog.getExistingDirectory.return_value = setup.initial_config["start_dir"]
    setup.action_start_dir()
    assert setup.change_made == 0

    setup.start_dir.setText(setup.initial_config["start_dir"])
    mocker.patch.object(QFileDialog, "getExistingDirectory")
    QFileDialog.getExistingDirectory.return_value = (
        setup.initial_config["start_dir"] + "/Downloads"
    )
    setup.start_dir_action.trigger()
    assert setup.change_made == setup.entry_changed["start_dir"]
    close_window(setup)


def test_01_19_action_backup_location(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    setup.change_made = 0
    setup.backup_location.setText(setup.initial_config["backup_location"])
    mocker.patch.object(QFileDialog, "getExistingDirectory")
    QFileDialog.getExistingDirectory.return_value = setup.initial_config[
        "backup_location"
    ]
    setup.action_backup_location()
    assert setup.change_made == 0

    setup.backup_location.setText(setup.initial_config["backup_location"])
    mocker.patch.object(QFileDialog, "getExistingDirectory")
    QFileDialog.getExistingDirectory.return_value = (
        setup.initial_config["backup_location"] + "/Downloads"
    )
    setup.backup_location_action.trigger()
    assert setup.change_made == setup.entry_changed["backup_location"]
    close_window(setup)


def test_01_20_action_common_next_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(setup.common_tab)
    setup.common_next_button.click()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.exclusions_tab
    )
    close_window(setup)


def test_01_21_action_checkbox_clicked(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    for check_box, name in [
        (setup.exclude_cache_dir, "exclude_cache_dir"),
        (setup.exclude_trash_dir, "exclude_trash_dir"),
        (setup.exclude_download_dir, "exclude_download_dir"),
        (setup.exclude_backup_files, "exclude_backup_files"),
    ]:
        setup.change_made = 0
        assert check_box.isChecked() == setup.initial_config[name]
        check_box.click()
        assert check_box.isChecked() != setup.initial_config[name]
        assert setup.change_made == setup.entry_changed[name]

        check_box.click()
        assert check_box.isChecked() == setup.initial_config[name]
        assert setup.change_made == 0


def test_01_22_action_exclude_specific_dirs(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    new_list = ["A", "B", "C"]
    setup.fill_table(setup.exclude_specific_dirs, new_list)
    assert setup.exclude_specific_dirs.rowCount() == len(new_list) + 1
    setup.exclude_specific_dirs.setItem(0, 0, QTableWidgetItem("YYY"))
    assert setup.exclude_specific_dirs.rowCount() == len(new_list) + 1
    setup.exclude_specific_dirs.setItem(len(new_list), 0, QTableWidgetItem("YYY"))
    assert setup.exclude_specific_dirs.rowCount() == len(new_list) + 2
    close_window(setup)


def test_01_23_action_exclude_specific_files(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    new_list = ["A", "B", "C"]
    setup.fill_table(setup.exclude_specific_files, new_list)
    assert setup.exclude_specific_files.rowCount() == len(new_list) + 1
    setup.exclude_specific_files.setItem(0, 0, QTableWidgetItem("YYY"))
    assert setup.exclude_specific_files.rowCount() == len(new_list) + 1
    setup.exclude_specific_files.setItem(len(new_list), 0, QTableWidgetItem("YYY"))
    assert setup.exclude_specific_files.rowCount() == len(new_list) + 2
    close_window(setup)


def test_01_24_action_exclude_previous_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    setup.tabWidget.setCurrentIndex(setup.tabWidget.indexOf(setup.exclusions_tab))
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.exclusions_tab
    )
    setup.exclude_previous_button.click()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(setup.common_tab)
    close_window(setup)


def test_01_25_action_exclude_next_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    setup.tabWidget.setCurrentIndex(setup.tabWidget.indexOf(setup.exclusions_tab))
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.exclusions_tab
    )
    setup.exclude_next_button.click()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.inclusions_tab
    )
    close_window(setup)


def test_01_26_action_include_specific_dirs(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    new_list = ["A", "B", "C"]
    setup.fill_table(setup.include_specific_dirs, new_list)
    assert setup.include_specific_dirs.rowCount() == len(new_list) + 1
    setup.include_specific_dirs.setItem(0, 0, QTableWidgetItem("YYY"))
    assert setup.include_specific_dirs.rowCount() == len(new_list) + 1
    setup.include_specific_dirs.setItem(len(new_list), 0, QTableWidgetItem("YYY"))
    assert setup.include_specific_dirs.rowCount() == len(new_list) + 2
    close_window(setup)


def test_01_27_action_include_specific_files(qtbot, tmp_path, mocker):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    new_list = ["A", "B", "C"]
    setup.fill_table(setup.include_specific_files, new_list)
    assert setup.include_specific_files.rowCount() == len(new_list) + 1
    setup.include_specific_files.setItem(0, 0, QTableWidgetItem("YYY"))
    assert setup.include_specific_files.rowCount() == len(new_list) + 1
    setup.include_specific_files.setItem(len(new_list), 0, QTableWidgetItem("YYY"))
    assert setup.include_specific_files.rowCount() == len(new_list) + 2
    close_window(setup)


def test_01_29_action_include_previous_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)
    load_test_config(setup)

    setup.tabWidget.setCurrentIndex(setup.tabWidget.indexOf(setup.inclusions_tab))
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.inclusions_tab
    )
    setup.include_previous_button.click()
    assert setup.tabWidget.currentIndex() == setup.tabWidget.indexOf(
        setup.exclusions_tab
    )
    close_window(setup)


def test_01_29_get_table_list(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    new_list = ["A", "B", "C"]
    setup.fill_table(setup.include_specific_files, new_list)
    assert setup.include_specific_files.rowCount() == len(new_list) + 1
    a_list = setup.get_table_list(setup.include_specific_files)
    assert len(a_list) == len(new_list)
    for i in range(0, len(new_list)):
        assert a_list[i] in new_list
    close_window(setup)


def test_01_30_save_config(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    new_list = ["A", "B", "C"]
    setup.backup_location.setText("zxy")
    setup.fill_table(setup.include_specific_files, new_list)

    setup.save_config()
    assert setup.config.value("start_dir") == setup.start_dir.text()
    assert setup.config.value("backup_location") == setup.backup_location.text()
    assert (
        setup.config.bool_value("exclude_cache_dir")
        == setup.exclude_cache_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_trash_dir")
        == setup.exclude_trash_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_download_dir")
        == setup.exclude_download_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_backup_files")
        == setup.exclude_backup_files.isChecked()
    )
    assert setup.config.read_list("exclude_specific_dirs") == setup.get_table_list(
        setup.exclude_specific_dirs
    )
    assert setup.config.read_list("exclude_specific_files") == setup.get_table_list(
        setup.exclude_specific_files
    )
    assert setup.config.read_list("include_specific_dirs") == setup.get_table_list(
        setup.include_specific_dirs
    )
    assert setup.config.read_list("include_specific_files") == setup.get_table_list(
        setup.include_specific_files
    )


def test_01_31_action_save_continue_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    new_list = ["A", "B", "C"]
    setup.backup_location.setText("zxy")
    setup.fill_table(setup.include_specific_files, new_list)
    setup.save_continue_button.click()

    assert setup.config.value("start_dir") == setup.start_dir.text()
    assert setup.config.value("backup_location") == setup.backup_location.text()
    assert (
        setup.config.bool_value("exclude_cache_dir")
        == setup.exclude_cache_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_trash_dir")
        == setup.exclude_trash_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_download_dir")
        == setup.exclude_download_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_backup_files")
        == setup.exclude_backup_files.isChecked()
    )
    assert setup.config.read_list("exclude_specific_dirs") == setup.get_table_list(
        setup.exclude_specific_dirs
    )
    assert setup.config.read_list("exclude_specific_files") == setup.get_table_list(
        setup.exclude_specific_files
    )
    assert setup.config.read_list("include_specific_dirs") == setup.get_table_list(
        setup.include_specific_dirs
    )
    assert setup.config.read_list("include_specific_files") == setup.get_table_list(
        setup.include_specific_files
    )


def test_01_32_action_save_exit_button(qtbot, tmp_path):
    setup, starting_dir, dest_dir = build_window(qtbot, tmp_path)

    new_list = ["A", "B", "C"]
    setup.backup_location.setText("zxy")
    setup.fill_table(setup.include_specific_files, new_list)
    setup.save_exit_button.click()

    assert setup.config.value("start_dir") == setup.start_dir.text()
    assert setup.config.value("backup_location") == setup.backup_location.text()
    assert (
        setup.config.bool_value("exclude_cache_dir")
        == setup.exclude_cache_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_trash_dir")
        == setup.exclude_trash_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_download_dir")
        == setup.exclude_download_dir.isChecked()
    )
    assert (
        setup.config.bool_value("exclude_backup_files")
        == setup.exclude_backup_files.isChecked()
    )
    assert setup.config.read_list("exclude_specific_dirs") == setup.get_table_list(
        setup.exclude_specific_dirs
    )
    assert setup.config.read_list("exclude_specific_files") == setup.get_table_list(
        setup.exclude_specific_files
    )
    assert setup.config.read_list("include_specific_dirs") == setup.get_table_list(
        setup.include_specific_dirs
    )
    assert setup.config.read_list("include_specific_files") == setup.get_table_list(
        setup.include_specific_files
    )

    assert setup.isHidden()  # dialogs are hidden waiting garbage collection.
