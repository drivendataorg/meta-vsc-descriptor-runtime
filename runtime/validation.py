#!/usr/bin/env python3
"""
Descriptor Track validation script
"""
import logging
from argparse import ArgumentParser, Namespace

import numpy as np
import pandas as pd

parser = ArgumentParser()
parser.add_argument(
    "--query_features",
    help="Path containing query features",
    type=str,
    required=True,
)
parser.add_argument(
    "--ref_features",
    help="Path containing reference features",
    type=str,
    required=True,
)
parser.add_argument(
    "--query_metadata",
    help="Path containing query metadata",
    type=str,
    required=True,
)
parser.add_argument(
    "--ref_metadata",
    help="Path containing reference metadata",
    type=str,
    required=True,
)
parser.add_argument("--subset", help="Path containing query subset ids", type=str)


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("descriptor_eval_lib.py")
logger.setLevel(logging.INFO)


class DataValidationError(AssertionError):
    pass


def main(args: Namespace):
    query_features = np.load(args.query_features, allow_pickle=False)
    ref_features = np.load(args.ref_features, allow_pickle=False)
    query_meta = pd.read_csv(args.query_metadata)
    ref_meta = pd.read_csv(args.ref_metadata)
    if args.subset:
        subset = pd.read_csv(args.subset)
        query_meta = query_meta.set_index("video_id").loc[subset.video_id]
    query_total_seconds = query_meta.duration_sec.apply(np.ceil).sum()
    ref_total_seconds = ref_meta.duration_sec.apply(np.ceil).sum()

    def validate_shape(dataset: str, n_features: int, total_seconds: float):
        if n_features > total_seconds:
            raise DataValidationError(
                f"Error: Number of {dataset} video features must not exceed one feature per second. "
                f"Saw {n_features} vectors, max allowed is {query_total_seconds}"
            )

    validate_shape("query", query_features["features"].shape[0], query_total_seconds)
    validate_shape("reference", ref_features["features"].shape[0], ref_total_seconds)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
