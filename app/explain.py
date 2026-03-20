def generate_explanation(disease, answers, top3):

    explanation = []

    explanation.append(f"Top image prediction: {top3[0]['disease']}")

    if "YES" in answers:
        explanation.append("User responses support the diagnosis")

    if disease == "mel":
        explanation.append("Irregular borders or color changes suggest melanoma risk")

    elif disease == "bcc":
        explanation.append("Shiny or bleeding lesion indicates basal cell carcinoma")

    elif disease == "nv":
        explanation.append("Stable and uniform mole suggests benign nevus")

    return explanation