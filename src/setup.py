"""
Edit the configuration file for the backup program.

This configuration file provides the criteria for what is saved to the
backup file. The criteria are set as categories of files such as 'cache'
files and 'trash' files along with other settings.

The first time the program is run, a set of default settings are loaded
into the dialog. These can be accepted or modified as desired.then saved
to be used for future runs.

File:       setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT see file LICENSE
Version:    1.1.0
"""

import base64
#import os
from copy import deepcopy
#from datetime import datetime
from typing import Any

from lbk_library.gui import Dialog, Settings

# from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon, QPixmap
#from PySide6.QtWidgets import (  # QMainWindow QApplication, QHeaderView,;
#    QCheckBox,
#    QDialog,
#    QFileDialog,
#    QLineEdit,
#    QMessageBox,
#    QTableWidget,
#    QTableWidgetItem,
#)

from default_config import default_config
from setup_form import Ui_Setup

#file_version = "1.0.0"
#changes = {
#    "1.0.0": "Initial release",
#}


class Setup(Dialog, Ui_Setup):
    """Define the configuration parameters for the backup program."""

    icon_folder = (
        b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/I"
        + b"NwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAGr"
        + b"SURBVDjLxZO7ihRBFIa/6u0ZW7GHBUV0UQQTZzd3QdhMQxOfwMRXEANBMNQX"
        + b"0MzAzFAwEzHwARbNFDdwEd31Mj3X7a6uOr9BtzNjYjKBJ6nicP7v3KqcJFax"
        + b"hBVtZUAK8OHlld2st7Xl3DJPVONP+zEUV4HqL5UDYHr5xvuQAjgl/Qs7TzvO"
        + b"OVAjxjlC+ePSwe6DfbVegLVuT4r14eTr6zvA8xSAoBLzx6pvj4l+DZIezuVk"
        + b"G9fY2H7YRQIMZIBwycmzH1/s3F8AapfIPNF3kQk7+kw9PWBy+IZOdg5Ug3mk"
        + b"AATy/t0usovzGeCUWTjCz0B+Sj0ekfdvkZ3abBv+U4GaCtJ1iEm6ANQJ6fEz"
        + b"rG/engcKw/wXQvEKxSEKQxRGKE7Izt+DSiwBJMUSm71rguMYhQKrBygOIRSt"
        + b"f4TiFFRBvbRGKiQLWP29yRSHKBTtfdBmHs0BUpgvtgF4yRFR+NUKi0XZcYjC"
        + b"eCG2smkzLAHkbRBmP0/Uk26O5YnUActBp1GsAI+S5nRJJJal5K1aAMrq0d6T"
        + b"m9uI6zjyf75dAe6tx/SsWeD//o2/Ab6IH3/h25pOAAAAAElFTkSuQmCC"
    )
    """Define a folder icon to use in the file text boxes."""

