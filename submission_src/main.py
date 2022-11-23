from pathlib import Path
import pandas as pd
import numpy as np

ROOT_DIRECTORY = Path("/code_execution")
DATA_DIRECTORY = Path("/data")
QRY_VIDEOS_DIRECTORY = DATA_DIRECTORY / "query"
OUTPUT_FILE = ROOT_DIRECTORY / "subset_query_descriptors.npz"
QUERY_SUBSET_FILE = DATA_DIRECTORY / "query_subset.csv"


def generate_query_descriptors(query_video_ids) -> np.ndarray:
    raise NotImplementedError(
        "This script is just a template. You should adapt it with your own code."
    )
    video_ids = ...
    descriptors = ...
    timestamp_intervals = ...
    return video_ids, descriptors, timestamp_intervals


def main():
    # Loading subset of query images
    query_subset = pd.read_csv(QUERY_SUBSET_FILE)
    query_subset_video_ids = query_subset.video_id.values.astype("U")

    # Generation of query descriptors happens here
    query_video_ids, query_descriptors, query_timestamps = generate_query_descriptors(
        query_subset_video_ids
    )

    np.savez(
        OUTPUT_FILE,
        video_ids=query_video_ids,
        features=query_descriptors,
        timestamps=query_timestamps,
    )


if __name__ == "__main__":
    main()
