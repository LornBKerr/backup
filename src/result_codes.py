"""
Result Codes for Backup actions.

File:       result_codes.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see LICENSE file
"""


class ResultCodes:
    """Provides result codes for actions during the backup process."""

    SUCCESS = 0
    """Current action completed successfully. """

    NO_CONFIG_FILE = 3
    """Configuration file could not be found, run setup (--setup)."""

    FILE_NOT_COPIED = 4
    """File failed to copy during file backup to External Storage."""

    NO_SOURCE_OR_DESTINATION = 5
    """Need to specify both the source and destination directories. """

    NO_EXTERNAL_STORAGE = 6
    """Could not access the External Storage Drive."""
