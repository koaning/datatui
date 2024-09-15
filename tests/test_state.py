import pytest
from datatui.app import State
from diskcache import Cache
from pathlib import Path
import tempfile

@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def sample_input_stream():
    return [
        {"content": "Example 1"},
        {"content": "Example 2"},
        {"content": "Example 3"}
    ]

def test_state_initialization(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    assert isinstance(state.cache, Cache)
    assert state._collection_name == "test_collection"
    assert state._input_stream == sample_input_stream
    assert state._input_size == 3
    assert state._content_key == "content"
    assert state._current_example is None
    assert not state._done
    assert state._position == 0

def test_mk_hash(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    example = {"content": "Test content"}
    hash_value = state.mk_hash(example)
    assert isinstance(hash_value, str)
    assert len(hash_value) == 32  # MD5 hash is 32 characters long

def test_write_annot(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    state._current_example = sample_input_stream[0]
    result = state.write_annot("test_label")
    assert result  # Should return True as there are more examples
    assert state._position == 1
    
    # Check if the annotation was written to cache
    cached_item = state.cache[state.mk_hash(sample_input_stream[0])]
    assert cached_item["label"] == "test_label"
    assert cached_item["collection"] == "test_collection"
    assert "timestamp" in cached_item

def test_stream(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    stream = list(state.stream())
    assert len(stream) == 3
    assert state._position == 3

def test_current_example(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    assert state.current_example == sample_input_stream[0]
    state.next_example()
    assert state.current_example == sample_input_stream[1]
    state.next_example()
    assert state.current_example == sample_input_stream[2]
    state.next_example()
    assert state.current_example == {"content": "No more examples."}
    assert state._done

def test_stream_size(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    assert state.stream_size == 3
