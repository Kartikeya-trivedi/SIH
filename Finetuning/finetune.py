# kolam_train_efficientnet_modal.py
import modal

# --- Step 1: Modal image setup ---
image = (
    modal.Image.debian_slim()
    .pip_install("torch", "torchvision", "tqdm", "scikit-learn")
)

app = modal.App("kolam-efficientnet")

# --- Step 2: Persistent volume for dataset & model ---
vol = modal.Volume.from_name("kolam-dataset", create_if_missing=True)

# --- Step 3: Training function ---
@app.function(
    image=image,
    gpu="any",
    volumes={"/data": vol},
    timeout=60 * 90  # 1.5 hours
)
def train_model(epochs: int = 5, resume: bool = True, checkpoint_path: str = "/data/kolam_efficientnet_b4.pth"):
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torchvision import datasets, transforms, models
    from torch.utils.data import DataLoader, random_split
    from tqdm import tqdm
    
    from PIL import Image
    from PIL import ImageFile
    import os

    # Allow PIL to load truncated images as a last resort (still filtered below)
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # --- Dataset setup ---
    data_dir = "/data/kolam_dataset"
    transform = transforms.Compose([
        transforms.Resize((380, 380)),  # EfficientNet-B4 expects 380x380
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    def safe_loader(image_path: str):
        try:
            with Image.open(image_path) as image:
                return image.convert("RGB")
        except Exception as error:
            print(f"[WARN] Skipping corrupt image: {image_path} ({error})")
            raise FileNotFoundError

    dataset = datasets.ImageFolder(
        root=data_dir,
        transform=transform,
        loader=safe_loader,
    )

    # Proactively filter out corrupt/unreadable samples so DataLoader won't crash
    cleaned_samples = []
    for image_path, label_idx in list(getattr(dataset, "samples", [])):
        try:
            with Image.open(image_path) as im:
                im.verify()  # lightweight integrity check
            cleaned_samples.append((image_path, label_idx))
        except Exception as e:
            print(f"[WARN] Removing corrupt image from dataset: {image_path} ({e})")
            continue

    # If any were removed, update underlying lists
    if cleaned_samples and len(cleaned_samples) != len(dataset.samples):
        dataset.samples = cleaned_samples
        dataset.imgs = cleaned_samples  # alias used by ImageFolder
        dataset.targets = [lbl for _, lbl in cleaned_samples]

    # Split into train/val (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

    # --- EfficientNet-B4 Transfer Learning ---
    model = models.efficientnet_b4(pretrained=True)

    # Freeze backbone layers
    for param in model.features.parameters():
        param.requires_grad = False

    num_classes = len(dataset.classes)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=0.001)

    # --- Resume from checkpoint if available ---
    start_epoch = 0
    if resume and os.path.exists(checkpoint_path):
        try:
            ckpt = torch.load(checkpoint_path, map_location=device)
            # Support both .pth (state_dict) and .ckpt (dict with keys)
            if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
                model.load_state_dict(ckpt["model_state_dict"])
                if "optimizer_state_dict" in ckpt:
                    optimizer.load_state_dict(ckpt["optimizer_state_dict"])
                start_epoch = ckpt.get("epoch", 0)
            else:
                # Assume plain state_dict
                model.load_state_dict(ckpt)
                start_epoch = 0
            print(f"Resumed from checkpoint '{checkpoint_path}' at epoch {start_epoch}")
        except Exception as e:
            print(f"[WARN] Failed to load checkpoint: {e}. Starting from scratch.")

    # --- Training loop ---
    for epoch in range(start_epoch, epochs):
        model.train()
        total_loss = 0
        for inputs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1} Training"):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}, Training Loss: {avg_loss:.4f}")

        # --- Validation ---
        model.eval()
        correct, total = 0, 0
        all_preds, all_labels = [], []
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)

                correct += (preds == labels).sum().item()
                total += labels.size(0)

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        acc = 100 * correct / total
        print(f"Validation Accuracy after epoch {epoch+1}: {acc:.2f}%")

        # --- Save checkpoint each epoch ---
        ckpt = {
            "epoch": epoch + 1,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "classes": dataset.classes,
        }
        torch.save(ckpt, checkpoint_path)
        print(f"✅ Checkpoint saved at {checkpoint_path}")

    # --- Final Report ---
    print("\n📊 Classification Report:")
    print(classification_report(all_labels, all_preds, target_names=dataset.classes))
    print("✅ Training complete")


# --- Step 4: Entry point ---
@app.local_entrypoint()
def main():
    print("🚀 Starting training on Modal with EfficientNet-B4...")
    # Example: extend epochs and resume from previous fine-tuned checkpoint
    train_model.remote(epochs=20, resume=True)
