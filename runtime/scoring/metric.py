import numpy as np
import pandas as pd
from typing import Tuple, Optional, List


def argsort(seq):
    """
    Like np.argsort but for 1D sequences. Based on https://stackoverflow.com/a/3382369/3853462
    """
    return sorted(range(len(seq)), key=seq.__getitem__)


def precision_recall(
    y_true: np.ndarray, probas_pred: np.ndarray, num_positives: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute precisions, recalls and thresholds.

    Parameters
    ----------
    y_true : np.ndarray
        Binary label of each prediction (0 or 1). Shape [n, k] or [n*k, ]
    probas_pred : np.ndarray
        Score of each prediction (higher score == images more similar, ie not a distance)
        Shape [n, k] or [n*k, ]
    num_positives : int
        Number of positives in the groundtruth.

    Returns
    -------
    precisions, recalls, thresholds
        ordered by increasing recall, as for a precision-recall curve
    """
    probas_pred = probas_pred.flatten()
    y_true = y_true.flatten()
    # to handle duplicates scores, we sort (score, NOT(jugement)) for predictions
    # eg,the final order will be (0.5, False), (0.5, False), (0.5, True), (0.4, False), ...
    # This allows to have the worst possible AP.
    # It prevents participants from putting the same score for all predictions to get a good AP.
    order = argsort(list(zip(probas_pred, ~y_true)))
    order = order[::-1]  # sort by decreasing score
    probas_pred = probas_pred[order]
    y_true = y_true[order]

    ntp = np.cumsum(y_true)  # number of true positives <= threshold
    nres = np.arange(len(y_true)) + 1  # number of results

    precisions = ntp / nres
    recalls = ntp / num_positives
    return precisions, recalls, probas_pred


def average_precision(recalls: np.ndarray, precisions: np.ndarray):
    """
    Compute the micro-average precision score (μAP).

    Parameters
    ----------
    recalls : np.ndarray
        Recalls. Must be sorted by increasing recall, as in a PR curve.
    precisions : np.ndarray
        Precisions for each recall value.

    Returns
    -------
    μAP: float
    """

    # Check that it's ordered by increasing recall
    if not np.all(recalls[:-1] <= recalls[1:]):
        raise Exception("recalls array must be sorted before passing in")
    return ((recalls - np.concatenate([[0], recalls[:-1]])) * precisions).sum()


def find_operating_point(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, required_x: float
) -> Tuple[float, Optional[float], Optional[float]]:
    """
    Find the highest y (and corresponding z) with x at least `required_x`.

    Returns
    -------
    x, y, z
        The best operating point (highest y) with x at least `required_x`.
        If we can't find a point with the required x value, return
        x=required_x, y=None, z=None
    """
    valid_points = x >= required_x
    if not np.any(valid_points):
        return required_x, None, None

    valid_x = x[valid_points]
    valid_y = y[valid_points]
    valid_z = z[valid_points]
    best_idx = np.argmax(valid_y)
    return valid_x[best_idx], valid_y[best_idx], valid_z[best_idx]


def evaluate_metrics(submission_df: pd.DataFrame, gt_df: pd.DataFrame):
    gt_pairs = {
        tuple(row)
        for row in gt_df[["query_id", "reference_id"]].itertuples(index=False)
        if not pd.isna(row.reference_id)
    }

    # Binary indicator for whether prediction is a true positive or false positive
    y_true = np.array(
        [
            tuple(row) in gt_pairs
            for row in submission_df[["query_id", "reference_id"]].itertuples(
                index=False
            )
        ]
    )
    # Confidence score, as if probability. Only property required is greater score == more confident.
    probas_pred = submission_df["score"].values

    p, r, t = precision_recall(y_true, probas_pred, len(gt_pairs))

    # Micro-average precision
    ap = average_precision(r, p)

    # Metrics @ Precision>=90%
    pp90, rp90, tp90 = find_operating_point(p, r, t, required_x=0.9)

    if rp90 is None:
        # Precision was never above 90%
        rp90 = 0.0

    return ap, rp90


class MicroAveragePrecision:
    @classmethod
    def score(
        cls, submission_df: pd.DataFrame, gt_df: pd.DataFrame, prediction_limit: int
    ):
        return evaluate_metrics(submission_df, gt_df)
