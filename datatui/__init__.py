from .app import datatui, mk_hash

import srsly
from diskcache import Cache
from typing import List, Dict, Union, Iterable
from pathlib import Path
from itertools import islice


def new_batch(
    input_data: Union[str, Path, Iterable[Dict]],
    cache_name: str,
    collection_name: str,
    limit: int = 150
) -> List[Dict]:
    """
    Read examples from a JSONL file or an iterable of dictionaries and return only those not present in the cache.

    Args:
        input_data (Union[str, Path, Iterable[Dict]]): Path to a JSONL file (as string or Path object) or an iterable of dictionaries containing examples.
        cache_name (str): Path to the cache directory.
        collection_name (str): Name of the collection for these examples.
        limit (int, optional): Maximum number of uncached examples to return. If None, return all uncached examples.

    Returns:
        List[Dict]: A list of examples that are not present in the cache, up to the specified limit.
    """
    cache = Cache(cache_name)

    if isinstance(input_data, (str, Path)):
        examples = srsly.read_jsonl(input_data)
    else:
        examples = input_data

    def uncached_examples_generator():
        for example in examples:
            # Create a unique hash for the example
            example_hash = mk_hash(example, collection_name)
            if example_hash not in cache:
                yield example

    limited_examples = islice(uncached_examples_generator(), limit)

    return list(limited_examples)


def add_entity_highlighting(examples: Iterable[Dict]) -> Iterable[Dict]:
    """
    Add content key with background highlighting for entities to a stream of dictionaries.

    Args:
        examples (Iterable[Dict]): An iterable of dictionaries, each containing 'text' and 'entity' keys.

    Yields:
        Dict: A dictionary with the original keys and an additional 'content' key containing highlighted text.
    """
    for example in examples:
        text = example['text']
        entities = sorted(example['entity'], key=lambda e: e['start'])
        
        content = []
        last_end = 0
        
        for entity in entities:
            start, end = entity['start'], entity['end']
            
            # Add non-entity text
            if start > last_end:
                content.append(text[last_end:start])
            
            # Add highlighted entity text
            content.append("[black on yellow] " + text[start:end] + f"[bold] {entity['label']}[/] [/]")
            
            last_end = end
        
        # Add any remaining non-entity text
        if last_end < len(text):
            content.append(text[last_end:])
        
        example['content'] = " ".join(content)
        yield example


__all__ = ["datatui", "new_batch", "add_entity_highlighting"]
