import json
from multiprocessing.sharedctypes import Value
from pathlib import Path
from utils import VideoFeature
from metric import MicroAveragePrecision

import pandas as pd
import numpy as np
import typer
import faiss
from faiss.contrib import exhaustive_search

from typing import List, Optional, Tuple


PREDICTION_LIMIT = 100000
QUERY_ID_COL = "query_id"
DATABASE_ID_COL = "reference_id"
SCORE_COL = "score"


def query_iterator(xq: np.ndarray):
    """
    Produces batches of progressively increasing sizes.
    """
    nq = len(xq)
    bs = 32
    i = 0
    while i < nq:
        xqi = xq[i : i + bs]  # noqa: E203
        yield xqi
        if bs < 20_000:
            bs *= 2
        i += len(xqi)


def search_with_capped_res(
    xq: np.ndarray, xb: np.ndarray, num_results: int, metric=faiss.METRIC_L2
):
    """
    Searches xq (queries) into xb (reference), with a maximum total number of results.
    """
    index = faiss.IndexFlat(xb.shape[1], metric)
    index.add(xb)

    radius, lims, dis, ids = exhaustive_search.range_search_max_results(
        index,
        query_iterator(xq),
        1e10,  # initial radius is arbitrary
        max_results=2 * num_results,
        min_results=num_results,
        ngpu=-1,  # use GPU if available
    )

    n = len(dis)
    nq = len(xq)
    if n > num_results:
        # crop to num_results exactly
        o = dis.argpartition(num_results)[:num_results]
        mask = np.zeros(n, bool)
        mask[o] = True
        new_dis = dis[mask]
        new_ids = ids[mask]
        nres = [0] + [
            mask[lims[i] : lims[i + 1]].sum() for i in range(nq)
        ]  # noqa: E203
        new_lims = np.cumsum(nres)
        lims, dis, ids = new_lims, new_dis, new_ids

    return lims, dis, ids


def evaluate_similarity(
    query: List[VideoFeature],
    reference: List[VideoFeature],
    query_ids: List[int],
    reference_ids: List[int],
):
    # Build the index using reference descriptors and timestamps
    nq = len(query)

    # range search max results is not currently functioning for METRIC_INNER_PRODUCT
    # Workaround, per faiss wiki, is to add an extra dimension in such a way as to make
    # L2 search equivalent to IP search.
    # See https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances
    # and https://gist.github.com/mdouze/e4bdb404dbd976c83fe447e529e5c9dc
    def augment_xb(xb, phi=None):
        norms = (xb**2).sum(1)
        if phi is None:
            phi = norms.max()
        extracol = np.sqrt(phi - norms)
        return np.hstack((xb, extracol.reshape(-1, 1)))

    def augment_xq(xq):
        extracol = np.zeros(len(xq), dtype="float32")
        return np.hstack((xq, extracol.reshape(-1, 1)))

    aug_query = augment_xq(query)
    aug_reference = augment_xb(reference)

    lims, dis, ids = search_with_capped_res(
        aug_query,
        aug_reference,
        num_results=len(reference) * 30,
        metric=faiss.METRIC_L2,
    )

    score_df = pd.DataFrame(
        {
            "query_id": query_ids[i],
            "reference_id": reference_ids[ids[j]],
            "score": -dis[j],
        }
        for i in range(nq)
        for j in range(lims[i], lims[i + 1])
    )

    matching_submission_df = (
        score_df.groupby(["query_id", "reference_id"]).score.max().reset_index()
    )
    return matching_submission_df

    # Query index with each "batch" of query descriptors


def main(
    query_descriptors_path: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to query descriptors (query_descriptors.npz)",
    ),
    reference_descriptors_path: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to reference descriptors file (reference_descriptors.npz)",
    ),
    ground_truth_path: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to ground truth CSV file.",
    ),
):
    """Evaluate a submission for the Meta VSC."""

    # Load the query and reference descriptors
    query_dataset = np.load(query_descriptors_path, allow_pickle=False)
    query_ids = ["Q" + str(q_id).zfill(4) for q_id in query_dataset["video_ids"]]
    query_descriptors = query_dataset["features"]

    reference_dataset = np.load(reference_descriptors_path, allow_pickle=False)
    reference_ids = [
        "R" + str(r_id).zfill(5) for r_id in reference_dataset["video_ids"]
    ]
    reference_descriptors = reference_dataset["features"]

    # Load the ground truth
    gt_df = pd.read_csv(ground_truth_path)

    # Create rankings by scoring similarity
    submission_df = evaluate_similarity(
        query_descriptors, reference_descriptors, query_ids, reference_ids
    )

    # Calculate the metric
    micro_avg_precision = MicroAveragePrecision.score(
        submission_df, gt_df, PREDICTION_LIMIT
    )

    typer.echo(
        json.dumps(
            {
                "micro_average_precision": micro_avg_precision,
            }
        )
    )


if __name__ == "__main__":
    typer.run(main)
