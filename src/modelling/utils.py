import pickle
from pathlib import Path
from typing import Any


def save_pickle(obj: Any, path: str | Path) -> None:
    """Pickle `obj` to `path`, creating the parent folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path: str | Path) -> Any:
    """Load a pickled object from `path`."""
    with open(path, "rb") as f:
        return pickle.load(f)
