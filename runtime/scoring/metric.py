import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from utils import DataValidationError

QUERY_ID_COL = "query_id"
DATABASE_ID_COL = "reference_id"
SCORE_COL = "score"


class MicroAveragePrecision:
    _name = "Micro Average Precision"
    _short_name = "µAP"
    _tex_formula = r"µAP $= \sum_{k} (R_{k} - R_{k-1}) P_{k} $"
    _description = (
        r"The metric used for this competition is micro average precision (µAP). "
        r"µAP is calculated by ordering predictions by score and "
        r"finding the weighted average of the total precision at each threshold ${k}$ when weighted by "
        r"the increase in recall from the previous threshold. $P_{k}$ and $R_{k}$ are respectively "
        r"precision and recall at threshold $k$."
    )

    @classmethod
    def score(
        cls, predicted: pd.DataFrame, actual: pd.DataFrame, prediction_limit: int
    ):
        """Calculates micro average precision for a ranking task.

        :param predicted: The predicted values as a dataframe with specified column names
        :param actual: The ground truth values as a dataframe with specified column names
        :param prediction_limit: The maximum number of predictions to consider (Note: ignored for this metric)
        """
        if (
            not np.isfinite(predicted[SCORE_COL]).all()
            or np.isnan(predicted[SCORE_COL]).any()
        ):
            raise DataValidationError("Scores must be finite.")

        predicted = predicted.sort_values(SCORE_COL, ascending=False)

        merged = predicted.merge(
            right=actual.assign(actual=1.0),
            how="left",
            on=[QUERY_ID_COL, DATABASE_ID_COL],
        ).fillna({"actual": 0.0})

        # We may not predict for every ground truth, so calculate unadjusted AP then adjust it
        unadjusted_ap = (
            average_precision_score(merged["actual"].values, merged[SCORE_COL].values)
            if merged["actual"].sum()
            else 0.0
        )
        # Rescale average precisions based on total ground truth positive counts
        predicted_n_pos = int(merged["actual"].sum())

        # avoid rows added to validate query ids, will have blank ref_id
        actual_n_pos = int(actual[DATABASE_ID_COL].notna().sum())

        adjusted_ap = unadjusted_ap * (predicted_n_pos / actual_n_pos)
        return adjusted_ap
