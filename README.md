### 📁 Folder Synchronization System

---

### 📖 Overview

This is a Python-based folder synchronization tool that ensures two directories, a **source** folder and a **replica** folder, remain synchronized. 
The **replica** folder is updated to mirror the **source** folder, meaning any new, modified, or deleted files in the **source** folder will be reflected in the **replica** folder.
The program is designed to run periodically, checking for changes and updating the **replica** folder automatically. 
It's useful for backup purposes, ensuring that a folder is mirrored at all times.

---

### ✨ Features

- **One-way synchronization**: Changes made in the **source** folder are propagated to the **replica** folder, but not the other way around.
- **MD5 hashing**: The tool compares files using MD5 hash functions to determine if files in the **source** have been modified before copying them over to the **replica**. This ensures more accurate synchronization by avoiding redundant copying.
- **File operations**: 
  - New files in the **source** are copied to the **replica**.
  - Modified files in the **source** are updated in the **replica**.
  - Deleted files in the **source** are removed from the **replica**.
- **Log file**: All synchronization operations are logged, including timestamps and a summary of actions taken.
- **Automated synchronization**: The synchronization can run at a defined interval, allowing for regular updates without manual intervention.

---

### 🛠️ Requirements

- **Python 3.x** installed
- Required Python libraries:
  - `os`
  - `shutil`
  - `time`
  - `logging`
  - `hashlib`

---

### 🚀 Usage

You can execute the program from the **command line** by specifying the **source** folder, **replica** folder, **log output** file, and synchronization **interval**. 
The program will automatically synchronize the folders at the specified interval and log the details of each operation.

### Command Line Usage

```
python sync_folders.py <source_folder> <replica_folder> <log_output_file> <sync_interval>
```

The program can also be directly executed through python, where it will use the default folders and files (contained in the project folder) and values, like synchronization interval, defined in the code.

### Built-in Menu

Once the program is running, you can acess a built-in by inputting `?` or `help`. In this menu where you can:

  - **View** the source and replica folder paths, and interval timer by inputting `info`.
  - **Exit** the program, stopping the execution, by inputting `exit`.

---

### 🧪 Tests

During development, the folder synchronization tool was thoroughly tested to ensure its functionality. Below are the steps performed and the results from the tests:

### Test Setup

- **Source folder**: Contains files that will be mirrored to the **replica** folder.
  - Initial content: 
    - `file1`
    - `file2`
    - `folder1/`
      - `file_in_folder`
  
- **Replica folder**: Initially empty.

### Test Scenarios and Results

1. **Initial Synchronization**:
    - The **source folder** contents are copied to the **replica folder**.
    - **Expected result**: The **replica** folder mirrors the **source** folder exactly.

    **Test result**:
    - `folder1` → Created directory 'replica\folder1'.
    - `file1` → Copied file 'source\file1' to 'replica\file1'.
    - `file2` → Copied file 'source\file2' to 'replica\file2'.
    - `folder1/file_in_folder` → 'source\folder1\file_in_folder' to 'replica\folder1\file_in_folder'.
    
    **Replica folder** after initial sync:
    ```
    replica/
    ├── file1
    ├── file2
    └── folder1/
        └── file_in_folder
    ```

2. **Modification of a File** in the **Source** Folder:
    - `file1` was modified in the **source folder**.
    - **Expected result**: The modified `file1` is updated in the **replica folder**.

    **Test result**:
    - `file1` → Updated file 'replica\file1' with new content.
    
    **Replica folder** after modification sync:
    ```
    replica/
    ├── file1 (modified)
    ├── file2
    └── folder1/
        └── file_in_folder
    ```

3. **Addition of a New File** in the **Source** Folder:
    - A new file `file3` was added to the **source folder**.
    - **Expected result**: `file3` is copied to the **replica folder**.

    **Test result**:
    - `file3` → Copied file 'source\file3' to 'replica\file3'.
    
    **Replica folder** after file addition:
    ```
    replica/
    ├── file1 (modified)
    ├── file2
    ├── file3 (new)
    └── folder1/
        └── file_in_folder
    ```

