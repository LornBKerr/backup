"""
Edit the configuration file for the backup program.

File:       setup_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT see file LICENSE
"""

import base64
import os
from datetime import datetime
from typing import Any

from lbk_library import IniFileParser
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QLineEdit, QMainWindow
from PyQt6 import uic

from default_config import default_config
#from tab_pages.tab_page import TabPage
#from tab_pages.general_page import GeneralPage
#from tab_pages.excluded_page import ExcludedPage


class SetupWindow(QMainWindow):
    """
    Define the common elements for the tab pages contained in the
    tab widget for the setup program for the backup program.
    """
        # define a directory icon to use in the directory text boxes
    icon_folder = (
        b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/I' +
        b'NwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAGr' +
        b'SURBVDjLxZO7ihRBFIa/6u0ZW7GHBUV0UQQTZzd3QdhMQxOfwMRXEANBMNQX' +
        b'0MzAzFAwEzHwARbNFDdwEd31Mj3X7a6uOr9BtzNjYjKBJ6nicP7v3KqcJFax' +
        b'hBVtZUAK8OHlld2st7Xl3DJPVONP+zEUV4HqL5UDYHr5xvuQAjgl/Qs7TzvO' +
        b'OVAjxjlC+ePSwe6DfbVegLVuT4r14eTr6zvA8xSAoBLzx6pvj4l+DZIezuVk' +
        b'G9fY2H7YRQIMZIBwycmzH1/s3F8AapfIPNF3kQk7+kw9PWBy+IZOdg5Ug3mk' +
        b'AATy/t0usovzGeCUWTjCz0B+Sj0ekfdvkZ3abBv+U4GaCtJ1iEm6ANQJ6fEz' +
        b'rG/engcKw/wXQvEKxSEKQxRGKE7Izt+DSiwBJMUSm71rguMYhQKrBygOIRSt' +
        b'f4TiFFRBvbRGKiQLWP29yRSHKBTtfdBmHs0BUpgvtgF4yRFR+NUKi0XZcYjC' +
        b'eCG2smkzLAHkbRBmP0/Uk26O5YnUActBp1GsAI+S5nRJJJal5K1aAMrq0d6T' +
        b'm9uI6zjyf75dAe6tx/SsWeD//o2/Ab6IH3/h25pOAAAAAElFTkSuQmCC'
    )
        # define a file icon to use in the file text boxes
    icon_file = (
        b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/I' +
        b'NwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAIN' +
        b'SURBVBgZBcG/r55zGAfg6/4+z3va01NHlYgzEfE7MdCIGISFgS4Gk8ViYyM2' +
        b'Mdlsko4GSf8Do0FLRCIkghhYJA3aVBtEz3nP89wf11VJvPDepdd390+8Nso5' +
        b'nESBQoq0pfvXm9fzWf19453LF85vASqJlz748vInb517dIw6EyYBIIG49u+x' +
        b'i9/c9MdvR//99MPPZ7+4cP4IZhhTPbwzT2d+vGoaVRRp1rRliVvHq+cfvM3T' +
        b'D82+7mun0o/ceO7NT+/4/KOXjwZU1ekk0840bAZzMQ2mooqh0A72d5x/6sB9' +
        b'D5zYnff3PoYBoWBgFKPKqDKqjCpjKr//dcu9p489dra88cydps30KswACfNE' +
        b'KanSaxhlntjJ8Mv12Paie+vZ+0+oeSwwQ0Iw1xAR1CiFNJkGO4wu3ZMY1AAz' +
        b'BI0qSgmCNJsJUEOtJSMaCTBDLyQ0CknAGOgyTyFFiLI2awMzdEcSQgSAAKVU' +
        b'mAeNkxvWJWCGtVlDmgYQ0GFtgg4pNtOwbBcwQy/Rife/2yrRRVI0qYCEBly8' +
        b'Z+P4qMEMy7JaVw72N568e+iwhrXoECQkfH91kY7jwwXMsBx1L93ZruqrK6uu' +
        b'iAIdSnTIKKPLPFcvay8ww/Hh+ufeznTXu49v95IMoQG3784gYXdTqvRmqn/W' +
        b'pa/ADFX58MW3L71SVU9ETgEIQQQIOOzub+fhIvwPRDgeVjWDahIAAAAASUVO' +
        b'RK5CYII='
    )
    """
    Setup the configuration file for the backup.
    """
    def __init__(self, config: dict[str, Any], config_handler: IniFileParser) -> None:
        """
        Initialize the Setup dialog.

        Parameters:
            app (QApplication): the QApplication instance.
            config (dict): the current configuration settings, may be empty
            config_handler (IniFileParser): read and write the configuration
                settings
        """
        super().__init__()

        self.config = config
        if not self.config:
            self.config = default_config

        # Fill the form fields
        self.form = uic.loadUi("src/forms/setup_window.ui", self)

        # Fill the dialog fields
        self.fill_dialog_fields()


