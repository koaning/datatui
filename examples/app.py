import json 
from datatui import datatui, new_batch


# Read JSONL file 
def generator():
    with open("examples/arxiv.jsonl", "r") as f:
        for line in f:
            example = json.loads(line)
            yield example

batch = new_batch(generator(), cache_name="annotations", collection_name="default", limit=100)

if __name__ == "__main__":
    datatui(list(generator()), 
            cache_name="annotations", 
            collection_name="default",
            pbar=True, 
            description="Does this sentence suggest the article is about a [bold]new dataset[/bold]?.",
            content_render=lambda x: x["text"]
    )