#    icon_file = (
#        b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/I' +
#        b'NwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAIN' +
#        b'SURBVBgZBcG/r55zGAfg6/4+z3va01NHlYgzEfE7MdCIGISFgS4Gk8ViYyM2' +
#        b'Mdlsko4GSf8Do0FLRCIkghhYJA3aVBtEz3nP89wf11VJvPDepdd390+8Nso5' +
#        b'nESBQoq0pfvXm9fzWf19453LF85vASqJlz748vInb517dIw6EyYBIIG49u+x' +
#        b'i9/c9MdvR//99MPPZ7+4cP4IZhhTPbwzT2d+vGoaVRRp1rRliVvHq+cfvM3T' +
#        b'D82+7mun0o/ceO7NT+/4/KOXjwZU1ekk0840bAZzMQ2mooqh0A72d5x/6sB9' +
#        b'D5zYnff3PoYBoWBgFKPKqDKqjCpjKr//dcu9p489dra88cydps30KswACfNE' +
#        b'KanSaxhlntjJ8Mv12Paie+vZ+0+oeSwwQ0Iw1xAR1CiFNJkGO4wu3ZMY1AAz' +
#        b'BI0qSgmCNJsJUEOtJSMaCTBDLyQ0CknAGOgyTyFFiLI2awMzdEcSQgSAAKVU' +
#        b'mAeNkxvWJWCGtVlDmgYQ0GFtgg4pNtOwbBcwQy/Rife/2yrRRVI0qYCEBly8' +
#        b'Z+P4qMEMy7JaVw72N568e+iwhrXoECQkfH91kY7jwwXMsBx1L93ZruqrK6uu' +
#        b'iAIdSnTIKKPLPFcvay8ww/Hh+ufeznTXu49v95IMoQG3784gYXdTqvRmqn/W' +
#        b'pa/ADFX58MW3L71SVU9ETgEIQQQIOOzub+fhIvwPRDgeVjWDahIAAAAASUVO' +
#        b'RK5CYII='
#    )

    TOOLTIPS = {
        "start_dir": "Required: The directory to backup. The selected "
        + "directory\n and all sub-directories will be backed up to the"
        + " requested\nbackup location.\nClick the icon to select a "
        + "different directory location.",
        "backup_location": "The location to save the backup to. Click"
        + " the icon to select a different file location.",
        "last_backup": "This is the last time the system was backed up.",
        "value_log_filename": "This file contains the log of the backup actions.",
        "common_next_button": "Move to the 'Excluded Items' tab.",
        "exclude_cache_dir": "Cache directories can generally be excluded\n"
        + "and usually have the form '*/*cache*/'.",
        "exclude_trash_dir": "Trash directoriess can generally be excluded\n"
        + "and have 'trash' or recycle bin' in the name.",
        "exclude_download_dir": "Download directories are freqently "
        + "transient; download something\nand then put it where it belongs,"
        + "so no backup is needed.",
        "exclude_dirs_list": "Specific directories can be noted for exclusion "
        + "as desired. By default,\npython '*venv' (virtual environment) "
        + "directories and python 'tox'\n directories are excluded and should "
        + "be regenerated as needed.\nThis can be changed.",
        "exclude_cache_files": "Some programs use a single file for for the\n"
        + "'cache' rather than a directory. Exclude these files if True.",
        "exclude_backup_files": "Don't need standard backup files generated\n"
        + "by various programs with signatures like '*~' and '*.bak'",
        "exclude_files_list": "Specific files can be noted for exclusion as desired,",
        "exclude_previous_button": "Move to the 'Common' tab.",
        "exclude_next_button": "Move to the 'Included Items' tab.",
        "include_dirs_list": "Specific directories  that would otherwise be\n"
        + "excluded should be specified. Directory names or patterns may be used.",
        "include_files_list": "Specific files that would otherwise be\n"
        + "excluded should be specified. File names or patterns may be used.",
        "include_previous_button": "Move to the 'Excluded Items' tab.",
        "cancel_button": "Close the form. All unsaved changes will be lost.",
        "save_continue_button": "Save the changes made so far.",
        "save_exit_button": "Save the changes made so far, then close the form.",
    }
    """The default tool tips."""

    def __init__(self, config: Settings = None) -> None:
        """
        Initialize the Setup dialog.

        Parameters:
            config (dict): the current configuration settings,
                default is None. If there is no config, the config is 
                initialized to the default config settings,
        """
        super().__init__(None, None, None)
        self.setupUi(self)
        self.config: Settings = config
        """The current configuration settings."""
        self.initial_config: Dict[str, Any] = {}
        """The initial configuration from either self.config  or default config."""
        self.change_made: int = 0
        """ Has a config entry change been made, initially false (all zeros)."""
        self.entry_changed: dict[str, int] = {
            "start_dir": 1,
            "backup_location": 2,
            "exclude_cache_dir": 4,
            "exclude_trash_dir": 8,
            "exclude_download_dir": 16,
            "exclude_cache_files": 32,
            "exclude_backup_files": 64,
            "exclude_dirs_list": 128,
            "exclude_files_list": 256,
            "include_dirs_list": 512,
            "include_files_list": 1024,
        }
        """The binary value in self.change_made for a change to the form entries,"""

        self.set_tooltips()
        self.initial_config = self.initial_setup()
        self.fill_dialog_fields()
