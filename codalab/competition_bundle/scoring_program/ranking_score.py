"""A module for the evaluation metrics."""
import pandas as pd
from scipy.stats import spearmanr
from format_checker_for_submission import check_format_of_submission


def score_ranking_task(submission_file,truth_file): 
    """Compute a performance score based on predictions for the ranking task.
    :param submission_file: str path to submission file with predictions
    :param truth_file: str path to file with ground truth labels
    :return: float Spearman's rank correlation coefficient
    """
    submission = pd.read_csv(submission_file, delimiter="\t")
    check_format_of_submission(submission, evaluation_mode="ranking")

    reference = pd.read_csv(truth_file, delimiter="\t")
    del reference['Class']
    check_format_of_submission(reference, evaluation_mode="ranking")

    gold_ratings = []
    predicted_ratings = []

    for _, row in submission.iterrows():
        reference_indices = list(reference["Id"][reference["Id"] == row["Id"]].index)

        if not reference_indices:
            raise ValueError("Identifier {0} does not appear in reference file.".format(row["Id"]))
        elif len(reference_indices) > 1:
            raise ValueError("Identifier {0} appears several times in reference file.".format(row["Id"]))
        else:
            reference_index = reference_indices[0]
            gold_ratings.append(float(reference["Rating"][reference_index]))
            predicted_ratings.append(float(row["Rating"]))

    return spearmans_rank_correlation(gold_ratings=gold_ratings, predicted_ratings=predicted_ratings)


def spearmans_rank_correlation(gold_ratings, predicted_ratings): 
    """Score submission for the ranking task with Spearman's rank correlation.
    :param gold_ratings: list of float gold ratings
    :param predicted_ratings: list of float predicted ratings
    :return: float Spearman's rank correlation coefficient
    """
    if len(gold_ratings) == 1 and len(predicted_ratings) == 1:
        raise ValueError("Cannot compute rank correlation on only one prediction.")

    return spearmanr(a=gold_ratings, b=predicted_ratings)[0]
