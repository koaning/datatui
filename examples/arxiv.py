from rich.panel import Panel
import json 
from datatui import datatui, new_batch


# Read JSONL file 
def generator():
    with open("examples/arxiv.jsonl", "r") as f:
        for line in f:
            yield json.loads(line)

# Create a new batch, removes duplicates
batch = new_batch(generator(), cache_name="annotations", collection_name="default", limit=100)

# Run a new annotation session. Notice how we customise the content_render
# function to use rich Panels and that we add a description/progress bar to 
# the annotation task.
app = datatui(list(generator()), 
        cache_name="annotations", 
        collection_name="default",
        pbar=True, 
        description="Does this sentence suggest the article is about a [bold]new dataset[/bold]?.",
        content_render=lambda x: Panel(x["text"])
)

if __name__ == "__main__":
    app.run()
