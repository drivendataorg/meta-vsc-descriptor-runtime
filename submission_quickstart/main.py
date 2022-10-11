from pathlib import Path
import pandas as pd
import numpy as np

ROOT_DIRECTORY = Path("submission_quickstart")
DATA_DIRECTORY = Path("data")
OUTPUT_FILE = ROOT_DIRECTORY / "runtime_query_descriptors.npz"
QUERY_SUBSET_FILE = DATA_DIRECTORY / "query_subset.csv"


def generate_query_descriptors(subset_video_ids) -> np.ndarray:
    # Initialize a reproducible random number generator
    rng = np.random.RandomState(42)

    # Choose a descriptor dimensionality
    n_dim = rng.choice([16, 32, 64, 128])

    # Initialize return values
    video_ids = []
    timestamps = []
    descriptors = []

    # Generate random descriptors for each video
    for video_id in subset_video_ids:
        # TODO: limit number of descriptors by video length, either
        # from reading in video or checking metadata file
        n_descriptors = rng.randint(low=1, high=11)
        descriptors.append(rng.standard_normal(size=(n_descriptors, n_dim)))

        # Insert random timestamps
        start_timestamps = 30 * rng.random(size=(n_descriptors, 1))
        end_timestamps = start_timestamps + 30 * rng.random(size=(n_descriptors, 1))

        timestamps.append(np.hstack([start_timestamps, end_timestamps]))
        video_ids.append(np.full(n_descriptors, video_id))

    video_ids = np.concatenate(video_ids).astype(np.int32)
    descriptors = np.concatenate(descriptors).astype(np.float32)
    timestamps = np.concatenate(timestamps).astype(np.float32)

    return video_ids, descriptors, timestamps


def main():
    # Loading subset of query images
    query_subset = pd.read_csv(QUERY_SUBSET_FILE)
    query_subset_video_ids = query_subset.query_id.values

    ### Generation of query descriptors happens here ######
    query_video_ids, query_descriptors, query_timestamps = generate_query_descriptors(
        query_subset_video_ids
    )
    ##################################

    np.savez(
        OUTPUT_FILE,
        video_ids=query_video_ids,
        features=query_descriptors,
        timestamps=query_timestamps,
    )


if __name__ == "__main__":
    main()
