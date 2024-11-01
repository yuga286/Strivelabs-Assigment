Here's a README file that explains the setup, usage, and design of the local file-based data store, as well as notes on dependencies and limitations.

---

# Local File-Based Data Store

This project provides a simple, file-based key-value store that operates locally on a single machine. The data store supports basic Create, Read, and Delete operations with optional Time-to-Live (TTL) for each entry, as well as batch Create operations. This solution is cross-platform compatible and can be used on Windows, Linux, and macOS.

## Setup and Run Instructions

1. **Install Python 3**: Ensure you have Python 3 installed. You can check this by running:
   ```bash
   python3 --version
   ```
   
2. **Clone the repository**: If this code is in a repository, clone it using:
   ```bash
   git clone <repository_url>
   ```

3. **Run the script**: Execute the data store operations by running:
   ```bash
   python3 data_store.py
   ```

### Dependencies

- **Python 3.x**: No external libraries are required as it uses the standard Python library (`json`, `os`, and `time` modules).

## Usage and Design Decisions

### Initialization

The data store initializes with an optional file path parameter. If no path is provided, it defaults to a file named `data_store.json` in the current working directory. If the file already exists, the store will load the existing data from it.

Example:
```python
store = LocalDataStore(filepath='data.json')
```

### Operations

1. **Create**: Adds a key-value pair to the store with an optional TTL.
   - Constraints: Key (max 32 characters), Value (max 16KB).
   - If a key already exists and has not expired, an error is returned.

2. **Read**: Retrieves the value of a specified key if it exists and has not expired.

3. **Delete**: Removes a specified key from the store if it exists and has not expired.

4. **Batch Create**: Adds multiple key-value pairs at once with a limit of 10 entries per batch to balance memory use and performance.

### Example Usage

```python
# Initialize the data store
store = LocalDataStore(filepath='data.json')

# Create a new key-value pair with TTL
store.create("user1", {"name": "Alice", "age": 30}, ttl=10) 

# Read the value for a key
print(store.read("user1"))

# Batch create multiple entries
batch_entries = [
    {"key": "user4", "value": {"name": "Bob", "age": 25}},
    {"key": "user5", "value": {"name": "Charlie", "age": 35}, "ttl": 5}
]
store.batch_create(batch_entries)

# Delete a key
store.delete("user1")
```

### Exception Handling

Errors are raised with appropriate messages:
- Key size or value size limit exceeded
- Duplicate key
- Non-existent or expired key

### Design Notes

- **TTL Implementation**: Each key supports a TTL, stored as an expiration timestamp. The key becomes inaccessible once the TTL has passed.
- **Batch Create Limit**: A batch size of 10 was chosen to prevent memory overload, making batch operations efficient without risking performance degradation.

### Limitations and Constraints

- **Single Device**: This data store is designed for local, single-process use and is not suitable for concurrent access.
- **Cross-Platform Compatibility**: The code should work on major OSes (Windows, Linux, macOS) since it uses standard Python libraries.
- **TTL Expiration**: Expired keys are only removed when accessed. This means expired keys may remain in the store until they are accessed again, at which point they will be removed.

# Strivelabs-Assigment
