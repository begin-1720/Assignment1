
import os
import json
from pydantic import BaseModel
from datetime import date

DATA_FOLDER = os.path.join(os.path.dirname(__file__), os.pardir, "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

class JSONRepository:
    def __init__(self, filename: str, model_class: type[BaseModel]):
        self.path = os.path.join(DATA_FOLDER, filename)
        self.model_class = model_class
        # ensure file exists
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load(self) -> list[BaseModel]:
        with open(self.path, "r") as f:
            raw = json.load(f)
        # parse each dict into a model instance
        return [self.model_class(**item) for item in raw]

    def save(self, items: list[BaseModel]):
        # convert each model into a JSON-serializable dict
        to_dump = []
        for item in items:
            if isinstance(item, BaseModel):
                to_dump.append(item.model_dump())
            else:
                # fallback if someone passed raw dicts
                to_dump.append(item)
        with open(self.path, "w") as f:
            json.dump(to_dump, f, indent=2, default=str)
