#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from pathlib import Path
from shutil import copyfile, move

import numpy as np
import pandas as pd

parser = ArgumentParser()
parser.add_argument(
    "--subset_proportion",
    help="Proportion of data to include in subset",
    type=float,
    default=0.01,
)
parser.add_argument(
    "--dataset",
    help="Dataset type",
    type=str,
    required=True,
    choices=["train", "test", "phase2"],
)

RUNTIME_DATA_DIR = Path(__file__).parent.parent / "data"
QUERY_SUBSET_DIR = RUNTIME_DATA_DIR / "query"


def main(args: Namespace):
    # Ensure that data has been downloaded to the correct place
    competition_data_dir = Path("competition_data")
    dataset_folder = competition_data_dir / args.dataset
    query_video_dir = dataset_folder / "query"

    query_metadata = dataset_folder / f"{args.dataset}_query_metadata.csv"
    reference_metadata = dataset_folder / f"{args.dataset}_reference_metadata.csv"

    for file in [
        competition_data_dir,
        dataset_folder,
        query_metadata,
        reference_metadata,
    ]:
        if not file.exists():
            raise FileExistsError(
                f"Error: {file} not found. Have you downloaded or symlinked the competition dataset into {competition_data_dir}?"
            )

    p_subset = args.subset_proportion

    # Choose a random subset of query IDs to include
    rng = np.random.RandomState(42)
    query_metadata_df = pd.read_csv(query_metadata)
    subset_query_ids = query_metadata_df.video_id.sample(
        int(np.ceil(query_metadata_df.shape[0] * p_subset)), random_state=rng
    )

    # Copy metadata files and chosen videoss

    subset_query_ids.sort_values().to_csv(
        RUNTIME_DATA_DIR / "query_subset.csv", index=False
    )
    for query_id in subset_query_ids:
        copyfile(
            query_video_dir / f"{query_id}.mp4",
            QUERY_SUBSET_DIR / f"{query_id}.mp4",
        )
    copyfile(query_metadata, RUNTIME_DATA_DIR / "query_metadata.csv")
    copyfile(reference_metadata, RUNTIME_DATA_DIR / "reference_metadata.csv")

    if args.dataset == "train":
        train_ground_truth = dataset_folder / "train_descriptor_ground_truth.csv"
        copyfile(train_ground_truth, RUNTIME_DATA_DIR / train_ground_truth.name)
        ground_truth_subset_df = pd.read_csv(train_ground_truth).set_index("query_id")
        ground_truth_subset_df.loc[
            ground_truth_subset_df.index.isin(subset_query_ids)
        ].to_csv(RUNTIME_DATA_DIR / "subset_ground_truth.csv")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
