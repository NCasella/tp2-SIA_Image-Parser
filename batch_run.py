import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Path to the folder with all the config.json files
batch_folder = Path("batch_config")

# Get all .json files in that folder
config_paths = list(batch_folder.glob("*.json"))


def run_config(config_path: Path):
    folder_name = config_path.stem
    output_folder = Path(folder_name)
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / f"{folder_name}.txt"

    print(f"[STARTED] {config_path.name}")

    try:
        with open(output_file, "w") as out:
            subprocess.run(
                ["python3", "main.py", str(config_path)],
                stdout=out,
                stderr=subprocess.STDOUT,
                check=True
            )
        print(f"[FINISHED] {config_path.name} -> {output_file}")
    except subprocess.CalledProcessError:
        print(f"[FAILED] {config_path.name} (see {output_file} for logs)")


# Limit number of concurrent runs if needed (None = all at once)
MAX_WORKERS = None  # or set to something like 4

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(run_config, config_path) for config_path in config_paths]
    for future in as_completed(futures):
        pass  # All logging is handled in the run_config function