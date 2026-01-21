# A Backup Program for Linux and Windows.

## File Backup

Backup the '/home/{user}' file system to the backup storage and to cloud storage. This is a program built to satisfy my own way of working. It may or may not be useful to others. The basic usage is either at the command line or run automatically at some set time. For Linux, this automatic run can be done with either a cron job or using System-D. For Windows, use the built in Task Scheduler program. See (https://www.howtogeek.com/123393/how-to-automatically-run-programs-and-set-reminders-with-the-windows-task-scheduler/) for example.

Logging of results is automatic using a database and includes start and stop times, elapsed time, and any errors occurring. Adding the verbose option also sets the logging to verbose mode adding more information on files and directories backed up and errors.

The program is written in Python and is tested on Fedora Linux ( and soon Windows 11) using Python versions 3.14 with no errors and greater than 90% coverage.

### Backup to external storage

Backup any new and changed files in the global home directory to the backup directory on an external disk drive. A new file is one that has been added or renamed since the last backup. A changed file is defined as one whose modification time stamp is greater than the last stored backup time stamp.

Any new directories needed are created in the backup store and new/changed files are copied to the store.

## Usage

At the command prompt, enter backup \[args\].

Arguments (all are optional, -b is default if none are given):

- \-s, --setup Run the setup portion to configure the program. Currently sets the file source and destination directories to default values and enables backup to the external storage device. Note that these are specific to my system and will need to be changed for other systems.

- \-b, --backup Run the backup portion. This is the default if no other option is included, required if backup is desired when other options are included. It will fail with a message to the console and to the log if no configuration is found.

- \-v, --verbose Show information as program steps through the file backup process. When verbose mode is selected, the verbose messages are also added to the log.  
    
- \--version Display the version information for the program.

Single letter arguments (-s, -b, and -v) can be used individually or can be combined into a single argument and order does not matter.

For example, to setup the program then run a backup, you can use

setup -v -s

or

setup -sv

or

setup -vs

are all equivalent.

1.  **Examples**:
2.  \[[me@thebes](mailto:me@thebes)\]$ backup
3.  Will run the backup program with the previously stored configuration file; equivalent to
4.  backup -b.

6.  \[[me@thebes](mailto:me@thebes)\]$ backup –setup or
7.  \[[me@thebes](mailto:me@thebes)\]$ backup -s
8.  Will run the backup program opening the configuration window. When the configuration window is closed, the program will be terminated.

10. \[[me@thebes](mailto:me@thebes)\]> backup --setup -b or
11. \[[me@thebes](mailto:me@thebes)\]> backup -sb
12. Will first open the configuration window then, when the window is closed, runs the backup.

14. \[[me@thebes](mailto:me@thebes)\]> backup -b -v or
15. \[[me@thebes](mailto:me@thebes)\]> backup -bv
16. Will run the backup program with the previously stored configuration file. Additional progress messages will be sent to standard output along with any error messages. The logging subsystem will also save the additional messages. Note that the setup option must be run, before a file backup can be run.

## Installation

The program build and installation files are in the folder ‘install/linux’ and ‘install/windows’.

**For Linux:**

Run the shell program ‘install/linux/build_backup_exe.sh’ which will form a single executable file from the python source files.

Then run the shell program ‘install/linux/install.sh’ to install the systemd service to automatically run the backup program. The service timer is set to run at about 3 am every day within a window of 1 hour. In practice, on my machine, systemd does not wake the computer, so the backup runs on the first startup of the day.

\---

Author: Lorn B Kerr (lornburtkerr at gmail dot com)

Copyright: (c) 2022/2025 Lorn B Kerr

License: MIT License; see file LICENSE
