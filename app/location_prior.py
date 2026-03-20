LOCATION_PRIOR = {
    "face": {"bcc":1.4,"akiec":1.2,"mel":1.1},
    "back": {"mel":1.3,"nv":1.2},
    "leg": {"mel":1.2},
    "arm": {"nv":1.1}
}


def apply_location_prior(predictions, location):

    if location not in LOCATION_PRIOR:
        return predictions

    weights = LOCATION_PRIOR[location]

    for p in predictions:
        disease = p["disease"]
        if disease in weights:
            p["confidence"] *= weights[disease]

    total = sum(p["confidence"] for p in predictions)

    if total == 0:
        return predictions

    for p in predictions:
        p["confidence"] /= total

    return predictions