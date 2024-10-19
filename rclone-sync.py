import os
import time
import platform
import threading
import subprocess

# Make sure the correct platform libraries are loaded
# ToastType = 0: Windows, 1: Linux, 2: MacOS (Darwin)
match platform.system():
    case "Windows":
        from win11toast import toast
        ToastType = 0
        print("Detected Windows as the current platform")
    case "Linux":
        ToastType = 1
        print("Detected Linux as the current platform")
    case "Darwin":
        ToastType = 2
        print("Detected MacOS as the current platform")

# Flag to control the waiting and interruption
interrupt_flag = threading.Event()

# Function to mirror files using rclone
def mirror_files(FOLDER_ID, LOCAL_PATH, REMOTE, NAME):
    # Ensure the local directory exists
    if not os.path.exists(LOCAL_PATH):
        os.makedirs(LOCAL_PATH)
    
    # Check for files (used for toast later)
    previous_files = set(os.listdir(LOCAL_PATH))
    
    print(f"Syncing Google Drive folder (ID: {FOLDER_ID}) to local path: {LOCAL_PATH}")
    
    # Execute the rclone sync command
    try:
        subprocess.run([
            "rclone", "sync", REMOTE, LOCAL_PATH,
            #"--dry-run", # uncomment to simulate sync (no files changed)
            "--progress",
            "--drive-root-folder-id", FOLDER_ID,
            "--ignore-existing"
        ], check=True)
        print("Sync completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during sync: {e}")
    
    # Check files after rclone has run
    current_files = set(os.listdir(LOCAL_PATH))
    new_files = current_files - previous_files
    if new_files:
            for new_file in new_files:
                # Show toast notification for each new file
                # Match toasttype to make sure the correct OS is used
                match ToastType:
                    case 0:                                
                        toast(
                            f"New episode detected for {NAME}",
                            f"'{new_file}' was added to {LOCAL_PATH}.",
                            )
                    case 1:
                        os.system('notify-send f"New episode detected for {NAME}" f"{new_file} was added to {LOCAL_PATH}."')
                    case 2: # I don't know if this will work, as i don't have a mac. Please make a github issue if it doesn't work
                        os.system(f'osascript -e display notification "New episode detected for {NAME}" with title "{new_file} was added to {LOCAL_PATH}."')

                print(f"New file detected: {new_file}")

# Function that runs the mirroring process repeatedly with interruptible sleep
def periodic_sync():
    while True:
        # Syncjobs go here!
        mirror_files("12345abcdefgh-hijklmnopqrstuvwxyz", os.path.join("C:", "Videos", "Shows", "Murder Drones"), "gdrive:", "Murder Drones") # Replace with your intended values
        
        print("Now sleeping until next sync (or press 'Enter' to run immediately)...")
        
        # Wait for 3600 seconds (1 hour) or until interrupted
        interrupted = interrupt_flag.wait(timeout=3600)
        
        if interrupted:
            print("Running sync before next scheduled time\n")
            interrupt_flag.clear()  # Reset the flag

# Function to handle pressing button to force sync
def interrupt_handler():
    while True:
        input("")
        interrupt_flag.set() 
        
# Create and start the sync thread
sync_thread = threading.Thread(target=periodic_sync)
sync_thread.daemon = True  # Daemonize the thread so it exits when the program ends
sync_thread.start()

# Run the interrupt handler in the main thread
interrupt_handler()
