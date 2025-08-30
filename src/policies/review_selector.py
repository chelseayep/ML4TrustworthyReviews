import csv
import json
from utils import convert_dict_to_review


def get_violations(prediction: dict) -> list[str]:
    """
    Return a list of violated policies from model predictions.
    """
    violations = []
    if prediction["spam"]:
        violations.append("spam")
    if not prediction["relevance"]:
        violations.append("not relevant")
    if not prediction["credible"]:
        violations.append("not credible")
    return violations


def get_ground_truth_violations(truth: dict) -> list[str]:
    """
    Return a list of ground truth violated policies.
    Assumes truth values are stored as strings ("TRUE"/"FALSE").
    """
    violations = []
    if truth["spam"]:
        violations.append("spam")
    if not truth["relevance"]:
        violations.append("not relevant")
    if not truth["credible"]:
        violations.append("not credible")
    return violations


def load_review_metadata(path: str) -> list[dict]:
    """
    Load review metadata (CSV rows).
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def select_violated_reviews(evaluated_reviews_path: str, metadata_path: str) -> list[dict]:
    """
    Select reviews that violate policies and return a list of structured dicts.
    evaluated_reviews_path: path to JSONL file with predictions + truth
    metadata_path: path to annotated CSV
    """
    # load metadata rows
    metadata = load_review_metadata(metadata_path)

    violated_reviews = []

    # read jsonl predictions
    with open(evaluated_reviews_path) as infile:
        for i, line in enumerate(infile):
            review_json = json.loads(line)

            violations = get_violations(review_json["prediction"])
            truth = get_ground_truth_violations(review_json["truth"])

            if violations:
                review = convert_dict_to_review(i, metadata[i])

                violated_review = {
                    "text": review.input["text"],
                    "rating": review.input["rating"],
                    "business_name": review.input["business"].name,
                    "violations": violations,
                    "ground_truth_violations": truth,
                }
                violated_reviews.append(violated_review)

    return violated_reviews


# Example usage
# evaluated_reviews_path = "/Users/chelsea/Documents/ML4TrustworthyReviews/data/output/test_set_results.jsonl"
# metadata_path = "/Users/chelsea/Documents/ML4TrustworthyReviews/data/processed/test_set_annotated.csv"


# truth_json = truth = '{"id": 12, "prediction": {"review_quaity": "low", "spam": false, "relevance": true, "credible": false}, "truth": {"spam": true, "relevance": true, "credible": false, "_sentiment": "positive", "_informative": null}}'
# review = json.loads(truth_json)

# # Pass only the inner "truth" dict
# test = get_ground_truth_violations(review["truth"])
# print(test)

# =views(evaluated_reviews_path, metadata_path)

