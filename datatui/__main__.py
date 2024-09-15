import json
import srsly
import typer
from diskcache import Cache
from .app import datatui


app = typer.Typer(no_args_is_help=True)

@app.command()
def annotate(
    examples_path: str,
    cache: str = typer.Option("annotations", help='Cache path'),
    collection: str = typer.Option("default", help='Attach a collection name to each annotation'),
    descr: str = typer.Option(None, help='Add a description')
):
    """Annotate and put some examples into the cache."""
    examples = list(srsly.read_jsonl(examples_path))
    datatui(cache, examples, collection, pbar=True, description=descr)

@app.command()
def export(
    cache: str = typer.Option("annotations", help='Cache path'),
    collection: str = typer.Option(None, help='Subset a collection'),
    file_out: str = typer.Option(None, help='Output file path')
):
    """Export annotations from the cache."""
    cache = Cache(cache)
    relevant = (cache[k] for k in cache.iterkeys() 
                if collection is None or collection == cache[k]['collection'])
    if not file_out:
        for item in relevant:
            print(json.dumps(item))
    else:
        srsly.write_jsonl(file_out, relevant)

if __name__ == "__main__":
    app()

__all__ = ["annotate", "export"]