4. **Deletion of a File** in the **Source** Folder:
    - `file3` was deleted from the **source folder**.
    - **Expected result**: `file3` is removed from the **replica folder**.

    **Test result**:
    - `file3` → Removed file 'replica\file3'.
    
    **Replica folder** after file deletion:
    ```
    replica/
    ├── file1 (modified)
    ├── file2
    └── folder1/
        └── file_in_folder
    ```

5. **Deletion of a File** and **Modification of a File** in the **Replica** Folder:
    - `file2` was deleted from the **replica folder**.
    - `file_in_folder` was modified in the **replica folder**.
    - **Expected result**: `file2` is copied to the **replica folder** and the modified `file_in_folder` is updated in the **replica folder**.

    **Test result**:
    - `file3` → Copied file 'source\file2' to 'replica\file2'.
    - `file_in_folder` → Updated file 'replica\file_in_folder' with new content.
    
    **Replica folder** after file deletion and modification sync:
    ```
    replica/
    ├── file1 (modified)
    ├── file2 (new)
    └── folder1/
        └── file_in_folder (updated)
    ```

### Synchronization Interval Testing

- A synchronization interval of **25 seconds** was tested to ensure that regular syncs were performed without issues, and to be able to do changes while the script is running in order to test all functionalities.
- **Result**: The system successfully performed synchronization every 25 seconds, logging actions correctly.

### Logging

The `sync_output.log` file contains detailed information about each synchronization operation. It logs actions such as file copies, modifications, deletions, and any errors that occur during the synchronization process.

### Example log entries from the test performed:

```
[2024-08-16 16:12:57] -> Synchronizing folder 'replica' with folder 'source'..
Changes:
- Created directory 'replica\folder1'.
- Copied file 'source\file1' to 'replica\file1' (66 bytes).
- Copied file 'source\file2' to 'replica\file2' (72 bytes).
- Copied file 'source\folder1\file_in_folder' to 'replica\folder1\file_in_folder' (113 bytes).
Summary: 3 files added (251 bytes), 0 files changed (0 bytes), 0 files removed (0 bytes), 1 directories added, 0 directories removed.
Synchronization completed in 0.00 seconds.

[2024-08-16 16:13:22] -> Synchronizing folder 'replica' with folder 'source'..
Changes:
- Updated file 'replica\file1' with new content (35 bytes added).
Summary: 0 files added (0 bytes), 1 files changed (35 bytes), 0 files removed (0 bytes), 0 directories added, 0 directories removed.
Synchronization completed in 0.00 seconds.

[2024-08-16 16:13:47] -> Synchronizing folder 'replica' with folder 'source'..
Changes:
- Copied file 'source\file3' to 'replica\file3' (76 bytes).
Summary: 1 files added (76 bytes), 0 files changed (0 bytes), 0 files removed (0 bytes), 0 directories added, 0 directories removed.
Synchronization completed in 0.01 seconds.

[2024-08-16 16:14:12] -> Synchronizing folder 'replica' with folder 'source'..
Changes:
- Removed file 'replica\file3' (76 bytes).
Summary: 0 files added (0 bytes), 0 files changed (0 bytes), 1 files removed (76 bytes), 0 directories added, 0 directories removed.
Synchronization completed in 0.00 seconds.

[2024-08-16 16:14:37] -> Synchronizing folder 'replica' with folder 'source'..
Changes:
- Copied file 'source\file2' to 'replica\file2' (72 bytes).
- Updated file 'replica\folder1\file_in_folder' with new content (37 bytes removed).
Summary: 1 files added (72 bytes), 1 files changed (37 bytes), 0 files removed (0 bytes), 0 directories added, 0 directories removed.
Synchronization completed in 0.00 seconds.
```

