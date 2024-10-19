# rclone-drive-sync
Simple python script to periodically mirror files from a google drive folder, meant for jellyfin servers.<br>
## Installation
This script requires python (obviously), rclone and optionally, a working google cloud API Key.<br>
First, install rclone and configure it by running:
```
rclone config
```
After configuring rclone, if you're on windows you should install win11toast using pip, like so:
```
pip install win11toast
```
Linux and MacOS users shouldn't need any other programs (i don't have a mac so i'm not 100% sure) besides python and rclone.<br>
After doing all this, simply run 
```
python "rclone-sync.py"
```
in order to start the program and begin monitoring files.
## Usage
### Adding a folder
You can add as much folders as you want by editing the file and adding a command for every folder under `# Syncjobs go here!`.<br>
The syntax is as such:
```python
mirror_files(string FOLDER_ID, string LOCAL_PATH, string REMOTE, string NAME)
```
* `FOLDER_ID`:
  The Google Drive ID of the folder, can be found in the url when opening the folder in your browser.
* `LOCAL_PATH`:
  The path to the folder on your server/pc, should be done using `os.path.join()`.
* `REMOTE`:
  Determines what rclone remote you want to use, should be "gdrive:" or an equivalent.
  It does not need to be a specific google drive setup as this script uses FOLDER_ID to find the folder.
* `NAME`:
  The name of whatever you're syncing, for notifications and `print()`.
  Can be anything, or it can even be empty if you're running the script headless.
#### Other values
There are some values i'm too lazy to move, of which the most notable one is:
* The time which the script should wait before running again, found at the variable declaration of "interrupted".
