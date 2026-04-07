---
title: DermIntelligent
emoji: 🔬
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# 🔬 DermAI — Confidence-Aware Skin Pre-Diagnosis System

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=flat-square&logo=pytorch)
![EfficientNet](https://img.shields.io/badge/Model-EfficientNet--B0-orange?style=flat-square)

> An AI-powered skin disease pre-diagnosis system that uses EfficientNet-B0 with confidence-aware reasoning, adaptive clinical questioning, and Bayesian posterior updates to assist in identifying 7 types of skin lesions.

⚠️ **Disclaimer:** This system is for educational and research purposes only. It is **not a substitute for professional medical advice, diagnosis, or treatment.** Always consult a qualified dermatologist.

---

## 📸 Demo

| Step | Description |
|------|-------------|
| 1️⃣ Upload | Upload a skin lesion image + select body location |
| 2️⃣ Analysis | EfficientNet-B0 predicts disease with confidence score |
| 3️⃣ Questions | Adaptive clinical questions refine diagnosis via Bayesian update |
| 4️⃣ Doctors | Find nearby dermatologists using pincode |

---

## 🧠 How It Works

```
Image Upload
     │
     ▼
EfficientNet-B0 (7-class prediction)
     │
     ▼
Location Prior Applied (face/back/leg/arm)
     │
     ▼
Confidence + Uncertainty Check
     │
     ├── High Confidence (≥0.75) + Low Uncertainty → SAFE ADVISORY
     │
     └── Low Confidence / High Uncertainty → ASK QUESTIONS
                    │
                    ▼
          Adaptive Question Engine
          (disease-specific clinical questions)
                    │
                    ▼
          Bayesian Posterior Update
          (fuse image confidence + symptom score)
                    │
                    ▼
          Final Diagnosis + Explanation
                    │
                    ▼
          Nearby Doctor Search (Pincode)
```

---

## 🗂️ Project Structure

```
confidence-aware-skin-prediagnosis/
│
├── app/                          # FastAPI Backend
│   ├── main.py                   # API endpoints
│   ├── model.py                  # EfficientNet-B0 inference
│   ├── confidence_logic.py       # Confidence thresholds & fusion
│   ├── question_engine.py        # Adaptive clinical questions
│   ├── reasoning.py              # Answer scoring
│   ├── location_prior.py         # Body location priors
│   ├── explain.py                # Diagnosis explanation generator
│   ├── chatbot.py                # Pincode chatbot logic
│   ├── doctor_search.py          # Nearby doctor search (OpenStreetMap)
│   └── schemas.py                # Pydantic request/response models
│
├── Frontend/
│   └── index.html                # Single-page frontend (HTML/CSS/JS)
│
├── models/
│   └── efficientnet_skin_best.pth  # Trained model weights
│
├── data/
│   ├── HAM10000_metadata.csv       # Dataset metadata
│   ├── symptom_questions.csv       # Clinical question bank
│   ├── disease_symptom_matrix.csv  # Disease-symptom mapping
│   └── question_priority.csv      # Question priority weights
│
├── notebooks/
│   ├── 01_data_check.ipynb         # Dataset exploration & pipeline
│   ├── 02_model_basics.ipynb       # Model architecture prototyping
│   ├── 03_confidence_logic.ipynb   # Confidence fusion logic
│   ├── 04_training.ipynb           # Local training experiments
│   ├── 05_model_training_colab.ipynb  # Full GPU training (Colab)
│   └── 06_inference_and_reasoning.ipynb  # Full inference pipeline
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🦠 Supported Skin Conditions

| Code | Full Name |
|------|-----------|
| `mel` | Melanoma |
| `bcc` | Basal Cell Carcinoma |
| `nv` | Melanocytic Nevus |
| `bkl` | Benign Keratosis-like Lesions |
| `akiec` | Actinic Keratoses / Intraepithelial Carcinoma |
| `df` | Dermatofibroma |
| `vasc` | Vascular Lesion |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/jaganbatna/confidence-aware-skin-prediagnosis.git
cd confidence-aware-skin-prediagnosis
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Model Weights

Place your trained model file in the `models/` folder:
```
models/efficientnet_skin_best.pth
```

> The model is not included in the repo due to file size. Train it using `notebooks/05_model_training_colab.ipynb` on Google Colab with the HAM10000 dataset.

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

API will be available at: `http://localhost:8000`

### 6. Open the Frontend

Open `Frontend/index.html` directly in your browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict-image` | Upload image + location → get prediction |
| `POST` | `/submit-answers` | Submit clinical answers → get final diagnosis |
| `POST` | `/chat` | Chatbot for pincode-based doctor search |
| `GET` | `/find-doctors` | Find nearby dermatologists by pincode |

### Example: `/predict-image`

```bash
curl -X POST "http://localhost:8000/predict-image" \
  -F "file=@skin_image.jpg" \
  -F "location=face"
```

**Response:**
```json
{
  "disease": "mel",
  "confidence": 0.72,
  "uncertainty": 0.48,
  "action": "ASK_QUESTIONS",
  "top3": [
    {"disease": "mel", "confidence": 0.72},
    {"disease": "bcc", "confidence": 0.18},
    {"disease": "nv", "confidence": 0.07}
  ],
  "questions": [
    "Has the lesion changed color recently?",
    "Is the lesion asymmetrical?",
    "Does it have irregular borders?"
  ]
}
```

---

## 🧪 Model Training

The model was trained on the **HAM10000** dataset (10,015 dermoscopic images).

| Parameter | Value |
|-----------|-------|
| Architecture | EfficientNet-B0 (pretrained ImageNet) |
| Dataset | HAM10000 |
| Classes | 7 |
| Epochs | 20 |
| Batch Size | 32 |
| Optimizer | Adam (lr=1e-4 → 1e-5) |
| Loss | CrossEntropyLoss (class-weighted) |
| Best Val Accuracy | **72.09%** |
| Training Strategy | Freeze backbone (5 epochs) → Fine-tune all layers |

### Training on Google Colab

Open `notebooks/05_model_training_colab.ipynb` in Colab and connect your Google Drive with the HAM10000 dataset organized as:

```
MyDrive/Capstone Project/
├── data/
│   ├── HAM10000_images_part_1/
│   ├── HAM10000_images_part_2/
│   └── HAM10000_metadata.csv
```

---

## ⚙️ Confidence Logic

```
Uncertainty ≥ 0.45          → ASK_QUESTIONS
Confidence  ≤ 0.45          → ASK_QUESTIONS
Confidence  ≥ 0.75 and
Uncertainty < 0.30          → SAFE_ADVISORY
Otherwise                   → ASK_QUESTIONS
```

**Confidence Fusion Formula:**
```
fused = (0.7 × image_confidence) + (0.3 × sigmoid(symptom_score))
```

---

## 🏥 Doctor Search

Uses **OpenStreetMap (Nominatim + Overpass API)** — no API key required.

- Converts pincode → lat/lng via Nominatim
- Searches for clinics/hospitals within 8km via Overpass API
- Falls back to Google Maps search links if no results found

---

## 📦 Requirements

```
fastapi
uvicorn
torch
torchvision
Pillow
numpy
scikit-learn
pandas
requests
pydantic
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 📓 Notebooks Overview

| Notebook | Purpose |
|----------|---------|
| `01_data_check` | Load HAM10000, verify images, build dataset pipeline |
| `02_model_basics` | TinyCNN prototype, confidence thresholds |
| `03_confidence_logic` | Symptom-question mapping, confidence fusion |
| `04_training` | Local training experiments on small subset |
| `05_model_training_colab` | Full EfficientNet-B0 training on GPU (Colab) |
| `06_inference_and_reasoning` | Full Bayesian inference pipeline |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License


---

## 👤 Author

**Jagan Batna**  
GitHub: [@jaganbatna](https://github.com/jaganbatna)

---

*Built as a Capstone Project — AI-powered skin disease pre-diagnosis with confidence-aware reasoning.*
