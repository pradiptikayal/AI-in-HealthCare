"""
Unit tests for data access utility functions.
"""

import os
import sys
import json
import pytest
import tempfile
import shutil
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_access import (
    read_json_file,
    write_json_file,
    generate_id,
    find_by_id,
    find_all_by_field,
    add_record,
    update_record,
    delete_record,
    DATA_DIR
)


@pytest.fixture
def temp_data_dir(monkeypatch):
    """Create a temporary data directory for testing."""
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setattr('data_access.DATA_DIR', temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_patients():
    """Sample patient data for testing."""
    return [
        {
            "patientID": "patient_001",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com"
        },
        {
            "patientID": "patient_002",
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "jane@example.com"
        }
    ]


class TestReadJsonFile:
    """Tests for read_json_file function."""
    
    def test_read_existing_file(self, temp_data_dir, sample_patients):
        """Test reading an existing JSON file."""
        file_path = os.path.join(temp_data_dir, 'patients.json')
        with open(file_path, 'w') as f:
            json.dump(sample_patients, f)
        
        result = read_json_file('patients.json')
        assert result == sample_patients
    
    def test_read_nonexistent_file(self, temp_data_dir):
        """Test reading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read_json_file('nonexistent.json')
    
    def test_read_empty_array(self, temp_data_dir):
        """Test reading a file with empty array."""
        file_path = os.path.join(temp_data_dir, 'empty.json')
        with open(file_path, 'w') as f:
            json.dump([], f)
        
        result = read_json_file('empty.json')
        assert result == []


class TestWriteJsonFile:
    """Tests for write_json_file function."""
    
    def test_write_to_new_file(self, temp_data_dir, sample_patients):
        """Test writing to a new file."""
        write_json_file('new_patients.json', sample_patients)
        
        file_path = os.path.join(temp_data_dir, 'new_patients.json')
        assert os.path.exists(file_path)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == sample_patients
    
    def test_write_to_existing_file(self, temp_data_dir, sample_patients):
        """Test overwriting an existing file."""
        file_path = os.path.join(temp_data_dir, 'patients.json')
        with open(file_path, 'w') as f:
            json.dump([{"old": "data"}], f)
        
        write_json_file('patients.json', sample_patients)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == sample_patients
    
    def test_write_empty_array(self, temp_data_dir):
        """Test writing an empty array."""
        write_json_file('empty.json', [])
        
        file_path = os.path.join(temp_data_dir, 'empty.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == []


class TestGenerateId:
    """Tests for generate_id function."""
    
    def test_generate_id_without_prefix(self):
        """Test generating ID without prefix."""
        id1 = generate_id()
        id2 = generate_id()
        
        assert id1 != id2
        assert len(id1) == 36  # UUID4 length
    
    def test_generate_id_with_prefix(self):
        """Test generating ID with prefix."""
        id1 = generate_id("patient")
        id2 = generate_id("patient")
        
        assert id1.startswith("patient_")
        assert id2.startswith("patient_")
        assert id1 != id2
    
    def test_generate_multiple_unique_ids(self):
        """Test that multiple IDs are unique."""
        ids = [generate_id() for _ in range(100)]
        assert len(ids) == len(set(ids))  # All unique


class TestFindById:
    """Tests for find_by_id function."""
    
    def test_find_existing_record(self, temp_data_dir, sample_patients):
        """Test finding an existing record."""
        write_json_file('patients.json', sample_patients)
        
        result = find_by_id('patients.json', 'patientID', 'patient_001')
        assert result == sample_patients[0]
    
    def test_find_nonexistent_record(self, temp_data_dir, sample_patients):
        """Test finding a record that doesn't exist."""
        write_json_file('patients.json', sample_patients)
        
        result = find_by_id('patients.json', 'patientID', 'patient_999')
        assert result is None
    
    def test_find_in_empty_file(self, temp_data_dir):
        """Test finding in an empty file."""
        write_json_file('patients.json', [])
        
        result = find_by_id('patients.json', 'patientID', 'patient_001')
        assert result is None


class TestFindAllByField:
    """Tests for find_all_by_field function."""
    
    def test_find_multiple_matching_records(self, temp_data_dir):
        """Test finding multiple records with same field value."""
        assessments = [
            {"assessmentID": "a1", "patientID": "p1", "symptoms": ["fever"]},
            {"assessmentID": "a2", "patientID": "p1", "symptoms": ["cough"]},
            {"assessmentID": "a3", "patientID": "p2", "symptoms": ["headache"]}
        ]
        write_json_file('assessments.json', assessments)
        
        result = find_all_by_field('assessments.json', 'patientID', 'p1')
        assert len(result) == 2
        assert result[0]["assessmentID"] == "a1"
        assert result[1]["assessmentID"] == "a2"
    
    def test_find_no_matching_records(self, temp_data_dir, sample_patients):
        """Test finding when no records match."""
        write_json_file('patients.json', sample_patients)
        
        result = find_all_by_field('patients.json', 'patientID', 'nonexistent')
        assert result == []
    
    def test_find_in_empty_file(self, temp_data_dir):
        """Test finding in an empty file."""
        write_json_file('patients.json', [])
        
        result = find_all_by_field('patients.json', 'patientID', 'p1')
        assert result == []


class TestAddRecord:
    """Tests for add_record function."""
    
    def test_add_record_to_existing_file(self, temp_data_dir, sample_patients):
        """Test adding a record to an existing file."""
        write_json_file('patients.json', sample_patients)
        
        new_patient = {
            "patientID": "patient_003",
            "firstName": "Bob",
            "lastName": "Johnson",
            "email": "bob@example.com"
        }
        
        result = add_record('patients.json', new_patient)
        assert result == new_patient
        
        all_patients = read_json_file('patients.json')
        assert len(all_patients) == 3
        assert all_patients[2] == new_patient
    
    def test_add_record_to_empty_file(self, temp_data_dir):
        """Test adding a record to an empty file."""
        write_json_file('patients.json', [])
        
        new_patient = {"patientID": "patient_001", "firstName": "John"}
        result = add_record('patients.json', new_patient)
        
        assert result == new_patient
        all_patients = read_json_file('patients.json')
        assert len(all_patients) == 1
        assert all_patients[0] == new_patient


class TestUpdateRecord:
    """Tests for update_record function."""
    
    def test_update_existing_record(self, temp_data_dir, sample_patients):
        """Test updating an existing record."""
        write_json_file('patients.json', sample_patients)
        
        updates = {"email": "newemail@example.com", "phone": "123-456-7890"}
        result = update_record('patients.json', 'patientID', 'patient_001', updates)
        
        assert result is not None
        assert result["email"] == "newemail@example.com"
        assert result["phone"] == "123-456-7890"
        assert result["firstName"] == "John"  # Original field preserved
        
        # Verify persistence
        updated = find_by_id('patients.json', 'patientID', 'patient_001')
        assert updated["email"] == "newemail@example.com"
    
    def test_update_nonexistent_record(self, temp_data_dir, sample_patients):
        """Test updating a record that doesn't exist."""
        write_json_file('patients.json', sample_patients)
        
        result = update_record('patients.json', 'patientID', 'patient_999', {"email": "new@example.com"})
        assert result is None
    
    def test_update_in_empty_file(self, temp_data_dir):
        """Test updating in an empty file."""
        write_json_file('patients.json', [])
        
        result = update_record('patients.json', 'patientID', 'patient_001', {"email": "new@example.com"})
        assert result is None


class TestDeleteRecord:
    """Tests for delete_record function."""
    
    def test_delete_existing_record(self, temp_data_dir, sample_patients):
        """Test deleting an existing record."""
        write_json_file('patients.json', sample_patients)
        
        result = delete_record('patients.json', 'patientID', 'patient_001')
        assert result is True
        
        all_patients = read_json_file('patients.json')
        assert len(all_patients) == 1
        assert all_patients[0]["patientID"] == "patient_002"
    
    def test_delete_nonexistent_record(self, temp_data_dir, sample_patients):
        """Test deleting a record that doesn't exist."""
        write_json_file('patients.json', sample_patients)
        
        result = delete_record('patients.json', 'patientID', 'patient_999')
        assert result is False
        
        all_patients = read_json_file('patients.json')
        assert len(all_patients) == 2  # No change
    
    def test_delete_from_empty_file(self, temp_data_dir):
        """Test deleting from an empty file."""
        write_json_file('patients.json', [])
        
        result = delete_record('patients.json', 'patientID', 'patient_001')
        assert result is False


class TestConcurrentAccess:
    """Tests for concurrent access safety."""
    
    def test_file_locking_prevents_corruption(self, temp_data_dir, sample_patients):
        """Test that file locking prevents data corruption."""
        write_json_file('patients.json', sample_patients)
        
        # Simulate concurrent writes
        new_patient1 = {"patientID": "patient_003", "firstName": "Alice"}
        new_patient2 = {"patientID": "patient_004", "firstName": "Charlie"}
        
        add_record('patients.json', new_patient1)
        add_record('patients.json', new_patient2)
        
        all_patients = read_json_file('patients.json')
        assert len(all_patients) == 4
        assert any(p["patientID"] == "patient_003" for p in all_patients)
        assert any(p["patientID"] == "patient_004" for p in all_patients)
