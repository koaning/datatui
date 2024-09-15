import json 
from datatui import datatui


# Read JSONL file 
def generator():
    with open("examples/arxiv.jsonl", "r") as f:
        for line in f:
            example = json.loads(line)
            example["content"] = example["text"]
            yield example

if __name__ == "__main__":
    datatui("annotations", list(generator()), "default", pbar=True, description="Does this sentence suggest the article is about a [bold]new dataset[/bold]?.")
