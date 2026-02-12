from pathlib import Path
import requests  # type: ignore
from tqdm import tqdm  # type: ignore
import os


def zenodo_base_url(use_sandbox: bool = False) -> str:
    return "https://sandbox.zenodo.org" if use_sandbox else "https://zenodo.org"


def download_zenodo_record(
    record_id: int,
    out_dir: str | Path,
    # *,
    # access_token: str | None = None,
    use_sandbox: bool = False,
):
    base = zenodo_base_url(use_sandbox)
    if not isinstance(out_dir, Path):
        out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    headers = {}
    # if access_token is not None:
    # headers["Authorization"] = f"Bearer {os.environ['ZENODO_ACCESS_TOKEN']}"

    # Get record metadata
    r = requests.get(f"{base}/api/records/{record_id}", headers=headers, timeout=60)
    r.raise_for_status()
    record = r.json()
    files = record["files"]

    for f in files:
        filename = f["key"]
        url = f["links"]["self"]  # direct download URL

        out_path = out_dir / filename
        print(f"Downloading {filename}")

        with requests.get(url, headers=headers, stream=True, timeout=300) as resp:
            resp.raise_for_status()
            total = int(resp.headers.get("Content-Length", 0))

            with open(out_path, "wb") as fp, tqdm(
                total=total, unit="B", unit_scale=True, unit_divisor=1024
            ) as bar:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))

    print("Download complete.")
