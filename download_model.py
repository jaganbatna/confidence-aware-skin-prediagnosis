from huggingface_hub import hf_hub_download
import os

os.makedirs("models", exist_ok=True)

if not os.path.exists("models/efficientnet_skin_best.pth"):
    print("Downloading model...")
    hf_hub_download(
        repo_id="Jaganbatna20/DermIntelligent",
        filename="efficientnet_skin_best.pth",
        local_dir="models",
        repo_type="model"
    )
    print("Done!")