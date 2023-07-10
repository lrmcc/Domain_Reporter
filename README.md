# Domain Reporter 
## Domain Record Monitor and Alert Tool

### Overview
Logs WHOIS domain status.

## How to use it
Launch the __main__.py file.
### What it does now 
Monitors attribute changes in WHOIS records (i.e. registration and domain status) over specified durations and frequencies to allow for alert triggers.

### Upcoming features
- Alert on changes, and only record changes
- Monitor other WHOIS attributes besides domain status
- Email alerts

### Prequisites:
1. WHOIS is installed
2. Allow file creation/modification within script directory

## Known Issues:
1. On MacOS it is possible the gui may appear dark. This is due to issues with Tkinter arising from updates to MacOS and Python. I was able to over come it by using virtualenv and few attempts at solutions found in these posts:
https://stackoverflow.com/questions/71294521/tkinter-window-appears-black-upon-running-in-pycharm
https://stackoverflow.com/questions/72472167/deprecation-warning-the-system-version-of-tk-is-deprecated-m1-mac-in-vs-code
https://stackoverflow.com/questions/5459444/tkinter-python-may-not-be-configured-for-tk
