# src/services/ai/detection_service.py
import torch
from torchvision import models, transforms
from PIL import Image
from pathlib import Path

CKPT_PATH = Path(r"C:\TechTitans\Finetuning\kolam_efficientnet_b4.pth")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Image transforms
transform = transforms.Compose([
    transforms.Resize((380, 380)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# Load model function
def load_model(ckpt_path: str):
    ckpt = torch.load(ckpt_path, map_location=DEVICE)
    classes = ckpt.get("classes", None)

    model = models.efficientnet_b4(weights=None)
    if classes is None:
        num_classes = model.classifier[1].out_features
        print("WARN: classes not found in checkpoint; using existing head:", num_classes)
    else:
        num_classes = len(classes)
        model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)

    state_dict = ckpt["model_state_dict"] if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
    model.load_state_dict(state_dict, strict=False)
    model.to(DEVICE).eval()
    return model, classes

# Predict image function
@torch.inference_mode()
def predict_image(model, image_path: str, classes=None, topk=1):
    img = Image.open(image_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(DEVICE)

    logits = model(x)
    probs = torch.softmax(logits, dim=1)[0]
    top_probs, top_idxs = probs.topk(topk)
    top_probs = top_probs.detach().cpu().tolist()
    top_idxs = top_idxs.detach().cpu().tolist()

    if classes:
        labels = [classes[i] for i in top_idxs]
    else:
        labels = [str(i) for i in top_idxs]

    return list(zip(labels, [round(p*100, 2) for p in top_probs]))

# Load model at module level for API usage
try:
    model, classes = load_model(CKPT_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model, classes = None, None
