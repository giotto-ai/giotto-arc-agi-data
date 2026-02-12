# Copyright © 2026 Giotto.ai SA. All rights reserved.

from pathlib import Path
from typing import List

ROOT = Path(__file__).parent.parent.parent
OUT_PATH = ROOT / Path("dataset")
PARTS: List[str] = [
    "automata",
    "dsl_random",
    "dsl_deterministic",
    "rearc",
    "seeds_original",
    "seeds_additional",
]
RECORD_ID = 18508333
