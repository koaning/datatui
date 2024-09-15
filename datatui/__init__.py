from .app import datatui, mk_hash

import srsly
from diskcache import Cache
from typing import List, Dict, Union, Iterable
from pathlib import Path
from itertools import islice


def new_batch(
    input_data: Union[str, Path, Iterable[Dict]],
    cache_path: str,
    collection: str,
    limit: int = 150
) -> List[Dict]:
    """
    Read examples from a JSONL file or an iterable of dictionaries and return only those not present in the cache.

    Args:
        input_data (Union[str, Path, Iterable[Dict]]): Path to a JSONL file (as string or Path object) or an iterable of dictionaries containing examples.
        cache_path (str): Path to the cache directory.
        collection (str): Name of the collection for these examples.
        limit (int, optional): Maximum number of uncached examples to return. If None, return all uncached examples.

    Returns:
        List[Dict]: A list of examples that are not present in the cache, up to the specified limit.
    """
    cache = Cache(cache_path)

    if isinstance(input_data, (str, Path)):
        examples = srsly.read_jsonl(input_data)
    else:
        examples = input_data

    def uncached_examples_generator():
        for example in examples:
            # Create a unique hash for the example
            example_hash = mk_hash(example, collection)
            if example_hash not in cache:
                yield example

    limited_examples = islice(uncached_examples_generator(), limit)

    return list(limited_examples)

__all__ = ["datatui"]
