"""A module for checking the format of a submission with predictions.

The requirements for the dataframe representing a submission for the classification task are:
* shall have two columns, one with identifiers and another with class labels
* each id is a string:
    * it starts with an integer representing the id of the instance
    * next, there is an underscore
    * finally, the id of the filler (1 to 5)
    * e. g. "42_1" stands for the sentence with id 42 with filler 1
* the class label is string from the label set "IMPLAUSIBLE", "NEUTRAL", "PLAUSIBLE"

The requirements for the dataframe representing a submission for the ranking task are:
* shall have two columns, one with identifiers and another with real-valued plausibility scores
* the id looks like the one for the classification task
* the plausibility score is a float
"""
import logging

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
        raise ValueError("Evaluation mode {} not available.".format(evaluation_mode))

    logging.debug("Format checking for submission successful. No problems detected.")


def check_format_for_ranking_submission(submission):
    """Check the format of predictions for the ranking task.

    :param submission: dataframe with submission data
    """
    check_identifiers(submission["Id"])

    for rating_str in submission["Rating"]:
        try:
            float(rating_str)
        except ValueError:
            raise ValueError("Rating {} is not a float.".format(rating_str))


def check_format_for_classification_submission(submission):
    """Check format of predictions for the classification task.

    :param submission: dataframe with submission data
    """
    check_identifiers(submission[0])

    valid_class_labels = ["IMPLAUSIBLE", "NEUTRAL", "PLAUSIBLE"]
    for class_label in submission[1]:
        if class_label not in valid_class_labels:
            raise ValueError(
                "Label {} is not part of the label set {}".format(class_label, valid_class_labels)
            )


def check_identifiers(id_list):
    for identifier in id_list:
        if "_" not in identifier:
            raise ValueError("Id {} does not contain an underscore.".format(identifier))
        else:
            sentence_id_str, filler_id_str = identifier.split("_")

            try:
                int(sentence_id_str)
            except ValueError:
                raise ValueError(
                    "The sentence id {} in id {} is not a valid integer.".format(sentence_id_str, identifier)
                )

            try:
                filler_id = int(filler_id_str)
            except ValueError:
                raise ValueError(
                    "The filler id {} in id {} is not a valid integer.".format(filler_id_str, identifier)
                )
            else:
                if 1 > filler_id or filler_id > 5:
                    raise ValueError(
                        "The filler id {} in id {} is not in the range of 1 to 5.".format(filler_id, identifier)
                    )
