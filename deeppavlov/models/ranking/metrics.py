from deeppavlov.core.common.metrics_registry import register_metric

import numpy as np


@register_metric('r@1')
def r_at_1(y_true, y_pred):
    return recall_at_k(y_true, y_pred, k=1)


@register_metric('r@2')
def r_at_2(y_true, y_pred):
    return recall_at_k(y_true, y_pred, k=2)


@register_metric('r@5')
def r_at_5(labels, predictions):
    return recall_at_k(labels, predictions, k=5)

@register_metric('r@10')
def r_at_10(labels, predictions):
    return recall_at_k(labels, predictions, k=10)

def recall_at_k(y_true, y_pred, k):
    num_examples = float(len(y_pred))
    predictions = np.array(y_pred)
    predictions = np.argsort(predictions, -1)[:, :k][::-1]
    num_correct = 0
    for el in predictions:
        if 0 in el:
            num_correct += 1
    return num_correct / num_examples

@register_metric('rank_response')
def rank_response(y_true, y_pred):
    num_examples = float(len(y_pred))
    predictions = np.array(y_pred)
    predictions = np.argsort(predictions, -1)
    rank_tot = 0
    for el in predictions:
        for i, x in enumerate(el):
            if x == 0:
                rank_tot += i
                break
    return float(rank_tot)/num_examples

@register_metric('r@1_insQA')
def r_at_1_insQA(y_true, y_pred):
    return recall_at_k_insQA(y_true, y_pred, k=1)

def recall_at_k_insQA(y_true, y_pred, k):
    labels = np.repeat(np.expand_dims(np.asarray(y_true), axis=1), k, axis=1)
    predictions = np.array(y_pred)
    predictions = np.argsort(predictions, -1)[:, :k]
    flags = np.zeros_like(predictions)
    for i in range(predictions.shape[0]):
        for j in range(predictions.shape[1]):
            if predictions[i][j] in np.arange(labels[i][j]):
                flags[i][j] = 1.
    return np.mean((np.sum(flags, -1) >= 1.).astype(float))
