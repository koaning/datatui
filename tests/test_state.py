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
    assert len(state) == 3
    assert state.position == 0
    assert state.current_example == {"content": "Example 1"}
    assert state.collection == "test_collection"
    assert not state.done()

def test_state_prev_next_example(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    assert state.position == 0
    assert state.next_example() == {"content": "Example 2"}
    assert state.current_example == {"content": "Example 2"}
    assert state.position == 1
    assert state.next_example() == {"content": "Example 3"}
    assert state.current_example == {"content": "Example 3"}
    assert state.position == 2
    assert state.next_example() == {"content": "No more examples. All done!"}
    assert state.position == 2
    assert state.done()
    assert state.prev_example() == {"content": "Example 2"}
    assert state.position == 1
    assert state.prev_example() == {"content": "Example 1"}
    assert state.position == 0
    assert state.prev_example() == {"content": "Example 1"}
    assert state.position == 0

def test_state_write_annot(temp_cache_dir, sample_input_stream):
    state = State(sample_input_stream, temp_cache_dir, "test_collection")
    state.write_annot("yes")
    assert state.position == 1
    cache = Cache(temp_cache_dir)
    stored_example = cache[state.mk_hash(sample_input_stream[0])]
    assert stored_example["label"] == "yes"
    assert stored_example["collection"] == "test_collection"
    assert "timestamp" in stored_example
