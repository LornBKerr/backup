"""
Result Codes for Backup actions

File:       result_codes.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see LICENSE file
"""


class ResultCodes:
    """
    Provides result codes for various actions happening during the backup
    process.
    """

    SUCCESS = 0
    """ The current action completed successfully """

    NO_CONFIG_FILE = 3
    """ The configuration file could not be found, run setup (-s or --setup) """

    FILE_NOT_COPIED = 4
    """ During file backup to External Storage, a file failed to copy. """

    NO_SOURCE_OR_DESTINATION = 5
    """ Need to specify both the source and destination directories """
