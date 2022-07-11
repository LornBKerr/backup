"""
Manage the database log of backup actions.

File:       logger.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see LICENSE file
"""

import os

from lbk_library import Dbal


class Logger:
    """
    Manage the database log of backup actions.
    """
    def __init__(self, log_path: str) -> None:
        """
        Setup the path to the log file and open the log database.
        
        Parameters:
            log_path (str): the path to the log database
        """
        self.log_db: Dbal
        """ the log database """
        self.log_path = log_path
        """ The full path to the logging database """
        
        # Open or create the database file.
        if os.path.exists(self.log_path):
            self.log_db = Dbal()
            self.log_db.sql_connect(elf.log_path)
        else:
            self.create_log_database(self.log_path)
    
    # end __init__()
    
    
    
    
    
    
    
    
    
    
    
    def create_log_database(self, log_path: str):
        pass
    # end cteate_log_database()
    
           
