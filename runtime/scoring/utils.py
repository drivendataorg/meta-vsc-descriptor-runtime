from pathlib import Path
from dataclasses import dataclass
from typing import List
import numpy as np
from typing import Tuple


@dataclass
class VideoMetadata:
    video_id: int
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
        video_ids.append(np.full(len(feature), feature.video_id, dtype=np.int32))
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


class DataValidationError(Exception):
    pass


class DescriptorSubmission:

    QUERY_RANGE = (20_000, 27_999)
    MAX_QUERY_ROWS = 8_000 * 60
    REFERENCE_RANGE = (200_000, 239_999)
    MAX_REFERENCE_ROWS = 40_000 * 60
    MAX_DIM = 512
    SUBMISSION_DTYPE = np.float32

    def __init__(self, query_path: Path, reference_path: Path):
        self._query = self._load_datset(query_path)
        self._reference = self._load_datset(reference_path)

        self._validate_descriptors(
            self._query, self.QUERY_RANGE, self.MAX_QUERY_ROWS, "query"
        )
        self._validate_descriptors(
            self._reference, self.REFERENCE_RANGE, self.MAX_REFERENCE_ROWS, "reference"
        )

    @property
    def query_descriptors(self):
        """Return full query descriptors ndarray"""
        return self._query["features"]

    @property
    def reference_descriptors(self):
        """Return full reference descriptors ndarray"""
        return self._reference["features"]

    @property
    def query_ids(self):
        """Return strings of the format Q12345"""
        return ["Q" + str(r_id).zfill(5) for r_id in self._query["video_ids"]]

    @property
    def reference_ids(self):
        """Return strings of the format R123456"""
        return ["R" + str(r_id).zfill(6) for r_id in self._reference["video_ids"]]

    @property
    def query_timestamps(self):
        """Return query timestamps"""
        return self._query["timestamps"]

    @property
    def reference_timestamps(self):
        """Return reference timestamps"""
        return self._reference["timestamps"]

    def _validate_descriptors(self, dataset, range: Tuple, max_rows: int, axis: str):
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
            assert all(dataset["video_ids"] >= range[0]) and all(
                dataset["video_ids"] <= range[1]
            ), f"Expected {axis} video IDS in range {range}, got id out of range."

        except AssertionError as e:
            raise DataValidationError("Failed to validate dataset: {e}")

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
