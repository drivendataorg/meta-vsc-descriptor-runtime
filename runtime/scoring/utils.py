from pathlib import Path
from dataclasses import dataclass
from typing import List
import numpy as np
import pandas as pd
from tqdm import tqdm


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
                timestamps=timestamps[start:end],
                feature=feats[start:end, :],
            )
        )
    return results
