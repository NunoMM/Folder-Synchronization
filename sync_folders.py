import os
import shutil
import hashlib
import time
import logging
from datetime import datetime
from collections import namedtuple
import argparse
import sys
import threading

SyncStats = namedtuple('SyncStats', [
    'changes_made', 'files_added', 'files_changed', 'files_removed', 'dirs_added', 'dirs_removed',
    'bytes_added', 'bytes_changed', 'bytes_removed'
])

exit_flag = threading.Event()  # Global flag to signal exit

def calculate_md5(file_path):
    """
    Calculate the MD5 checksum of a file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_folder_state(folder):
    """
    Get the state of a folder including all files and directories.
    """
    state = {'files': {}, 'dirs': set()}
    for root, dirs, files in os.walk(folder):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            rel_path = os.path.relpath(dir_path, folder)
            state['dirs'].add(rel_path)
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder)
            state['files'][rel_path] = (calculate_md5(file_path), os.path.getsize(file_path))
    return state

def safe_operation(logger, operation, *args, **kwargs):
    """
    Perform a file operation and log any errors that occur.
    """
    try:
        operation(*args, **kwargs)
        return True
    except Exception as e:
        logger.error(f"Failed to {operation.__name__}: {e}")
        return False

def update_stats(stats, stat_type, size=0):
    """
    Update synchronization statistics.
    """
    stats = stats._replace(changes_made=True, **{stat_type: getattr(stats, stat_type) + 1})
    if size:
        byte_stat = f"bytes_{stat_type.split('_')[1]}"
        stats = stats._replace(**{byte_stat: getattr(stats, byte_stat) + size})
    return stats

def sync_folders(source, replica, logger):
    """
    Synchronize files and directories between source and replica folders.
    """
    stats = SyncStats(False, 0, 0, 0, 0, 0, 0, 0, 0)
    current_source_state = get_folder_state(source)
    current_replica_state = get_folder_state(replica)
    changes = []

    # Create replica root if it doesn't exist
    if not os.path.exists(replica):
        safe_operation(logger, os.makedirs, replica)
        changes.append(f"Created replica directory '{replica}'.")
        stats = update_stats(stats, 'dirs_added')

    # Sync directories
    for dir_path in current_source_state['dirs']:
        replica_dir = os.path.join(replica, dir_path)
        if not os.path.exists(replica_dir):
            safe_operation(logger, os.makedirs, replica_dir)
            changes.append(f"Created directory '{replica_dir}'.")
            stats = update_stats(stats, 'dirs_added')

    # Sync files
    for rel_path, (curr_hash, curr_size) in current_source_state['files'].items():

        source_file = os.path.join(source, rel_path)
        replica_file = os.path.join(replica, rel_path)

        if rel_path not in current_replica_state['files']:
            # File doesn't exist in replica; copy it
            os.makedirs(os.path.dirname(replica_file), exist_ok=True)
            safe_operation(logger, shutil.copy2, source_file, replica_file)
            changes.append(f"Copied file '{source_file}' to '{replica_file}' ({curr_size} bytes).")
            stats = update_stats(stats, 'files_added', curr_size)
        else:
            # File exists in replica; check if it has changed
            rep_hash, rep_size = current_replica_state['files'][rel_path]
            if curr_hash != rep_hash:
                os.makedirs(os.path.dirname(replica_file), exist_ok=True)
                safe_operation(logger, shutil.copy2, source_file, replica_file)
                size_diff = curr_size - rep_size
                stats = update_stats(stats, 'files_changed', abs(size_diff))
                changes.append(f"Updated file '{replica_file}' with new content ({abs(size_diff)} bytes {'added' if size_diff > 0 else 'removed'}).")

    # Remove files from replica that no longer exist in source
    for rel_path, (_, size) in current_replica_state['files'].items():
        if rel_path not in current_source_state['files']:
            replica_file = os.path.join(replica, rel_path)
            safe_operation(logger, os.remove, replica_file)
            changes.append(f"Removed file '{replica_file}' ({size} bytes).")
            stats = update_stats(stats, 'files_removed', size)

    # Remove directories from replica that no longer exist in source
    for dir_path in sorted(current_replica_state['dirs'], key=len, reverse=True):
        if dir_path not in current_source_state['dirs']:
            replica_dir = os.path.join(replica, dir_path)
            safe_operation(logger, shutil.rmtree, replica_dir)
            changes.append(f"Removed directory '{replica_dir}'.")
            stats = update_stats(stats, 'dirs_removed')

    return stats, changes

def setup_logging(log_file):
    """
    Setup logging to both file and console.
    """
    logger = logging.getLogger('sync_logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def print_intro():
    """
    Print the introduction message for the folder synchronization script.
    """
    print("\n=============================")
    print("Folder Synchronization System")
    print("=============================")

def print_info_menu(source, replica, log_file, interval):
    """
    Print detailed help menu showing information about the synchronization.
    """
    print("\nInfo Menu:")
    print(f"  Source folder: {os.path.abspath(source)}")
    print(f"  Replica folder: {os.path.abspath(replica)}")
    print(f"  Log file path: {os.path.abspath(log_file)}")
    print(f"  Synchronization interval: {interval} seconds\n")

def print_command_menu():
    """
    Print command menu showing basic commands.
    """
    print("\nCommand Menu:")
    print("  '?' or 'help' - Show command menu")
    print("  'info' - Show info menu")
    print("  'exit' - Exit the program\n")

def command_listener():
    """
    Continuously listen for user commands.
    """
    while not exit_flag.is_set():
        user_command = input().strip().lower()
        if user_command in ['?', 'help']:
            print_command_menu()
        elif user_command == 'info':
            print_info_menu(args.source, args.replica, args.log_file, args.interval)
        elif user_command == 'exit':
            print("Exiting program...")
            exit_flag.set()  # Signal to exit the main loop
        else:
            print("Unknown command. Type '?' or 'help' for a list of commands.")

def main():
    global args
    parser = argparse.ArgumentParser(description='Folder synchronization script.')
    parser.add_argument('source', nargs='?', default='source', help='Source folder path')
    parser.add_argument('replica', nargs='?', default='replica', help='Replica folder path')
    parser.add_argument('log_file', nargs='?', default='sync_output.log', help='Log file path')
    parser.add_argument('interval', nargs='?', type=int, default=15, help='Synchronization interval in seconds')

    args = parser.parse_args()
    logger = setup_logging(args.log_file)

    print_intro()
    print_command_menu()

    # Start the command listener thread
    command_thread = threading.Thread(target=command_listener, daemon=True)
    command_thread.start()

    # Continuous synchronization
    while not exit_flag.is_set():
        start_time = time.time()
        stats, changes = sync_folders(args.source, args.replica, logger)
        end_time = time.time()

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{current_time}] -> Synchronizing folder '{os.path.basename(args.replica)}' with folder '{os.path.basename(args.source)}'..\n"

        if stats.changes_made:
            log_message += "Changes:\n"
            for change in changes:
                log_message += f"- {change}\n"
            log_message += (f"Summary: {stats.files_added} files added ({stats.bytes_added} bytes), "
                            f"{stats.files_changed} files changed ({stats.bytes_changed} bytes), "
                            f"{stats.files_removed} files removed ({stats.bytes_removed} bytes), "
                            f"{stats.dirs_added} directories added, "
                            f"{stats.dirs_removed} directories removed.\n")
        else:
            log_message += "No changes were made. Folders are synchronized.\n"

        log_message += f"Synchronization completed in {end_time - start_time:.2f} seconds.\n"
        logger.info(log_message)

        time.sleep(args.interval)

if __name__ == "__main__":
    main()