#
#        self.start_dir.editingFinished.connect(self.action_start_dir)
#        self.start_dir_action.triggered.connect(self.action_start_dir)
#        self.backup_location_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.backup_location)
#        )
#        self.exclude_dirs_list.cellChanged.connect(self.action_exclude_dirs_list)
#        self.exclude_files_list.cellChanged.connect(self.action_exclude_files_list)
#        self.include_dirs_list.cellChanged.connect(self.action_include_dirs_list)
#        self.include_files_list.cellChanged.connect(self.action_include_files_list)
#
#        self.common_next_button.clicked.connect(self.action_common_next_button_clicked)
#        self.exclude_previous_button.clicked.connect(
#            self.action_exclude_previous_button_clicked
#        )
#        self.exclude_next_button.clicked.connect(
#            self.action_exclude_next_button_clicked
#        )
#        self.include_previous_button.clicked.connect(
#            self.action_include_previous_button_clicked
#        )
#        self.cancel_button.clicked.connect(self.action_cancel_button)
#        self.save_continue_button.clicked.connect(self.action_save_continue_button)
#        self.save_exit_button.clicked.connect(self.action_save_exit_button)

        self.show()

#    def save_config(self) -> None:
#        """ Save the entered configuration values to the config.file."""
#        
#    def action_cancel_button(self) -> None:
#        """
#        Cancel the actions on the form and exit.
#        
#        If there are changes entered, check that the user wants to save 
#        the changes before closing.
#        """
#        changes = self.change_made
#        if changes:
#            result = self.message_box_exec(self.message_question_changed_close("The form Data has "))
#            if result == QMessageBox.StandardButton.Yes:
#                # Save than close
#                self.save_config()
#                self.exit()
#
#            elif result == QMessageBox.StandardButton.No:
#                # Don't save, just close
#                pass
#
#            elif result == QMessageBox.StandardButton.Cancel:
#                # close dialog and return to form.
#                pass
#
#    def action_include_previous_button_clicked(self) -> None:
#        """Move to the 'Excluded Items' tab."""
#        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.exclusions_tab))
#
#    def action_include_files_list(self, row: int, column: int)-> None:
#        """
#        One of the cells in the list has changed.
#
#        If this is the last row in the list, then append an empty row.
#
#        Parameters:
#            row (int) - The row of the cell
#            column (int) - The column of the cell.
#        """
#        if row == self.include_files_list.rowCount() - 1:
#            self.include_files_list.insertRow(self.include_files_list.rowCount())
#
#    def action_include_dirs_list(self, row: int, column: int)-> None:
#        """
#        One of the cells in the list has changed.
#
#        If this is the last row in the list, then append an empty row;
#        otherwise just ignore.
#
#        Parameters:
#            row (int) - The row of the cell
#            column (int) - The column of the cell.
#        """
#        if row == self.include_dirs_list.rowCount() - 1:
#            self.include_dirs_list.insertRow(self.include_dirs_list.rowCount())
#
#    def action_exclude_files_list(self, row: int, column: int) -> None:
#        """
#        One of the cells in the list has changed.
#
#        If this is the last row in the list, then append an empty row.
#
#        Parameters:
#            row (int) - The row of the cell
#            column (int) - The column of the cell.
#        """
#        if row == self.exclude_files_list.rowCount() - 1:
#            self.exclude_files_list.insertRow(self.exclude_files_list.rowCount())
#
#    def action_exclude_dirs_list(self, row: int, column: int) -> None:
#        """
#        One of the cells in the list has changed.
#
#        If this is the last row in the list, then append an empty row;
#        otherwise just ignore.
#
#        Parameters:
#            row (int) - The row of the cell
#            column (int) - The column of the cell.
#        """
#        if row == self.exclude_dirs_list.rowCount() - 1:
#            self.exclude_dirs_list.insertRow(self.exclude_dirs_list.rowCount())
#
#    def action_exclude_previous_button_clicked(self) -> None:
#        """Move to the 'Common Items' tab."""
#        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.common_tab))
#
#    def action_exclude_next_button_clicked(self) -> None:
#        """Move to the 'Included Items' tab."""
#        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.inclusions_tab))
#
#    def action_common_next_button_clicked(self) -> None:
#        """Move to the 'Excluded Items' tab."""
#        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.exclusions_tab))
#
#    def action_start_dir(self) -> None:
#        """Handle a change in the starting directory location."""
#        print(bin(self.change_made))
#        self.open_dir_dialog(self.start_dir)
#        if self.start_dir.text() != self.initial_config["start_dir"]:
#            self.change_made = self.change_made | self.entry_changed["start_dir"]
#        else:
#            self.change_made = self.change_made & ~self.entry_changed["start_dir"]
#        print(bin(self.change_made))
#
#    def open_dir_dialog(self, edit_box: QLineEdit) -> None:
#        """
#        Select a directory from the file dialog.
#
#        Parameters:
#            edit_box (QLineEdit): the line edit box to hold the selected
#                directory.
#        """
#        current_dir = edit_box.text()
#        if current_dir is None or not os.path.isdir(current_dir):
#            current_dir = os.path.expanduser("~")
#
#        new_dir = QFileDialog.getExistingDirectory(
#            edit_box,
#            "Get a Directory Name",
#            current_dir,
#            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
#        )
#        if len(new_dir):
#            edit_box.setText(new_dir)

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields from the initial config file.

        The dialog entries will be filled from the default config file
        if no config file has been stored.
        """
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.common_tab))
        self.fill_common_tab()
#        self.fill_exclude_items_tab()
#        self.fill_include_items_tab()
#
#    def fill_include_items_tab(self) -> None:
#        """
#        Initialize and modify the current included directories and files
#        configuration settings.
#        """
#        self.fill_include_dirs_table()
#        self.fill_include_files_table()
#
#    def fill_include_files_table(self) -> None:
#        """fill the excluded directories table."""
#        listing = self.initial_config["include_specific_files"]
#        self.fill_table(self.include_files_list, listing)
#
#    def fill_include_dirs_table(self) -> None:
#        """fill the included directories table."""
#        listing = self.initial_config["include_specific_dirs"]
#        self.fill_table(self.include_dirs_list, listing)
#
#    def fill_exclude_items_tab(self) -> None:
#        """
#        Initialize and modify the current excluded directories and files
#        configuration settings.
#        """
#        self.initialize_checkboxes()
#        self.fill_exclude_dirs_table()
#        self.fill_exclude_files_table()
#
#    def fill_exclude_files_table(self) -> None:
#        """fill the excluded files table."""
#        listing = self.initial_config["exclude_specific_files"]
#        self.fill_table(self.exclude_files_list, listing)
#
#    def fill_exclude_dirs_table(self) -> None:
#        """fill the excluded directories table."""
#        listing = self.initial_config["exclude_specific_dirs"]
#        self.fill_table(self.exclude_dirs_list, listing)
#
#    def fill_table(self, table_widget: QTableWidget, list_contents: list[str]) -> None:
#        table_widget.setRowCount(len(list_contents) + 1)
#        table_widget.setColumnCount(1)
#        table_widget.horizontalHeader().hide()
#        table_widget.verticalHeader().hide()
#        table_widget.horizontalHeader().setStretchLastSection(True)
#        for i in range(len(list_contents)):
#            table_widget.setItem(i, 0, QTableWidgetItem(list_contents[i]))
#        table_widget.setItem(len(list_contents) + 1, 0, QTableWidgetItem(""))
#
#    def initialize_checkboxes(self) -> None:
#        """Initialize the checkboxes on the excluded page."""
#        self.initialize_checkbox(self.exclude_cache_dir, "exclude_cache_dir")
#        self.initialize_checkbox(self.exclude_trash_dir, "exclude_trash_dir")
#        self.initialize_checkbox(self.exclude_download_dir, "exclude_download_dir")
#        self.initialize_checkbox(self.exclude_cache_files, "exclude_cache_files")
#        self.initialize_checkbox(self.exclude_backup_files, "exclude_backup_files")
#
#    def initialize_checkbox(self, box: QCheckBox, config_name: str) -> None:
#        """
#        Initialize a specific dialog check box.
#        
#        Parameteres:
#            box (QCheckBox) - The checkbox being initialized.
#            config_name str) - the config entry name.
#        """
#        box.setChecked(self.initial_config[config_name])
#        if box.isChecked() != self.config.value(config_name):
#            self.change_made = self.change_made  | self.entry_changed[config_name]
#        else:
#            self.change_made = self.change_made & ~self.entry_changed[config_name]
        
    def fill_common_tab(self) -> None:
        """Initialize the General Settings page of the dialog."""
        self.set_start_directory()
        self.set_backup_location()
        self.set_info_values()

    def set_info_values(self) -> None:
        """Fill the info fields on the 'common' tab of the dialog"""
        last_backup = self.initial_config["last_backup"]
        if last_backup not in ("", "-", "0", 0):
            self.last_backup.setText(
                datetime.fromtimestamp(int(last_backup)).strftime("%H:%M, %b %d, %Y")
            )
        else:
            self.last_backup.setText("0")
        self.value_log_filename.setText(self.initial_config["log_file"])

    def set_backup_location(self) -> None:
        """
        Set the contents and actions of the directory edit box.
        """
        self.backup_location.setText(self.initial_config["backup_location"])
        self.backup_location_action = self.backup_location.addAction(
            self.dir_icon(),
            self.backup_location.ActionPosition.TrailingPosition,
        )
        if self.backup_location.text() != self.config.value("backup_location"):
            self.change_made = self.change_made  | self.entry_changed["backup_location"]
        else:
            self.change_made = self.change_made & ~self.entry_changed["backup_location"]

    def set_start_directory(self) -> None:
        """Set the initial value and actions of the start directory box."""
        self.start_dir.setText(self.initial_config["start_dir"])
        self.start_dir_action = self.start_dir.addAction(
            self.dir_icon(),
            self.start_dir.ActionPosition.TrailingPosition,
        )
        if self.start_dir.text() != self.config.value("start_dir"):
            self.change_made = self.change_made  | self.entry_changed["start_dir"]
        else:
            self.change_made = self.change_made & ~self.entry_changed["start_dir"]

    def initial_setup(self) -> dict[str, Any]:
        """
        Set initial configuration from provided config file or default 
        config.

        Returns:
            dict[str, Any] - The initials set of config settings.
        """
        initial_config = {}
        if len(self.config.allKeys()) == 0:
            # set to default config
            initial_config = deepcopy(default_config)
        else:
            # copy the current config to the initial_config
            config_arrays = [
                "exclude_specific_dirs",
                "exclude_specific_files",
                "include_specific_dirs",
                "include_specific_files",
            ]
            for key in default_config.keys():
                if key in config_arrays:
                    initial_config[key] = self.config.read_list(key)
                else:
                    initial_config[key] = self.config.value(key)
        return initial_config

    def set_tooltips(self) -> None:
        """Set tooltips for all entry elements and buttons."""
        self.start_dir.setToolTip(self.TOOLTIPS["start_dir"])
        self.backup_location.setToolTip(self.TOOLTIPS["backup_location"])
        self.last_backup.setToolTip(self.TOOLTIPS["last_backup"])
        self.value_log_filename.setToolTip(self.TOOLTIPS["value_log_filename"])
        self.common_next_button.setToolTip(self.TOOLTIPS["common_next_button"])

        self.exclude_cache_dir.setToolTip(self.TOOLTIPS["exclude_cache_dir"])
        self.exclude_trash_dir.setToolTip(self.TOOLTIPS["exclude_trash_dir"])
        self.exclude_download_dir.setToolTip(self.TOOLTIPS["exclude_download_dir"])
        self.exclude_dirs_list.setToolTip(self.TOOLTIPS["exclude_dirs_list"])
        self.exclude_cache_files.setToolTip(self.TOOLTIPS["exclude_cache_files"])
        self.exclude_backup_files.setToolTip(self.TOOLTIPS["exclude_backup_files"])
        self.exclude_files_list.setToolTip(self.TOOLTIPS["exclude_files_list"])
        self.exclude_previous_button.setToolTip(
            self.TOOLTIPS["exclude_previous_button"]
        )
        self.exclude_next_button.setToolTip(self.TOOLTIPS["exclude_next_button"])

        self.include_dirs_list.setToolTip(self.TOOLTIPS["include_dirs_list"])
        self.include_files_list.setToolTip(self.TOOLTIPS["include_files_list"])
        self.include_previous_button.setToolTip(
            self.TOOLTIPS["include_previous_button"]
        )

        self.cancel_button.setToolTip(self.TOOLTIPS["cancel_button"])
        self.save_continue_button.setToolTip(self.TOOLTIPS["save_continue_button"])
        self.save_exit_button.setToolTip(self.TOOLTIPS["save_exit_button"])

    def dir_icon(cls) -> None:
        """
        Create the directory icon for a widget

        Returns:
            QIcon - an icon of a folder
        """
        dir_open_pixmap = QPixmap()
        dir_open_pixmap.loadFromData(base64.b64decode(Setup.icon_folder))
        return QIcon(dir_open_pixmap)


