from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator

import numpy as np
import pandas as pd

DATA_DIRECTORY = Path("/data")
QUERY_METADATA_PATH = DATA_DIRECTORY / "query_metadata.csv"
REFERENCE_METADATA_PATH = DATA_DIRECTORY / "reference_metadata.csv"


@dataclass
class VideoMetadata:
    video_id: str
    timestamps: np.ndarray

    def __len__(self):
        return len(self.timestamps)


@dataclass
class VideoFeature(VideoMetadata):
    feature: np.ndarray

    def metadata(self):
        return VideoMetadata(video_id=self.video_id, timestamps=self.timestamps)

    def dimensions(self):
        return self.feature.shape[1]


def same_value_ranges(values):
    start = 0
    value = values[start]

    for i, v in enumerate(values):
        if v == value:
            continue
        yield value, start, i
        start = i
        value = values[start]

    yield value, start, len(values)


def store_features(f, features: List[VideoFeature]):
    video_ids = []
    feats = []
    timestamps = []
    for feature in features:
        video_ids.append(np.full(len(feature), feature.video_id))
        feats.append(feature.feature)
        timestamps.append(feature.timestamps)
    video_ids = np.concatenate(video_ids)
    feats = np.concatenate(feats)
    timestamps = np.concatenate(timestamps)
    np.savez(f, video_ids=video_ids, features=feats, timestamps=timestamps)


def load_features(f) -> List[VideoFeature]:
    data = np.load(f, allow_pickle=False)
    video_ids = data["video_ids"]
    feats = data["features"]
    timestamps = data["timestamps"]

    results = []
    for video_id, start, end in same_value_ranges(video_ids):
        results.append(
            VideoFeature(
                video_id=video_id,
                timestamps=timestamps[start:end, :],
                feature=feats[start:end, :],
            )
        )
    return results


def format_list_truncated(li: Iterator):
    li = list(li)
    if len(li) <= 3:
        return str(li)
    else:
        return str(li[:3]).rstrip("]") + ", ...]"


class DataValidationError(Exception):
    pass


class DescriptorSubmission:
    """For reading and validating descriptor submissions"""

    MAX_DIM = 512
    SUBMISSION_DTYPE = np.float32

    def __init__(self, query_path: Path, reference_path: Path):
        # Load metadata files for validating against
        valid_query_ids, max_query_rows = self._load_metadata(QUERY_METADATA_PATH)
        valid_reference_ids, max_reference_rows = self._load_metadata(
            REFERENCE_METADATA_PATH
        )

        # Load submitted descriptors from npzs
        self._query = self._load_datset(query_path)
        self._reference = self._load_datset(reference_path)

        # Validate submitted descriptor data against emtadata
        self._validate_descriptors(
            self._query, valid_query_ids, max_query_rows, "query"
        )
        self._validate_descriptors(
            self._reference,
            valid_reference_ids,
            max_reference_rows,
            "reference",
        )

    @property
    def query_descriptors(self):
        return self._query["features"]

    @property
    def reference_descriptors(self):
        return self._reference["features"]

    @property
    def query_ids(self):
        return self._query["video_ids"]

    @property
    def reference_ids(self):
        return self._reference["video_ids"]

    @property
    def query_timestamps(self):
        return self._query["timestamps"]

    @property
    def reference_timestamps(self):
        return self._reference["timestamps"]

    def _validate_descriptors(self, dataset, valid_ids, max_rows: int, axis: str):
        try:
            # Shape
            nrows = dataset["features"].shape[0]
            assert (
                nrows < max_rows
            ), f"Too many {axis} rows. Expected {max_rows}, got {nrows}"

            ndims = dataset["features"].shape[1]
            assert (
                ndims <= self.MAX_DIM
            ), f"{axis} descriptor dimensionality {ndims} exceeds max of {self.MAX_DIM}"

            # Non-null
            assert not np.isnan(
                dataset["features"]
            ).any(), f"Your {axis} descriptors contain at least one null value"

            # Valid IDs
            valid_ids = set(valid_ids)
            submission_ids = set(dataset["video_ids"])
            invalid_ids = submission_ids.difference(valid_ids)
            assert (
                len(invalid_ids) == 0
            ), f"Submission has {len(invalid_ids)} invalid {axis} id values: {format_list_truncated(invalid_ids)}"

        except AssertionError as e:
            raise DataValidationError(f"Failed to validate dataset: {e}")

    def _load_metadata(self, path: Path):
        try:
            metadata_df = pd.read_csv(path)
            valid_int_ids = metadata_df.video_id
            max_rows = metadata_df.duration_sec.apply(np.ceil).sum()
        except:
            raise DataValidationError(
                f"Unable to read in metadata csv {path} and extract video ids and lengths."
            )
        return valid_int_ids, max_rows

    def _load_datset(self, path: Path):
        try:
            with np.load(path, allow_pickle=False) as dataset:
                descriptors = dataset["features"]
                video_ids = dataset["video_ids"]
                timestamps = dataset["timestamps"]
        except (OSError, ValueError) as e:
            raise DataValidationError(f"Error loading path {path} using np.load: {e}")
        except KeyError as e:
            raise DataValidationError(f"Data structure did not have expected key: {e}")

        try:
            assert len(descriptors) == len(video_ids) and len(descriptors) == len(
                timestamps
            )
        except AssertionError:
            lengths = {k: len(dataset[v]) for k, v in dataset.items()}
            raise DataValidationError(
                f"Descriptors, video_ids, and timestamps must have same length, got {lengths}."
            )
        return {
            "features": descriptors,
            "video_ids": video_ids,
            "timestamps": timestamps,
        }
