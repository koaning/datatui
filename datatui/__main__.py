import json
import srsly
import typer
from rich.console import Console
from rich.table import Table
from diskcache import Cache
from .app import datatui


app = typer.Typer(no_args_is_help=True)

@app.command()
def annotate(
    examples_path: str,
    cache: str = typer.Option("annotations", help='Cache path'),
    collection: str = typer.Option("default", help='Attach a collection name to each annotation'),
    render_key: str = typer.Option("text", help='What key of the content to render'),
    descr: str = typer.Option(None, help='Add a description')
):
    """Annotate and put some examples into the cache."""
    examples = list(srsly.read_jsonl(examples_path))
    app = datatui(examples, cache_name=cache, collection_name=collection, pbar=True, description=descr, content_render=lambda x: x[render_key])
    app.run()


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
            print(json.dumps(item))  # noqa
    else:
        srsly.write_jsonl(file_out, relevant)


@app.command()
def count(
    cache: str = typer.Option("annotations", help='Cache path'),
):
    """Count and pretty print the number of annotations per collection."""
    cache = Cache(cache)
    collections = {}
    for key in cache.iterkeys():
        item = cache[key]
        collection = item.get('collection', 'default')
        collections[collection] = collections.get(collection, 0) + 1
    
    if not collections:
        print("No annotations found.")
        return
    
    console = Console()
    table = Table(title="Annotations per collection")
    table.add_column("Collection", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta", justify="right")

    for collection, count in sorted(collections.items()):
        table.add_row(collection, str(count))

    table.add_section()
    total = sum(collections.values())
    table.add_row("Total", str(total), style="bold")

    console.print(table)




if __name__ == "__main__":
    app()


__all__ = ["annotate", "export"]
