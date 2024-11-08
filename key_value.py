import json
import os
import time
import fcntl

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB in bytes

class LocalDataStore:
    def __init__(self, filepath='data.json'):
        self.filepath = filepath or os.path.join(os.getcwd(), 'data_store.json')
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                # Lock the file exclusively before reading
                fcntl.flock(file, fcntl.LOCK_EX)
                try:
                    return json.load(file)
                finally:
                    # Release the lock after reading
                    fcntl.flock(file, fcntl.LOCK_UN)
        return {}

    def save_data(self):
        # Ensure the file size limit is not exceeded
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) >= MAX_FILE_SIZE:
            raise Exception("File size limit of 1GB reached. Cannot save more data.")
        
        with open(self.filepath, 'w') as file:
            # Lock the file exclusively before writing
            fcntl.flock(file, fcntl.LOCK_EX)
            try:
                json.dump(self.data, file, indent=4)
            finally:
                # Release the lock after writing
                fcntl.flock(file, fcntl.LOCK_UN)

    def _check_key_constraints(self, key):
        if len(key) > 32:
            raise KeyError("Key length must not exceed 32 characters.")

    def _check_value_constraints(self, value):
        if len(json.dumps(value)) > 16 * 1024: 
            raise ValueError("Value size must not exceed 16KB.")

    def _is_expired(self, key):
        ttl = self.data[key].get("ttl")
        if ttl and time.time() > ttl:
            del self.data[key]
            self.save_data()
            return True
        return False

    def is_key_expired(self, key):
        ttl = self.data.get(key, {}).get("ttl")
        return ttl and time.time() > ttl

    def create(self, key, value, ttl=None):
        self._check_key_constraints(key)
        self._check_value_constraints(value)
        if key in self.data and not self._is_expired(key):
            raise KeyError("Key already exists.")
        
        self.data[key] = {
            "value": value,
            "ttl": time.time() + ttl if ttl else None
        }
        self.save_data()

    def read(self, key):
        if key not in self.data:
            return "Key does not exist."
        
        if self.is_key_expired(key):
            return "Key has expired."
        
        return self.data[key]["value"]

    def delete(self, key):
        if key not in self.data or self._is_expired(key):
            raise KeyError("Key does not exist or has expired.")
        del self.data[key]
        self.save_data()

    def batch_create(self, entries):
        if len(entries) > 10:
            raise ValueError("Batch size limit exceeded. Max 10 entries allowed.")
        
        for entry in entries:
            key, value, ttl = entry.get("key"), entry.get("value"), entry.get("ttl", None)
            try:
                self.create(key, value, ttl)
            except (ValueError, KeyError) as e:
                print(f"Error adding key '{key}': {e}")


store = LocalDataStore(filepath='data.json')

try:
    store.create("user1", {"name": "Alice", "age": 30}, ttl=10) 
    print("User1:", store.read("user1"))
except Exception as e:
    print(e)

batch_entries = [
    {"key": "user4", "value": {"name": "Bob", "age": 25}},
    {"key": "user5", "value": {"name": "Charlie", "age": 35}, "ttl": 5}
]

try:
    store.batch_create(batch_entries)
except Exception as e:
    print(e)

try:
    print("User3 (after TTL expiration):", store.read("user3"))
except KeyError as e:
    print(e)

try:
    store.delete("user1")
except KeyError as e:
    print(e)
