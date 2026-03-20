from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

# IMPORTS (THIS WAS MISSING)
from app.model import predict
from app.confidence_logic import decide_action, fuse_confidence
from app.question_engine import get_questions
from app.reasoning import evaluate_answers
from app.schemas import AnswerRequest
from app.chatbot import ask_chatbot
from app.doctor_search import find_nearby_doctors
from app.location_prior import apply_location_prior
from app.explain import generate_explanation

# CREATE APP (THIS WAS MISSING)
app = FastAPI(title="Skin Disease Diagnostic API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROOT
@app.get("/")
def root():
    return {"message": "System Running"}

# ---------------- IMAGE PREDICTION ----------------
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...), location: str = Form("unknown")):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    result = predict(image)

    top3 = result["top3"]
    uncertainty = result["uncertainty"]

    # Apply location prior
    top3 = apply_location_prior(top3, location)

    top1 = top3[0]

    action = decide_action(top1["confidence"], uncertainty)

    questions = None
    if action == "ASK_QUESTIONS":
        questions = get_questions(top3)

    return {
        "disease": top1["disease"],
        "confidence": top1["confidence"],
        "uncertainty": uncertainty,
        "action": action,
        "questions": questions
    }

# ---------------- ANSWERS ----------------
@app.post("/submit-answers")
def submit_answers(data: AnswerRequest):

    disease = data.disease
    image_conf = data.image_conf
    answers = data.answers

    symptom_score = evaluate_answers(answers)

    fused = fuse_confidence(image_conf, symptom_score)

    decision = decide_action(fused, 0.2)

    explanation = generate_explanation(
        disease,
        answers,
        [{"disease": disease, "confidence": image_conf}]
    )

    return {
        "disease": disease,
        "confidence": fused,
        "decision": decision,
        "explanation": explanation
    }

# ---------------- CHATBOT ----------------
@app.post("/chat")
def chat(data: dict):

    message = data.get("message")
    disease = data.get("disease")

    response = ask_chatbot(message, disease)

    if response.get("action") == "FETCH_DOCTORS":

        doctors = find_nearby_doctors(
            response["pincode"],
            response["disease"]
        )

        if not doctors:
            return {"reply": "❌ No doctors found nearby."}

        return {
            "reply": f"🏥 Doctors for {response['disease']}:",
            "doctors": doctors
        }

    return response

# ---------------- DOCTOR SEARCH ----------------
@app.get("/find-doctors")
def find_doctors(pincode: str, disease: str):

    doctors = find_nearby_doctors(pincode, disease)

    return {"doctors": doctors}