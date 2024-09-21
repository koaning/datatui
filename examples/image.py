from PIL import Image
from rich.align import Align
from rich_pixels import Pixels
from datatui import datatui
from pathlib import Path

stream = [{"path": str(p)} for p in sorted(Path("examples/pokemons").glob("*.png"))]

def render_image(ex):
    with Image.open(ex["path"]) as image:
        resized_image = image.resize((40, 40), Image.LANCZOS)
        return Align.center(Pixels.from_image(resized_image), vertical="middle")
    
app = datatui(stream, 
        cache_name="annotations", 
        collection_name="pokemon", 
        pbar=True, 
        description="Is this a fire pokemon?",
        content_render=render_image)

if __name__ == "__main__":
    app.run()
