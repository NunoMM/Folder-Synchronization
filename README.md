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

---

### 🧪 Tests

During development, the folder synchronization tool was thoroughly tested to ensure its functionality. Below are the steps performed and the results from the tests:

### Test Setup

- **Source folder**: Contains files that will be mirrored to the **replica** folder.
  - Initial content: 
    - `file1.txt`
    - `file2.txt`
    - `folder1/`
      - `file_in_folder.txt`
  
- **Replica folder**: Initially empty.

### Test Scenarios and Results

1. **Initial Synchronization**:
    - The **source folder** contents are copied to the **replica folder**.
    - **Expected result**: The **replica** folder mirrors the **source** folder exactly.

    **Test result**:
    - `file1.txt` → Copied to replica.
    - `file2.txt` → Copied to replica.
    - `folder1/file_in_folder.txt` → Copied to replica.
    
    **Replica folder** after initial sync:
    ```
    replica/
    ├── file1.txt
    ├── file2.txt
    └── folder1/
        └── file_in_folder.txt
    ```

2. **Modification of a File** in the **Source** Folder:
    - `file1.txt` was modified in the **source folder**.
    - **Expected result**: The modified `file1.txt` is updated in the **replica folder**.

    **Test result**:
    - `file1.txt` → Updated in replica.
    
    **Replica folder** after modification sync:
    ```
    replica/
    ├── file1.txt (modified)
    ├── file2.txt
    └── folder1/
        └── file_in_folder.txt
    ```

3. **Addition of a New File** in the **Source** Folder:
    - A new file `file3.txt` was added to the **source folder**.
    - **Expected result**: `file3.txt` is copied to the **replica folder**.

    **Test result**:
    - `file3.txt` → Copied to replica.
    
    **Replica folder** after file addition:
    ```
    replica/
    ├── file1.txt (modified)
    ├── file2.txt
    ├── file3.txt (new)
    └── folder1/
        └── file_in_folder.txt
    ```

4. **Deletion of a File** in the **Source** Folder:
    - `file2.txt` was deleted from the **source folder**.
    - **Expected result**: `file2.txt` is removed from the **replica folder**.

    **Test result**:
    - `file2.txt` → Deleted from replica.
    
    **Replica folder** after file deletion:
    ```
    replica/
    ├── file1.txt (modified)
    ├── file3.txt (new)
    └── folder1/
        └── file_in_folder.txt
    ```

### Synchronization Interval Testing

- A synchronization interval of **30 seconds** was tested to ensure that regular syncs were performed without issues.
- **Result**: The system successfully performed synchronization every 30 seconds, logging actions correctly.

### Logging

- All operations (file copies, modifications, and deletions) were properly logged into the designated log file.
- Example log entry:

