import pandas as pd
from sklearn.metrics import average_precision_score


QUERY_ID_COL = "query_id"
DATABASE_ID_COL = "reference_id"
SCORE_COL = "score"


class MicroAveragePrecision:
    _name = "Micro Average Precision"
    _short_name = "µAP"
    _tex_formula = r"µAP $= \sum_{n=1}^N (R_{n} - R_{n-1}) P_{n} $"
    _description = (
        r"The metric used for this competition is micro average precision (µAP). "
        r"µAP is calculated by ordering predictions by score and "
        r"finding the weighted average of precisions at each score threshold when weighted by "
        r"the increase in recall from the previous threshold. $P_{n}$ and $R_{n}$ are respectively "
        r"precision and recall threshold $n$."
    )

    @classmethod
    def score(
        cls, predicted: pd.DataFrame, actual: pd.DataFrame, prediction_limit: int
    ):
        """Calculates micro average precision for a ranking task.

        :param predicted: The predicted values as a dataframe with specified column names
        :param actual: The ground truth values as a dataframe with specified column names
        :param prediction_limit: The maximum number of predictions to consider
        """
        predicted = predicted.sort_values(SCORE_COL, ascending=False).iloc[
            :prediction_limit, :
        ]
        import pdb

        pdb.set_trace()

        merged = predicted.merge(
            right=actual.assign(actual=1.0),
            how="left",
            on=[QUERY_ID_COL, DATABASE_ID_COL],
        ).fillna({"actual": 0.0})

        ap = (
            average_precision_score(merged["actual"].values, merged[SCORE_COL].values)
            if merged["actual"].sum()
            else 0.0
        )

        return ap
