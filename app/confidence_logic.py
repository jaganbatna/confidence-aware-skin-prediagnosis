import math

HIGH_CONF = 0.75
LOW_CONF = 0.45

HIGH_UNCERTAINTY = 0.45
MOD_UNCERTAINTY = 0.30


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def decide_action(confidence: float, uncertainty: float) -> str:
    if uncertainty >= HIGH_UNCERTAINTY:
        return "ASK_QUESTIONS"

    if confidence <= LOW_CONF:
        return "ASK_QUESTIONS"

    if confidence >= HIGH_CONF and uncertainty < MOD_UNCERTAINTY:
        return "SAFE_ADVISORY"

    return "ASK_QUESTIONS"


def fuse_confidence(image_conf: float, symptom_score: float, alpha: float = 0.7) -> float:
    symptom_conf = sigmoid(symptom_score)
    fused = (alpha * image_conf) + ((1 - alpha) * symptom_conf)
    return min(max(fused, 0.0), 1.0)