from sklearn.metrics import accuracy_score, log_loss

def evaluate_predictions(y_true, y_pred, y_prob=None):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred)
    }

    if y_prob is not None:
        metrics["log_loss"] = log_loss(y_true, y_prob)

    return metrics