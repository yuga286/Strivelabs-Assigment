LocalDataStore
A simple Python-based data store that saves data in a JSON file with thread-safe and process-safe file access. This data store supports TTL (Time to Live) for entries, as well as file size and entry constraints.

Features
Concurrency: Uses file locking (fcntl) to ensure two processes cannot access the same file simultaneously.
Constraints: Enforces limits on key length, value size, and file size (1GB max).
TTL Support: Entries can expire after a specified time (TTL).
Batch Operations: Supports batch creation of entries (limit of 10 per batch).
Requirements
Python 3.x
OS-Specific: fcntl module for file locking, which is natively supported on Unix-based systems (Linux, macOS) but not on Windows.
Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd LocalDataStore
Ensure you have Python 3 installed:

bash
Copy code
python3 --version
Install any required Python packages (if not already installed):

bash
Copy code
pip install -r requirements.txt
(Currently, there are no external requirements for this code.)

Usage
Setting Up
The data store can be instantiated by providing a file path for the JSON storage:

python
Copy code
from data_store import LocalDataStore

# Initialize the store with a file path (default: 'data.json')
store = LocalDataStore(filepath='data.json')
Running Basic Operations
To interact with the data store, use the following methods:

Create an entry
python
Copy code
store.create("user1", {"name": "Alice", "age": 30}, ttl=10)
Read an entry
python
Copy code
value = store.read("user1")
print(value)
Delete an entry
python
Copy code
store.delete("user1")
Batch Create
python
Copy code
batch_entries = [
    {"key": "user4", "value": {"name": "Bob", "age": 25}},
    {"key": "user5", "value": {"name": "Charlie", "age": 35}, "ttl": 5}
]
store.batch_create(batch_entries)
Testing TTL Expiration
TTL is set in seconds. To test entry expiration, set a TTL and read the entry after the TTL expires:

python
Copy code
store.create("temp_key", {"temp_data": 123}, ttl=5)
time.sleep(6)
print(store.read("temp_key"))  # Should return "Key has expired."
Design Decisions
Concurrency: Implemented file locking using fcntl to prevent concurrent access by multiple processes. However, since fcntl is not available on Windows, this is currently only compatible with Unix-based systems.
TTL Check: The _is_expired method checks and removes expired entries when accessed, allowing entries to auto-expire without a scheduled job.
File Size Limit: Before each write, the file size is checked to prevent exceeding 1 GB.
Constraints: Key length is limited to 32 characters, and values cannot exceed 16 KB, making the data store more predictable and preventing excessive memory usage.
System Limitations
OS Compatibility: Due to the fcntl module, the code currently runs only on Unix-based systems (Linux, macOS). To use this on Windows, you may need to implement alternative file-locking mechanisms, such as msvcrt.
File Size Limit: The data store enforces a 1 GB file size limit. If this limit is reached, no additional data will be saved.
