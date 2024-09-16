from datatui import datatui, add_entity_highlighting

stream = [
    {"text": "John Doe is a software engineer at Google.", "entity": [{"start": 0, "end": 5, "label": "Person"}]},
    {"text": "Jane Smith works as a data scientist at Facebook.", "entity": [{"start": 0, "end": 4, "label": "Person"}]},
    {"text": "The Eiffel Tower is in Paris.", "entity": [{"start": 0, "end": 13, "label": "Location"}]},
    {"text": "The Louvre is a museum in Paris.", "entity": [{"start": 4, "end": 10, "label": "Location"}]},
    {"text": "The Mona Lisa is a painting by Leonardo da Vinci.", "entity": [{"start": 0, "end": 13, "label": "Location"}]},
]

examples = list(add_entity_highlighting(stream))

if __name__ == "__main__":
    datatui(examples, cache_name="annotations", collection_name="ner", pbar=True, description="Are the NER highlights [bold]accuracte[/bold]?.")
