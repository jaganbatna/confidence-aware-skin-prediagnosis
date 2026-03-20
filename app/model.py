import torch
import torch.nn.functional as F
from torchvision import models, transforms
from torchvision.models import EfficientNet_B0_Weights
from PIL import Image
import numpy as np

# ---------------- CONFIG ----------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASSES = ["akiec","bcc","bkl","df","mel","nv","vasc"]

MODEL_PATH = "models/efficientnet_skin_best.pth"

# ⚠️ REMOVE temperature scaling (important fix)
TEMPERATURE = 1.0

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# ---------------- LOAD MODEL ----------------
def load_model():
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 7)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()

    return model

model = load_model()

# ---------------- PREDICT ----------------
def predict(image: Image.Image):

    img = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(img)

        # ⚠️ FIXED: no artificial scaling
        outputs = outputs / TEMPERATURE

        probs = F.softmax(outputs, dim=1)[0].cpu().numpy()

    # Top-3
    idx = np.argsort(probs)[-3:][::-1]

    top3 = []
    for i in idx:
        top3.append({
            "disease": CLASSES[i],
            "confidence": float(probs[i])
        })

    # entropy (uncertainty)
    entropy = -np.sum(probs * np.log(probs + 1e-9))

    return {
        "top3": top3,
        "uncertainty": float(entropy)
    }