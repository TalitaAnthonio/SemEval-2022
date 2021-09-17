"""A module for checking the format of a submission with predictions.

The requirements for the dataframe representing a submission for the classification task are:
* shall have two columns "Id" and "Class"
* the id is a string:
    * it starts with an integer representing the id of the instance
    * next, there is an underscore
    * finally, the id of the filler (1 to 5)
    * e. g. "42_1" stands for the sentence with id 42 with filler 1
* the class label is string from the label set "implausible", "not-sure", "plausible"

The requirements for the dataframe representing a submission for the ranking task are:
* shall have two columns "Id" and "Rating"
* the id looks like the one for the classification task
* the rating is a float
"""
import argparse
import logging

import pandas as pd

logging.basicConfig(level=logging.DEBUG)


def check_format_of_submission(submission, evaluation_mode): 
    """Check the format of a dataframe with predictions.

    :param submission: dataframe with submission data
    :param evaluation_mode: str describing whether the submission is for the 'ranking' or 'classification' task
    """
    logging.debug("Verifying the format of submission")

    if evaluation_mode == "ranking":
        check_format_for_ranking_submission(submission)

    elif evaluation_mode == "classification":
        check_format_for_classification_submission(submission)

    else:
        raise ValueError("Evaluation mode {0} not available.".format(evaluation_mode))

    logging.debug("Format checking for submission successful. No problems detected.")


def check_format_for_ranking_submission(submission): 
    """Check the format of predictions for the ranking task.

    :param submission: dataframe with submission data
    """
    required_columns = [
        "Id",
        "Rating",
    ]
    if not list(submission.columns) == required_columns:
        raise ValueError(
            "File does not have the required columns: {list(submission.columns)} != {required_columns}."
        )

    check_identifiers(submission["Id"])

    for rating_str in submission["Rating"]:
        try:
            rating = float(rating_str)
        except ValueError:
            raise ValueError("Rating {0} is not a float.".format(rating_str))
        else:
            if 1 > rating or rating > 5:
                raise ValueError(
                    "Rating {0} is not within the range between 1 and 5.".format(rating)
                )


def check_format_for_classification_submission(submission): 
    """Check format of predictions for the classification task.

    :param submission: dataframe with submission data
    """
    required_columns = [
        "Id",
        "Class",
    ]
    if not list(submission.columns) == required_columns:
        raise ValueError("File does not have the required columns: {list(submission.columns)} != {required_columns}.")

    check_identifiers(submission["Id"])

    for class_label in submission["Class"]:
        if class_label not in ["implausible", "not-sure", "plausible"]:
            raise ValueError(
                "Label {0} does not correspond to one of the three available class labels: "
                "'implausible', 'not-sure' and 'plausible'.".format(class_label)
            )


def check_identifiers(id_list): 
    for identifier in id_list:
        if "_" not in identifier:
            raise ValueError("Id {0} does not contain an underscore.".format(identifier))
        else:
            sentence_id_str, filler_id_str = identifier.split("_")

            try:
                int(sentence_id_str)
            except ValueError:
                raise ValueError("The sentence id {0} in id {1} is not a valid integer.".format(sentence_id_str, identifier))

            try:
                filler_id = int(filler_id_str)
            except ValueError:
                raise ValueError(
                    "The filler id {0} in id {1} is not a valid integer.".format(filler_id_str, identifier)
                )
            else:
                if 1 > filler_id or filler_id > 5:
                    raise ValueError(
                        "The filler id {0} in id {1} is not in the range of 1 to 5.".format(filler_id_str, identifier)
                    )


