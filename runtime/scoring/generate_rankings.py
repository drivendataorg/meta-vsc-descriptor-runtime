import json
from multiprocessing.sharedctypes import Value
from pathlib import Path
from utils import VideoFeature, DescriptorSubmission
from metric import MicroAveragePrecision

import pandas as pd
import numpy as np
import typer
import faiss
from faiss.contrib import exhaustive_search

import time

from typing import List, Optional, Tuple
from loguru import logger


PREDICTION_LIMIT = 100_000
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
        logger.info(f"{i} of {nq}...")
        xqi = xq[i : i + bs]  # noqa: E203
        yield xqi
        if bs < 20_000:
            bs *= 2
        i += len(xqi)


def search_with_capped_res(
    xq: np.ndarray, xb: np.ndarray, num_results: int, metric=faiss.METRIC_INNER_PRODUCT
):
    """
    Searches xq (queries) into xb (reference), with a maximum total number of results.
    """
    start = time.time()
    logger.info("Creating index...")
    index = faiss.IndexFlat(xb.shape[1], metric)
    index.add(xb)

    logger.info("Running exhaustive search...")

    radius, lims, dis, ids = exhaustive_search.range_search_max_results(
        index,
        query_iterator(xq),
        0,  # initial radius should be zero
        max_results=2 * num_results,
        min_results=num_results,
        ngpu=-1,  # use GPU if available
    )

    logger.info(f"Final determined radius: {radius}")

    n = len(dis)
    nq = len(xq)
    if n > num_results:
        # crop to num_results exactly
        o = (-1 * dis).argpartition(num_results)[:num_results]
        mask = np.zeros(n, bool)
        mask[o] = True
        new_dis = dis[mask]
        new_ids = ids[mask]
        nres = [0] + [
            mask[lims[i] : lims[i + 1]].sum() for i in range(nq)
        ]  # noqa: E203
        new_lims = np.cumsum(nres)
        lims, dis, ids = new_lims, new_dis, new_ids

    end = time.time()

    logger.info(f"time taken: {end-start}")

    return lims, dis, ids


def evaluate_similarity(
    query: List[VideoFeature],
    reference: List[VideoFeature],
    query_ids: List[int],
    reference_ids: List[int],
):
    # Build the index using reference descriptors and timestamps
    nq = len(query)

    logger.info("Executing similarity search...")

    lims, dis, ids = search_with_capped_res(
        query,
        reference,
        num_results=len(reference),
        metric=faiss.METRIC_INNER_PRODUCT,
    )

    logger.info("Done!")

    score_df = pd.DataFrame(
        {
            "query_id": query_ids[i],
            "reference_id": reference_ids[ids[j]],
            "score": dis[j],
        }
        for i in range(nq)
        for j in range(lims[i], lims[i + 1])
    )

    matching_submission_df = (
        score_df.groupby(["query_id", "reference_id"]).score.max().reset_index()
    )
    return matching_submission_df


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

    logger.info("Loading submission files...")

    submission = DescriptorSubmission(
        query_descriptors_path, reference_descriptors_path
    )

    logger.info("Loading ground truth...")
    # Load the ground truth
    gt_df = pd.read_csv(ground_truth_path)

    # Create rankings by scoring similarity
    logger.info("Evaluating similarity...")
    submission_df = evaluate_similarity(
        submission.query_descriptors,
        submission.reference_descriptors,
        submission.query_ids,
        submission.reference_ids,
    )

    # Save to CSV
    submission_df.to_csv("/code_execution/submission/rankings.csv")

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
