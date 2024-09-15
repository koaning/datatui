import pytest
from datatui import new_batch
from pathlib import Path
import tempfile
import json

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "content": "Example 1"},
        {"id": 2, "content": "Example 2"},
        {"id": 3, "content": "Example 3"},
        {"id": 4, "content": "Example 4"},
        {"id": 5, "content": "Example 5"}
    ]

@pytest.fixture
def temp_jsonl_file(sample_data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as tmp:
        for item in sample_data:
            json.dump(item, tmp)
            tmp.write('\n')
    yield Path(tmp.name)
    Path(tmp.name).unlink()

@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_new_batch_from_jsonl(temp_jsonl_file, temp_cache_dir):
    result = new_batch(temp_jsonl_file, temp_cache_dir, "test_collection")
    assert len(result) == 5
    assert all(isinstance(item, dict) for item in result)

def test_new_batch_from_iterable(sample_data, temp_cache_dir):
    result = new_batch(sample_data, temp_cache_dir, "test_collection")
    assert len(result) == 5
    assert all(isinstance(item, dict) for item in result)
