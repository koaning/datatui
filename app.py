from diskcache import Cache 
from hashlib import md5
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static, ProgressBar
from textual.containers import Container, Center, Middle
from rich.text import Text

txt = Text("Hello, [bold magenta]World[/]!", justify="center")


class State:
    def __init__(self, input_stream, cache: str) -> None:
        self.cache = Cache(cache)
        self._input_stream = input_stream
        self._input_size = len(input_stream)
        self._content_key = "content"
        self._current_example = None
        self._done = False

    def mk_hash(self, ex):
        return md5(ex[self._content_key].encode()).hexdigest()

    def write_annot(self, label):
        if not self._done:
            self.cache[self.mk_hash(self.current_example)] = {**self.current_example, 'label': label}
            return self.next_example()
    
    @property
    def stream_size(self):
        return self._input_size

    def stream(self):
        for i in self._input_stream:
            ex = {self._content_key: f'example {i}'}
            if self.mk_hash(ex) not in self.cache:
                yield {self._content_key: f'example {i}'}
    
    @property
    def current_example(self):
        if self._current_example is None:
            try:
                self._current_example = next(self.stream())
            except StopIteration:
                self._current_example = {"content": "No more examples."}
                self._done = True
        return self._current_example
    
    def next_example(self):
        try:
            self._current_example = next(self.stream())
        except StopIteration:
            self._current_example = {"content": "No more examples."}
            self._done = True
        return self._current_example


class DatatuiApp(App):
    ACTIVE_EFFECT_DURATION = 0.6
    CSS_PATH = "app.css"
    BINDINGS = [
        Binding(key="y", action="on_annot('yes')", description="Annotate yes."),
        Binding(key="n", action="on_annot('no')", description="Annotate no."),
        Binding(key="m", action="on_annot('maybe')", description="Annotate maybe."),
        Binding(key="s", action="on_annot('skip')", description="Skip the thing."),
    ]
    state = State(range(10), "cache")

    def action_on_annot(self, answer: str) -> None:
        self._handle_annot_effect(answer=answer)
        self.state.write_annot(label=answer)
        self.update_view()
    
    def update_view(self):
        self.query_one("#content").update(self.state.current_example["content"])
        self.query_one("#pbar").update(advance=1)
    
    def _handle_annot_effect(self, answer: str) -> None:
        self.query_one("#content").remove_class("base-card-border")
        class_to_add = "gray-card-border"
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
        # yield Header()
        yield Container(
            Center(
                ProgressBar(total=self.state.stream_size, show_eta=False, id="pbar")
            ),
            Static(self.state.current_example['content'], id='content', classes='gray-card-border'),
            id='container'
        )
        yield Footer()
        
    
    def on_mount(self) -> None:
        self.title = "Datatui - enriching data from the terminal"
        self.icon = None
        self.query_one("#pbar").update(progress=len(self.state.cache))

if __name__ == "__main__":
    app = DatatuiApp()
    app.run()
