import pytest
from datatui.app import State, mk_hash
from diskcache import Cache
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
    # Test that the state is initialized correctly
    assert len(state) == 3
    assert state.position == 0
    assert state.current_example == {"content": "Example 1"}
    assert state.collection == "test_collection"
    assert not state.done()
    # Test that the next_example method works correctly
    assert state.next_example() == {"content": "Example 2"}
    assert state.current_example == {"content": "Example 2"}
    assert state.position == 1
    assert state.next_example() == {"content": "Example 3"}
    assert state.current_example == {"content": "Example 3"}
    assert state.position == 2
    assert state.next_example() == {"content": "No more examples. All done!"}
    assert state.position == 3
    assert state.done()
    # This should not move the position
    assert state.next_example() == {"content": "No more examples. All done!"}
    assert state.position == 3
    assert state.done()
    # Test that the prev_example method works correctly
    assert state.prev_example() == {"content": "Example 3"}
    assert state.position == 2
    assert state.prev_example() == {"content": "Example 2"}
    assert state.position == 1
    assert state.prev_example() == {"content": "Example 1"}
    assert state.position == 0
    # This should not move the position
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

def test_mk_hash_function():
    # Test that the order of keys doesn't affect the hash
    example1 = {"content": "Test content", "other_key": "value"}
    example2 = {"other_key": "value", "content": "Test content"}
    collection = "test_collection"
    
    assert mk_hash(example1, collection) == mk_hash(example2, collection)

    # Test that different collections produce different hashes
    collection1 = "collection1"
    collection2 = "collection2"
    example = {"content": "Same content"}
    
    assert mk_hash(example, collection1) != mk_hash(example, collection2)

    # Test that different content produces different hashes
    example1 = {"content": "Content 1"}
    example2 = {"content": "Content 2"}
    collection = "same_collection"
    
    assert mk_hash(example1, collection) != mk_hash(example2, collection)
