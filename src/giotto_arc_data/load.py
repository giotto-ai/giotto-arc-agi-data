from typing import Iterator, List, Optional
from pathlib import Path
from tqdm import tqdm  # type: ignore
import pyarrow.parquet as pq  # type: ignore
import orjson
from time import time

from .download import download_zenodo_record
from .types import Sample
from .consts import OUT_PATH, PARTS, RECORD_ID


def maybe_select_shards(path: Path, part: Optional[str] = None):
    shards = path.iterdir()
    if part is not None:
        shards = (x for x in shards if part in str(x))
    return list(shards)


def stream_parquet(
    path: Path, part: Optional[str] = None, batch_size: int = 128
) -> Iterator[Sample]:
    """
    Stream (key, value) pairs from a Parquet file in batches.
    """
    shards = maybe_select_shards(path, part)
    for shard in shards:
        pf = pq.ParquetFile(shard)
        for batch in pf.iter_batches(batch_size=batch_size, columns=["id", "task"]):
            keys = batch.column(0).to_pylist()
            vals = batch.column(1).to_pylist()
            for k, v in zip(keys, vals):
                yield (k, orjson.loads(v))


def load_all_parquet(path: Path, part: Optional[str] = None) -> List[Sample]:
    shards = maybe_select_shards(path, part)
    data: List[Sample] = []
    print("Building dataset")
    time_start = time()
    for shard in tqdm(shards, total=len(shards)):
        table = pq.read_table(shard)  # reads entire file
        keys = table["id"].to_pylist()
        vals = table["task"].to_pylist()
        pbar = tqdm(zip(keys, vals), total=len(keys))
        data.extend((k, orjson.loads(v)) for k, v in pbar)
    print(f"Done in {time() - time_start:3.3}s")
    return data


def load_dataset(
    # path: str | Path,
    stream: bool = True,
    batch_size: int = 128,
    part: Optional[str] = None,
) -> List[Sample] | Iterator[Sample]:

    if part is not None:
        message = f'Expected "part" to be one of ["automata", "dsl_random", "dsl_deterministic", "rearc"], got {part}.'
        assert part in PARTS, message

    ### check is the dataset hsa been downloaded already, if not, download
    download = False
    for part_ in PARTS:
        if not (OUT_PATH / Path(f"{part_}.parquet")).exists():
            download = True
    if download:
        OUT_PATH.mkdir(exist_ok=True, parents=True)
        download_zenodo_record(record_id=RECORD_ID, out_dir=OUT_PATH)

    ### load the data in memory
    if stream:
        return stream_parquet(OUT_PATH, batch_size=batch_size, part=part)
    else:
        return load_all_parquet(OUT_PATH, part=part)
