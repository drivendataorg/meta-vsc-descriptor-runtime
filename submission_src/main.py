from pathlib import Path

import pandas as pd
import numpy as np


ROOT_DIRECTORY = Path("/code_execution")
DATA_DIRECTORY = Path("/data")
OUTPUT_FILE = ROOT_DIRECTORY / "submission" / "runtime_query_descriptors.npz"

def generate_query_descriptors(query_video_ids) -> np.ndarray:
    raise NotImplementedError(
        "This script is just a template. You should adapt it with your own code."
    )
    result_images = ...
    scores = ...
    return result_images, scores

def main():
    # Loading subset of query images
    query_subset = pd.read_csv(DATA_DIRECTORY / "query_subset.csv")
    query_subset_video_ids = query_subset.query_ids.values

    ### Generation of query descriptors happens here ######
    query_descriptors, query_video_ids, query_timestamps = generate_query_descriptors(
        query_video_ids
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
