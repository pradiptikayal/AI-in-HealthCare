"""
Data access utility functions for JSON-based storage.

This module provides thread-safe functions for reading and writing JSON files,
ID generation, and file locking for concurrent access safety.
"""

import json
import os
import uuid
import threading
from typing import Any, List, Dict, Optional
from contextlib import contextmanager


# Base directory for data files
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Thread lock for file access
_file_locks = {}
_locks_lock = threading.Lock()


def _get_file_lock(file_path: str) -> threading.Lock:
    """Get or create a lock for a specific file path."""
    with _locks_lock:
        if file_path not in _file_locks:
            _file_locks[file_path] = threading.Lock()
        return _file_locks[file_path]


@contextmanager
def file_lock(file_path: str, mode: str = 'r'):
    """
    Context manager for file locking to ensure thread-safe file access.
    Uses threading locks for cross-platform compatibility.
    
    Args:
        file_path: Path to the file to lock
        mode: File open mode ('r' for read, 'r+' for read/write)
    
    Yields:
        File object with exclusive lock
    """
    lock = _get_file_lock(file_path)
    lock.acquire()
    try:
        file_obj = open(file_path, mode)
        try:
            yield file_obj
        finally:
            file_obj.close()
    finally:
        lock.release()


def read_json_file(filename: str) -> List[Dict[str, Any]]:
    """
    Read data from a JSON file with file locking.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
    
    Returns:
        List of records from the JSON file
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    file_path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {filename}")
    
    with file_lock(file_path, 'r') as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def write_json_file(filename: str, data: List[Dict[str, Any]]) -> None:
    """
    Write data to a JSON file with file locking.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
        data: List of records to write to the file
    
    Raises:
        IOError: If the file cannot be written
    """
    file_path = os.path.join(DATA_DIR, filename)
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Use r+ mode to lock existing file, or create new file
    if os.path.exists(file_path):
        with file_lock(file_path, 'r+') as f:
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    else:
        # For new files, use write mode with lock
        lock = _get_file_lock(file_path)
        lock.acquire()
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        finally:
            lock.release()


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID using UUID4.
    
    Args:
        prefix: Optional prefix for the ID (e.g., 'patient', 'assessment')
    
    Returns:
        Unique ID string (UUID4 format with optional prefix)
    """
    unique_id = str(uuid.uuid4())
    return f"{prefix}_{unique_id}" if prefix else unique_id


def find_by_id(filename: str, id_field: str, id_value: str) -> Optional[Dict[str, Any]]:
    """
    Find a record by ID in a JSON file.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
        id_field: Name of the ID field (e.g., 'patientID')
        id_value: Value of the ID to search for
    
    Returns:
        Record dictionary if found, None otherwise
    """
    data = read_json_file(filename)
    for record in data:
        if record.get(id_field) == id_value:
            return record
    return None


def find_all_by_field(filename: str, field: str, value: Any) -> List[Dict[str, Any]]:
    """
    Find all records matching a field value in a JSON file.
    
    Args:
        filename: Name of the JSON file (e.g., 'assessments.json')
        field: Name of the field to match (e.g., 'patientID')
        value: Value to match
    
    Returns:
        List of matching records
    """
    data = read_json_file(filename)
    return [record for record in data if record.get(field) == value]


def add_record(filename: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new record to a JSON file.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
        record: Record dictionary to add
    
    Returns:
        The added record
    """
    data = read_json_file(filename)
    data.append(record)
    write_json_file(filename, data)
    return record


def update_record(filename: str, id_field: str, id_value: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update a record in a JSON file.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
        id_field: Name of the ID field (e.g., 'patientID')
        id_value: Value of the ID to update
        updates: Dictionary of fields to update
    
    Returns:
        Updated record if found, None otherwise
    """
    data = read_json_file(filename)
    for record in data:
        if record.get(id_field) == id_value:
            record.update(updates)
            write_json_file(filename, data)
            return record
    return None


def delete_record(filename: str, id_field: str, id_value: str) -> bool:
    """
    Delete a record from a JSON file.
    
    Args:
        filename: Name of the JSON file (e.g., 'patients.json')
        id_field: Name of the ID field (e.g., 'patientID')
        id_value: Value of the ID to delete
    
    Returns:
        True if record was deleted, False if not found
    """
    data = read_json_file(filename)
    original_length = len(data)
    data = [record for record in data if record.get(id_field) != id_value]
    
    if len(data) < original_length:
        write_json_file(filename, data)
        return True
    return False
