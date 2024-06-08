from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static, Header
from textual.containers import Container
from rich.text import Text

txt = Text("Hello, [bold magenta]World[/]!", justify="center")

class DatatuiApp(App):
    CSS_PATH = "app.css"
    BINDINGS = [
        Binding(key="yes", action="quit", description="Annotate yes."),
        Binding(key="no", action="no", description="Annotate no."),
        Binding(key="maybe", action="maybe", description="Annotate maybe."),
        Binding(key="skip", action="skip", description="Skip the thing."),
    ]

    def compose(self) -> ComposeResult: 
        yield Header()
        yield Container(
            # Static('Confirm if the entity is correctly assigned. One entity at a time.', id='descr'),
            Static('[black]This is [black on #fef08a] pandas [bold]PYTOOL [/][/] and it is a nice tool. There are so many other great tools too, like scikit-learn and stuff. But this time fi want to focus on this one thing that is the thiing that ia m talking about!', id='content'),
            id='container'
        )
        yield Footer()
        
    
    def on_mount(self) -> None:
        self.title = "Datatui - enriching data from the terminal"
        self.icon = None

if __name__ == "__main__":
    app = DatatuiApp()
    app.run()
