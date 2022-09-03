<# ############################
Build the backup executable file.

Windows 11 Variant

File:       build_backup_executable.bat
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see file LICENSE

############################ #>

<# Clean out old build and dist fiels
then make the executable as one file and no console window.
#>
if (Test-Path '.\build') {
    Remove-Item -path '.\build' -Recurse
}

if (Test-Path '.\dist') {
    Remove-Item -path '.\dist' -Recurse
}

if (Test-Path '.\backup.spec') {
    Remove-Item -path '.\backup.spec' -Recurse
}

pyinstaller --onefile --noconsole C:\Users\kerrl\development\backup\src\backup.py

