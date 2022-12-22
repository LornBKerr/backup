"""
Edit the configuration file for the backup program.

File:       setup_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT see file LICENSE
"""

import os
from datetime import datetime
from typing import Any

from lbk_library import IniFileParser, Validate
from PyQt6.QtWidgets import QApplication, QFileDialog, QLineEdit, QMainWindow, QStyle
from PyQt6 import uic

from default_config import default_config


class SetupWindow(QMainWindow):
    """
    Setup the configuration file for the backup.
    """

    def __init__(
        self, app: QApplication, config: dict[str, Any], config_handler: IniFileParser
    ) -> None:
        """
        Initialize the Setup dialog.

        Parameters:
            app (QApplication) the QApplication instance.
            config: (dict) the current configuration settings, may be empty
            config_handler (IniFileParser) read and write the configuration
                settings
        """
        super().__init__()
        self.app = app
        self.setWindowTitle("Setup")
        self.validate = Validate()  # setup input validator

        self.config = config
        if not self.config:
            self.config = default_config

        # Fill the form fields
        self.form = uic.loadUi("src/forms/setup_window.ui", self)
        self.fill_dialog_fields()
        #
        #        # set dialog element actions
        #        # set cancel/save button bar

        # set general page action handling
        self.edit_start_dir_action.triggered.connect(
            lambda: self.action_open_file_dialog(self.form.edit_start_dir)
        )
        self.form.chkbx_external_storage.stateChanged.connect(
            self.action_chkbx_external_storage
        )
        self.edit_backup_dir_action.triggered.connect(
            lambda: self.action_open_file_dialog(self.form.edit_backup_dir)
        )
        self.form.chkbx_cloud_storage.stateChanged.connect(
            self.action_chkbx_cloud_storage
        )
        self.form.btn_general_next.clicked.connect(self.action_btn_general_next_clicked)

        self.show()

    # end __init__()

    # Action Handlers
    def action_open_file_dialog(self, parent: QLineEdit = None) -> None:
        """
        Select a directory from the file dialog.

        Parameters:
            parent (QIlneEdit): the line edit box to hold the selected
                directory.
        """
        dir = QFileDialog.getExistingDirectory(
            parent, "Select Directory", os.path.expanduser("~")
        )
        parent.setText(dir)

    # action_open_file_dialog()

    def action_chkbx_external_storage(self, state_changed: int = 0) -> None:
        """
        Update the external storage settings based on state of the
        external storage checkbox.

        If checked, enable the Excluded Items and Included Items tabs
        and the backup destination directory selection box. If not
        checked, disables these items

        Parameters:
            state_changed (int) not used.
        """
        chkbx_external_storage = self.form.chkbx_external_storage.isChecked()
        if chkbx_external_storage:
            self.form.lbl_backup_dir.setEnabled(True)
            self.form.edit_backup_dir.setEnabled(True)
        else:
            self.form.lbl_backup_dir.setEnabled(False)
            self.form.edit_backup_dir.setEnabled(False)

        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.exclusions_tab),
            chkbx_external_storage,
        )
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.inclusions_tab),
            chkbx_external_storage,
        )
        self.form.btn_general_next.setEnabled(
            chkbx_external_storage or self.form.chkbx_cloud_storage.isChecked()
        )

    # end action_chkbx_external_storage()

    def action_chkbx_cloud_storage(self, state_changed: int = 0) -> None:
        """
        Enable or disable the Cloud Storage tab based on the new setting
        of the Cloud Storage checkbox.
        """
        chkbx_cloud_storage = self.form.chkbx_cloud_storage.isChecked()
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.cloud_storage_tab),
            chkbx_cloud_storage,
        )
        self.form.btn_general_next.setEnabled(
            chkbx_cloud_storage or self.form.chkbx_external_storage.isChecked()
        )

    # end action_chkbx_cloud_storage()

    def action_btn_general_next_clicked(self) -> None:
        """
        Move to the next active page, if any.

        If "External Storage" is selected, then move to the "Excluded Items"
        tab. Otherwise if "Cloud Storage is selected, move to the
        "Cloud Storage" tab.
        """
        if self.form.chkbx_external_storage.isChecked():
            self.form.tabWidget.setCurrentIndex(
                self.form.tabWidget.indexOf(self.form.exclusions_tab)
            )
        elif self.form.chkbx_cloud_storage.isChecked():
            self.form.tabWidget.setCurrentIndex(
                self.form.tabWidget.indexOf(self.form.cloud_storage_tab)
            )

    # end action_btn_general_next_clicked()

    # Fill the form customizing elements as necessary and set custom actions.
    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields from the current config file.

        The dialog entries will be filled from the default config file
        if no config file has been stored.
        """
        # define a directory icon to use in the file and diretory text boxes
        self.dir_icon = self.app.style().standardIcon(
            QStyle.StandardPixmap.SP_DirOpenIcon
        )

        # set startup page
        self.form.tabWidget.setCurrentIndex(
            self.form.tabWidget.indexOf(self.form.general_tab)
        )

        # fill the form tabs
        self.fill_general_tab(self.config)
        self.fill_excluded_items_tab(self.config)

    # end fill_dialog_fields()

    def fill_general_tab(self, config: dict[str, Any]) -> None:
        """
        Fill the fields on the 'General' tab of the dialog

        Parameters:
            config (dict) the set of configuration settings.
        """
        start_dir = self.config["general"]["base_dir"]
        if not start_dir:
            start_dir = os.path.expanduser("~")
        self.form.edit_start_dir.setText(start_dir)
        self.edit_start_dir_action = self.form.edit_start_dir.addAction(
            self.dir_icon, self.form.edit_start_dir.ActionPosition.TrailingPosition
        )

        external_storage = self.config["general"]["external_storage"]
        self.form.chkbx_external_storage.setChecked(external_storage)
        self.action_chkbx_external_storage(external_storage)
        backup_dir = self.config["general"]["backup_dir"]
        self.form.edit_backup_dir.setText(backup_dir)
        self.edit_backup_dir_action = self.form.edit_backup_dir.addAction(
            self.dir_icon, self.form.edit_backup_dir.ActionPosition.TrailingPosition
        )

        cloud_storage = self.config["general"]["cloud_storage"]
        self.form.chkbx_cloud_storage.setChecked(cloud_storage)
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.cloud_storage_tab), cloud_storage
        )

        last_backup_timestamp = self.config["general"]["last_backup"]
        self.form.value_last_backup.setText(
            datetime.fromtimestamp(last_backup_timestamp).strftime("%H:%M %b %d, %Y")
        )

        self.form.value_config_filename.setText(self.config["general"]["config_file"])

        self.form.value_config_dir.setText(self.config["general"]["config_dir"])

        self.form.value_log_filename.setText(self.config["general"]["log_file"])

    # end fill_general_tab()

    def fill_excluded_items_tab(self, config: dict[str, Any]) -> None:
        self.form.chkbx_excld_cache_dir.setChecked(config["dir_exclude"]["cache_dir"])
        self.form.chkbx_excld_trash_dir.setChecked(config["dir_exclude"]["trash_dir"])
    
    
##        self.specific_file_excld_1 = self.form.specific_file_excld_1.addAction(
##            file_icon, self.form.specific_file_excld_1.ActionPosition.TrailingPosition
##        )
#

#
# end Class SetupWindow
