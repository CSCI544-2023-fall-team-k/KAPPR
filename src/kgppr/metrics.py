import re
import string
import unicodedata
import logging

def normalize_text(s):
    s = unicodedata.normalize('NFD', s)

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def em_score(prediction, ground_truth):
    normalized_pred = normalize_text(prediction)
    normalized_gt = normalize_text(ground_truth)
    return normalized_pred == normalized_gt

def em_f1score(prediction, ground_truth):
    # function for MetaQA
    # resolve issues on questions with mutltiple answers
    normalized_pred = set(normalize_text(prediction).split(" "))
    normalized_gt = set(normalize_text(ground_truth).split(" "))

    TP = len(normalized_gt.intersection(normalized_pred))
    precision = 0
    recall = 0
    if TP == 0 or len(normalized_gt) == 0:
        recall = 0
    else:
        recall = TP/len(normalized_gt)
    if TP == 0 or len(normalized_pred) == 0:
        precision = 0
    else:
        precision = TP/len(normalized_pred)
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    return f1_score

def exact_matching(example, pred):
    logging.info(f"Gold Answers: {example.answer} / Prediction: {pred.answer}")
    assert(type(example.answer) is list)
    
    # return max(em_f1score(pred.answer, ans) for ans in example.answer) # uncomment this line if you are running MetaQA or dataset with multiple answers
    return max(em_score(pred.answer, ans) for ans in example.answer) # uncomment this line if you are running dataset that needs exact matcing
