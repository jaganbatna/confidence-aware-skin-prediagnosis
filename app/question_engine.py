"""
Adaptive Question Engine

This module generates clinical questions based on the
top predicted diseases from the model.
"""

# Question database for each disease
questions_db = {

"mel":[
"Has the lesion changed color recently?",
"Is the lesion asymmetrical?",
"Does it have irregular borders?",
"Has the lesion increased in size?"
],

"bcc":[
"Does the lesion bleed easily?",
"Is it shiny or pearly?",
"Has it grown slowly over months?",
"Does it form a small open sore?"
],

"nv":[
"Has the mole remained stable for years?",
"Is it uniformly colored?",
"Is it round and symmetrical?"
],

"bkl":[
"Is the lesion rough or scaly?",
"Does it appear waxy or stuck-on?",
"Is it slightly raised?"
],

"akiec":[
"Is the lesion rough and dry?",
"Does it feel like sandpaper?",
"Is it located on sun-exposed skin?"
],

"df":[
"Is the lesion firm to touch?",
"Does it dimple when pressed?",
"Is it small and brownish?"
],

"vasc":[
"Is the lesion reddish or purple?",
"Does it look like a cluster of blood vessels?",
"Does it blanch when pressed?"
]

}


def get_questions(top3):
    """
    Generate adaptive clinical questions.

    Strategy:
    1. Ask questions mainly from the top predicted disease.
    2. Add supporting questions from the 2nd disease.
    3. Ensure no duplicates.
    4. Limit to maximum 5 questions for usability.
    """

    questions = []

    # Priority 1: top predicted disease
    primary_disease = top3[0]["disease"]
    questions.extend(questions_db.get(primary_disease, [])[:3])

    # Priority 2: second predicted disease
    if len(top3) > 1:
        secondary_disease = top3[1]["disease"]
        questions.extend(questions_db.get(secondary_disease, [])[:2])

    # Remove duplicates while preserving order
    unique_questions = []
    seen = set()

    for q in questions:
        if q not in seen:
            unique_questions.append(q)
            seen.add(q)

    # Limit number of questions
    return unique_questions[:5]