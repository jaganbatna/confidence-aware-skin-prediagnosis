def evaluate_answers(answers):

    score = 0

    for ans in answers:

        if ans == "YES":
            score += 1

        elif ans == "NO":
            score -= 0.5

    return score/3