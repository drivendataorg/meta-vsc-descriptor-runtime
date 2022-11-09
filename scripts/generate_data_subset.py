#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from pathlib import Path
from shutil import copyfile, move

import numpy as np
import pandas as pd

parser = ArgumentParser()
parser.add_argument(
    "--subset_fraction",
    help="Fraction of data to include in subset",
    type=float,
    default=0.01,
)
parser.add_argument(
    "--dataset", help="Dataset type - either 'train' or 'test'", type=str, required=True
)


def main(args: Namespace):
    # Ensure that data has been downloaded to the correct place
    COMPETITION_DATA_DIR = Path("competition_data")
    DATASET_FOLDER = COMPETITION_DATA_DIR / args.dataset
    QUERY_VIDEO_DIR = DATASET_FOLDER / "queries"

    QUERY_METADATA = DATASET_FOLDER / "query_metadata.csv"
    REFERENCE_METADATA = DATASET_FOLDER / "reference_metadata.csv"

    for file in [
        COMPETITION_DATA_DIR,
        DATASET_FOLDER,
        QUERY_METADATA,
        REFERENCE_METADATA,
    ]:
        if not file.exists():
            raise FileExistsError(
                f"Error: {file} not found. Have you downloaded or symlinked the competition dataset into {COMPETITION_DATA_DIR}?"
            )

    p_subset = args.subset_fraction

    # Choose a random subset of query IDs to include
    rng = np.random.RandomState(42)
    query_metadata = pd.read_csv(QUERY_METADATA)
    subset_query_ids = query_metadata.video_id.sample(
        int(np.ceil(query_metadata.shape[0] * p_subset)), random_state=rng
    )

    # Copy metadata files and chosen videoss
    RUNTIME_DATA_DIR = Path("data")
    QUERY_SUBSET_DIR = RUNTIME_DATA_DIR / "queries"

    subset_query_ids.to_csv(RUNTIME_DATA_DIR / "query_subset.csv", index=False)
    for query_id in subset_query_ids:
        copyfile(
            QUERY_VIDEO_DIR / f"{query_id}.mp4",
            QUERY_SUBSET_DIR / f"{query_id}.mp4",
        )
    copyfile(QUERY_METADATA, RUNTIME_DATA_DIR / QUERY_METADATA.name)
    copyfile(REFERENCE_METADATA, RUNTIME_DATA_DIR / REFERENCE_METADATA.name)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
