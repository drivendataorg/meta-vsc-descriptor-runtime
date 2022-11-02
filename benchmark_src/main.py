from pathlib import Path
import shlex
import subprocess

ROOT_DIRECTORY = Path("/code_execution/")
DATA_DIRECTORY = Path("/data")
QUERY_SUBSET_VIDEOS_FOLDER = DATA_DIRECTORY / "queries"
OUTPUT_FILE = ROOT_DIRECTORY / "subset_query_descriptors.npz"
QUERY_SUBSET_FILE = DATA_DIRECTORY / "query_subset.csv"


def main():
    command = shlex.split(
        f"""
    conda run --no-capture-output -n condaenv python -m vsc.baseline.inference
        --torchscript_path "/code_execution/vsc2022/vsc/baseline/adapted_sscd_disc_mixup.torchscript.pt"
        --accelerator=cuda --processes="1"
        --dataset_path "{QUERY_SUBSET_VIDEOS_FOLDER}"
        --output_file "{OUTPUT_FILE}"
    """
    )
    subprocess.run(command, cwd=(ROOT_DIRECTORY / "vsc2022"))


if __name__ == "__main__":
    main()
