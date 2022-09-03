:: ############################
:: Build the backup executable file.
::
:: Windows 11 Variant
::
:: File:       build_backup_executable.bat
:: Author:     Lorn B Kerr
:: Copyright:  (c) 2022 Lorn B Kerr
:: License:    see file LICENSE
::
:: ############################

:: Make the executable as one file and no console window.
pyinstaller --onefile --noconsole C:\Users\kerrl\development\backup\src\backup.py

