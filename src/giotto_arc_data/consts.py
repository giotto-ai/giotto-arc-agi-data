from pathlib import Path
from typing import List

ROOT = Path(__file__).parent.parent.parent
OUT_PATH = ROOT / Path("dataset")
PARTS: List[str] = ["automata", "dsl_random", "dsl_deterministic", "rearc"]
RECORD_ID = 18508333
