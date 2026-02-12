# Copyright © 2026 Giotto.ai SA. All rights reserved.
from typing import Dict, Optional, Any
import orjson
from tqdm import tqdm  # type: ignore
import pyarrow as pa  # type: ignore
from pathlib import Path

from .types import JSONTask


def save_to_parquet(
    tasks: Dict[str, Any],
    path: Path,
    compression: Optional[str] = "snappy",
) -> None:
    if not isinstance(path, Path):
        path = Path(path)
    d = {
        "id": list(tasks.keys()),
        "task": [
            orjson.dumps(x).decode() for x in tqdm(tasks.values(), total=len(tasks))
        ],
    }
    pa.parquet.write_table(pa.table(d), where=path, compression=compression)


if __name__ == "__main__":
    """Here data is a dictionary where:
    - keys: families = ["automata", "dsl_random", "dsl_deterministic", "rearc"]
    - items: a dict {task_id : JSONtask}
    """
    data: Dict[str, Dict[str, JSONTask]] = {}  # -> data is a dictionary
    for family, tasks in data.items():
        save_to_parquet(tasks, path=Path(f"arc_augmented_parquet/{family}.parquet"))
