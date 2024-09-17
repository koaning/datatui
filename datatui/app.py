import orjson
from collections import OrderedDict
from pathlib import Path 
from time import time
from typing import Dict
from diskcache import Cache 
from hashlib import md5
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static, ProgressBar
from textual.containers import Container, Center


def mk_hash(ex: Dict, collection: str) -> str:
    sorted_ex = OrderedDict(sorted(ex.items()))
    string_repr = orjson.dumps(sorted_ex).decode('utf-8') + collection
    return md5(string_repr.encode()).hexdigest()


class State:
    def __init__(self, examples, cache:str, collection:str) -> None:
        self.cache = Cache(cache)
        self.collection = collection
        self.examples = examples
        self._position = 0
        self._current_example = None
        self._content_key = "content"
        for i, ex in enumerate(examples):
            if self.mk_hash(ex) not in self.cache:
                self._position = i
                break
        else:
            self._position = len(examples) - 1
    
    @property
    def position(self):
        return self._position
    
    def mk_hash(self, ex):
        return mk_hash(ex, self.collection)

    def write_annot(self, label):
        if self.current_example:
            self.cache[self.mk_hash(self.current_example)] = {
                **self.current_example, 
                'label': label,
                'collection': self.collection,
                'timestamp': int(time())
            }
            return self.next_example()
    
    def __len__(self):
        return len(self.examples)
    
    @property
    def current_example(self):
        if self._position == len(self.examples):
            return {"content": "No more examples. All done!"}
        return self.examples[self._position]
    
    def next_example(self):
        if self._position == len(self.examples):
            return self.current_example
        self._position += 1
        return self.current_example

    def prev_example(self):
        if self._position == 0:
            return self.current_example
        self._position -= 1
        return self.current_example

    def done(self):
        return self._position == len(self.examples)

def datatui(input_stream: list, collection_name: str, cache_name: str = "annotations", pbar: bool = True, description=None, content_render=lambda x: x['content']):
    """
    Main function to run the datatui application.

    Args:
        input_stream (list): A list of examples to annotate.
        collection_name (str): The name of the collection for these examples.
        cache_name (str): The name or path of the cache to use for storing annotations.
        pbar (bool, optional): Whether to display a progress bar. Defaults to True.
        description (str, optional): A description to display above each example. Defaults to None.

    This function initializes and runs the DatatuiApp, which provides a text-based user interface
    for annotating examples. It uses the provided cache to store annotations and allows users
    to navigate through examples, annotating them as 'yes', 'no', 'maybe', or skipping them.
    """
    if len(input_stream) == 0:
        print("No examples to annotate. Exiting.")
        return
    class DatatuiApp(App):
        ACTIVE_EFFECT_DURATION = 0.3
        CSS_PATH = Path(__file__).parent / "static" / "app.css"
        BINDINGS = [
            Binding(key="f", action="on_annot('yes')", description="Annotate yes."),
            Binding(key="j", action="on_annot('no')", description="Annotate no."),
            Binding(key="m", action="on_annot('maybe')", description="Annotate maybe."),
            Binding(key="space", action="on_annot('skip')", description="Skip the thing."),
            Binding(key="backspace", action="on_annot('back')", description="Previous example."),
        ]
        state = State(input_stream, cache_name, collection_name)

        def action_on_annot(self, answer: str) -> None:
            if answer == "back":
                self.state.prev_example()
                self.update_view()
                return
            self._handle_annot_effect(answer=answer)
            self.state.write_annot(label=answer)
            self.update_view()
        
        def _example_content(self):
            content = self.state.current_example
            if self.state.done():
                return "\n\n" + content + "\n\n"
            if description:
                return f"[bold yellow]{description}[/]\n\n" + content_render(content)
            return content_render(content)

        def update_view(self):
            self.query_one("#content").update(self._example_content())
            if pbar:
                self.query_one("#pbar").update(progress=self.state.position + 1)
        
        def _handle_annot_effect(self, answer: str) -> None:
            self.query_one("#content").remove_class("base-card-border")
            class_to_add = "teal-card-border"
            if answer == "yes":
                class_to_add = "green-card-border"
            if answer == "no":
                class_to_add = "red-card-border"
            if answer == "maybe":
                class_to_add = "orange-card-border"
            self.query_one("#content").add_class(class_to_add)
            self.set_timer(
                self.ACTIVE_EFFECT_DURATION,
                lambda: self.query_one("#content").remove_class(class_to_add),
            )
            self.set_timer(
                self.ACTIVE_EFFECT_DURATION,
                lambda: self.query_one("#content").add_class("base-card-border"),
            )

        def compose(self) -> ComposeResult: 
            items = []
            if pbar:
                items.append(Center(ProgressBar(total=len(self.state), show_eta=False, id="pbar")))
            items.append(Static(self._example_content(), id='content', classes='gray-card-border'))
            yield Container(*items, id='container')
            yield Footer()
            
        
        def on_mount(self) -> None:
            self.title = "Datatui - enriching data from the terminal"
            self.icon = None
            if pbar:
                self.query_one("#pbar").update(progress=self.state.position)
    
    DatatuiApp().run()