#
##        # set cancel/save button bar
#
        self.form.general_next.clicked.connect(
            self.action_general_next_clicked
        )
        # Set Excluded Items page action handling

#        self.edit_specific_dir_excld_1_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_1)
#        )
#        self.form.edit_specific_dir_excld_1.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_1
#            )
#        )
#        self.edit_specific_dir_excld_2_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_2)
#        )
#        self.form.edit_specific_dir_excld_2.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_2
#            )
#        )
#        self.edit_specific_dir_excld_3_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_3)
#        )
#        self.form.edit_specific_dir_excld_3.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_3
#            )
#        )
#        self.edit_specific_dir_excld_4_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_4)
#        )
#        self.form.edit_specific_dir_excld_4.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_4
#            )
#        )
#        self.edit_specific_dir_excld_5_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_5)
#        )
#        self.form.edit_specific_dir_excld_5.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_5
#            )
#        )
#        self.edit_specific_dir_excld_6_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_6)
#        )
#        self.form.edit_specific_dir_excld_6.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_6
#            )
#        )
#        self.edit_specific_dir_excld_7_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_7)
#        )
#        self.form.edit_specific_dir_excld_7.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_7
#            )
#        )
#        self.edit_specific_dir_excld_8_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_8)
#        )
#        self.form.edit_specific_dir_excld_8.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_8
#            )
#        )
#        self.edit_specific_dir_excld_9_action.triggered.connect(
#            lambda: self.action_open_dir_dialog(self.edit_specific_dir_excld_9)
#        )
#        self.form.edit_specific_dir_excld_9.editingFinished.connect(
#            lambda: self.action_exclude_specific_dirs(
#                self.form.edit_specific_dir_excld_9
#            )
#        )
#
#        self.edit_specific_file_excld_1_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_1)
#        )
#        self.form.edit_specific_file_excld_1.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_1
#            )
#        )
#        self.edit_specific_file_excld_2_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_2)
#        )
#        self.form.edit_specific_file_excld_2.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_2
#            )
#        )
#        self.edit_specific_file_excld_3_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_3)
#        )
#        self.form.edit_specific_file_excld_3.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_3
#            )
#        )
#        self.edit_specific_file_excld_4_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_4)
#        )
#        self.form.edit_specific_file_excld_4.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_4
#            )
#        )
#        self.edit_specific_file_excld_5_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_5)
#        )
#        self.form.edit_specific_file_excld_5.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_5
#            )
#        )
#        self.edit_specific_file_excld_6_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_6)
#        )
#        self.form.edit_specific_file_excld_6.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_6
#            )
#        )
#        self.edit_specific_file_excld_7_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_7)
#        )
#        self.form.edit_specific_file_excld_7.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_7
#            )
#        )
#        self.edit_specific_file_excld_8_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_8)
#        )
#        self.form.edit_specific_file_excld_8.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_8
#            )
#        )
#        self.edit_specific_file_excld_9_action.triggered.connect(
#            lambda: self.action_open_file_dialog(self.edit_specific_file_excld_9)
#        )
#        self.form.edit_specific_file_excld_9.editingFinished.connect(
#            lambda: self.action_exclude_specific_files(
#                self.form.edit_specific_file_excld_9
#            )
#        )
#        
#        self.form.btn_excld_previous.clicked.connect(self.action_btn_excld_previous_clicked)
#        self.form.btn_excld_next.clicked.connect(self.action_btn_excld_next_clicked)
        
        self.show()

    # end __init__()

    # ##################################################################
    # Build the icons and handle the file/dir choosing
    # ##################################################################
    
    @staticmethod
    def dir_icon() -> None:
        """
        Create the directory icon for a widget
        
        Returns:
            QIcon - an icon of a folder
        """
        dir_open_pixmap = QPixmap()
        dir_open_pixmap.loadFromData(base64.b64decode(SetupWindow.icon_folder))
        return QIcon(dir_open_pixmap)
    
    @staticmethod
    def file_icon() -> None:
        """
        Create the file icon for a widget
        
        Returns:
            QIcon - an icon of a page representing a a file
        """
        dir_open_pixmap = QPixmap()
        dir_open_pixmap.loadFromData(base64.b64decode(SetupWindow.icon_filer))
        return QIcon(dir_open_pixmap)

    def action_open_dir_dialog(self, edit_box: QLineEdit) -> None:
        """
        Select a directory from the file dialog.

        Parameters:
            edit_box (QLineEdit): the line edit box to hold the selected
                directory.
        """
        current_dir = edit_box.text()
        if current_dir is None or not os.path.isdir(current_dir):
            current_dir = os.path.expanduser("~")

        new_dir = QFileDialog.getExistingDirectory(edit_box, "Get a Directory Name",
                                                current_dir,
                                                QFileDialog.Option.ShowDirsOnly
                                                | QFileDialog.Option.DontResolveSymlinks)
        if len(new_dir):
            edit_box.setText(new_dir)

    # end action_open_dir_dialog()

    def action_open_file_dialog(self, edit_box: QLineEdit) -> None:
        """
        Select a file from the file dialog.

        Parameters:
            edit_box (QIlneEdit): the line edit box to hold the selected
                directory.
        """
        current_file = os.getcwd()
        if current_file is None or not os.path.isdir(current_file):
            current_file = os.path.expanduser("~")

        new_filename = QFileDialog.getOpenFileName(edit_box, "Get a Filename",
                                                current_file)
        if len(new_filename[0]):
            edit_box.setText(new_filename[0])

    # end action_open_file_dialog()

    # ##################################################################
    # Set the actions for the general page
    # ##################################################################

    def action_start_dir_changed(self) -> None:
        """
        Save the form start directory entry in the config.
        """
        self.config["general"]["base_dir"] = self.form.start_dir.text()
        # end action_start_dir_changed()

    def action_external_storage(self, state_changed: int = 0) -> None:
        """
        Update the external storage settings based on state of the
        external storage checkbox.

        If checked, enable the Excluded Items and Included Items tabs
        and the backup destination directory selection box. If not
        checked, disables these items

        Parameters:
            state_changed (int) not used.
        """
        do_external_storage = self.form.external_storage.isChecked()
        if do_external_storage:
            self.form.lbl_backup_dir.setEnabled(True)
            self.form.backup_dir.setEnabled(True)
        else:
            self.form.lbl_backup_dir.setEnabled(False)
            self.form.backup_dir.setEnabled(False)

        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.exclusions_tab),
            do_external_storage,
        )
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.inclusions_tab),
            do_external_storage,
        )
        self.form.general_next.setEnabled(
            do_external_storage or self.form.cloud_storage.isChecked()
        )
        self.config["general"]["external_storage"] = do_external_storage

    # end action_external_storage()

    def action_backup_dir_changed(self) -> None:
        """
        Save the form backup directory entry in the config.
        """
        self.config["general"]["backup_dir"] = self.form.backup_dir.text()

    # end action_backup_dir_changed()

    def action_cloud_storage(self, state_changed: int = 0) -> None:
        """
        Enable or disable the Cloud Storage tab based on the new setting
        of the Cloud Storage checkbox.
        """
        do_cloud_storage = self.form.cloud_storage.isChecked()
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.cloud_storage_tab),
            do_cloud_storage,
        )
        self.form.general_next.setEnabled(
            do_cloud_storage or self.form.external_storage.isChecked()
        )
        self.config["general"]["cloud_storage"] = do_cloud_storage

    # end action_cloud_storage()

    def action_general_next_clicked(self) -> None:
        """
        Move to the next active page, if any.

        If "External Storage" is selected, then move to the "Excluded Items"
        tab. Otherwise if "Cloud Storage is selected, move to the
        "Cloud Storage" tab.
        """
        if self.form.external_storage.isChecked():
            self.form.tabWidget.setCurrentIndex(
                self.form.tabWidget.indexOf(self.form.exclusions_tab)
            )
        elif self.form.cloud_storage.isChecked():
            self.form.tabWidget.setCurrentIndex(
                self.form.tabWidget.indexOf(self.form.cloud_storage_tab)
            )

    # end action_general_next_clicked()

    # ##################################################################
    # Set the actions for the excluded page
    # ##################################################################

    def action_excld_cache_dir(self, state_changed: int) -> None:
        """
        Update the config["dir_exclude"]["cache_dir"] value on change.

        Parameters:
            state_changed (int) not used.
        """
        self.config["dir_exclude"]["cache_dir"] = self.form.excld_cache_dir.isChecked()
    # end action_excld_download_dir()


    def action_excld_trash_dir(self, state_changed: int) -> None:
        """
        Update the config["dir_exclude"]["trash_dir"] value on change.

        Parameters:
            state_changed (int) not used.
        """
        self.config["dir_exclude"]["trash_dir"] = self.form.excld_trash_dir.isChecked()
    # end action_excld_download_dir()

    def action_excld_download_dir(self, state_changed: int) -> None:
        """
        Update the config["dir_exclude"]["download_dir"] value on change.

        Parameters:
            state_changed (int) not used.
        """
        self.config["dir_exclude"]["download_dir"] = self.form.excld_download_dir.isChecked()
    # end action_excld_download_dir()

    def action_excld_cache_files(self, state_changed: int) -> None:
        """
        Update the config["file_exclude"]["cache_files"] value on change.

        Parameters:
            state_changed (int) not used.
        """
        self.config["file_exclude"]["cache_files"] = self.form.excld_cache_files.isChecked()
    # end action_excld_cache_files()

    def action_excld_backup_files(self, state_changed: int) -> None:
        """
        Update the config["file_exclude"]["backup_files"] value on change.

        Parameters:
            state_changed (int) not used.
        """
        self.config["file_exclude"]["backup_files"] = self.form.excld_backup_files.isChecked()
    # end action_excld_backup_files()






    # ##################################################################
    # Fill the dialog fields
    # ##################################################################

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields from the current config file.

        Add custom actions to the 'set directory/file' edit boxes to
        open a file dialog as required.

        The dialog entries will be filled from the default config file
        if no config file has been stored.
        """
        # set startup page
        self.form.tabWidget.setCurrentIndex(
            self.form.tabWidget.indexOf(self.form.general_tab)
        )

        # fill the form tabs
        self.fill_general_tab()
        self.fill_excluded_items_tab()




#
    # end fill_dialog_fields()

    def fill_general_tab(self) -> None:
        """
        Initialize the General Settings page of the Setup dialog.
        """
        self.set_start_dir()
        self.set_external_storage()
        self.set_cloud_storage()
        self.set_info_values()

        self.form.general_next.clicked.connect(
            self.action_general_next_clicked
        )
    # end fill_general_tab()
    
    def fill_excluded_items_tab(self) -> None:
        """
        Initialize and modify the current excluded directories and files
        configuration settings.
        """
        self.initialize_checkboxes()
        self.fill_excld_dirs_table()
        self.fill.excld_files_table()

    # end fill_excluded_items_tab()





    # Fill details of general page
    
    def set_start_dir(self) -> None:
        """
        Set the contents and actions of the starting directory edit box.
        """
        start_dir = self.config["general"]["base_dir"]
        if not start_dir:
            start_dir = os.path.expanduser("~")
        self.form.start_dir.setText(start_dir)
        self.start_dir_action = self.form.start_dir.addAction(
            self.dir_icon(),
            self.form.start_dir.ActionPosition.TrailingPosition,
        )
        self.start_dir_action.triggered.connect(
            lambda: self.action_open_dir_dialog(self.form.start_dir)
        )
        self.form.start_dir.editingFinished.connect(
            self.action_start_dir_changed
        )

    # end set_start_dir()

    def set_external_storage(self) -> None:
        """
        Set the contents and actions of the external storage checkbox
        and directory edit box.
        """
        external_storage = self.config["general"]["external_storage"]
        self.form.external_storage.setChecked(external_storage)
        self.action_external_storage(True)

        backup_dir = self.config["general"]["backup_dir"]
        self.form.backup_dir.setText(backup_dir)

        self.backup_dir_action = self.form.backup_dir.addAction(
            self.dir_icon(),
            self.form.backup_dir.ActionPosition.TrailingPosition,
        )
        self.form.external_storage.stateChanged.connect(
            self.action_external_storage
        )

        self.backup_dir_action.triggered.connect(
            lambda: self.action_open_dir_dialog(self.form.backup_dir)
        )
        self.form.backup_dir.editingFinished.connect(
            self.action_backup_dir_changed
        )

    # end set_external_storage()

    def set_cloud_storage(self) -> None:
        """
        Set the contents and actions of the cloud storagee checkbox.
        """
        cloud_storage = self.config["general"]["cloud_storage"]
        self.form.cloud_storage.setChecked(cloud_storage)
        self.form.tabWidget.setTabEnabled(
            self.form.tabWidget.indexOf(self.form.cloud_storage_tab),
            cloud_storage,
        )

        self.form.cloud_storage.stateChanged.connect(
            self.action_cloud_storage
        )

    # end set_cloud_storage()

    def set_info_values(self) -> None:
        """
        Fill the info fields on the 'General' tab of the dialog
        """
        last_backup_timestamp = self.config["general"]["last_backup"]
        self.form.value_last_backup.setText(
            datetime.fromtimestamp(last_backup_timestamp).strftime("%H:%M %b %d, %Y")
        )
        self.form.value_config_filename.setText(
            self.config["general"]["config_file"]
        )
        self.form.value_config_dir.setText(self.config["general"]["config_dir"])
        self.form.value_log_filename.setText(self.config["general"]["log_file"])

    # end set_info_values()

    # fill details of the excluded items tab

    def initialize_checkboxes(self) -> None:
        """
        Initialize the checkboxes on the excluded page.
        
        Set the check state and assign the action for the check state
        change for each box.
        """
        self.form.excld_cache_dir.setChecked(self.config["dir_exclude"]["cache_dir"])
        self.form.excld_cache_dir.stateChanged.connect(self.action_excld_cache_dir)

        self.form.excld_trash_dir.setChecked(self.config["dir_exclude"]["trash_dir"])
        self.form.excld_trash_dir.stateChanged.connect(self.action_excld_trash_dir)

        self.form.excld_download_dir.setChecked(self.config["dir_exclude"]["download_dir"])
        self.form.excld_download_dir.stateChanged.connect(self.action_excld_download_dir)

        self.form.excld_cache_files.setChecked(self.config["file_exclude"]["cache_files"])
        self.form.excld_cache_files.stateChanged.connect(self.action_excld_cache_files)

        self.form.excld_backup_files.setChecked(self.config["file_exclude"]["backup_files"])
        self.form.excld_cache_dir.stateChanged.connect(self.action_excld_cache_files)
    # end initialize_checkboxes

    def fill_excld_dirs_table(self) -> None:
    
    
    #end fill_excld_dirs_table()

    def fill_excld_files_table(self) -> None:


    # end fill_excld_files_table()



## end Class SetupWindow
