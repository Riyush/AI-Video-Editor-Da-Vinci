
from dataset import GameDataset
from in_game_classifier import GameDetectionModel
from train_helpers import train_one_epoch, evaluate

from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import os

# Constants
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCHS = 10
CLIP = 1.0
LOG_INTERVAL = 10
SAVE_PATH = "/Volumes/My Passport for Mac/Coding Projects/AI-Video-Editor-Da-Vinci/AI_tools/in_game_vs_not_in_game_classification/models/best_model.pt"
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)  # Ensure the directory exists

# folder paths
train_folder = "/Volumes/My Passport for Mac/Coding Projects/AI-Video-Editor-Da-Vinci/AI_tools/in_game_vs_not_in_game_classification/data/fortnite/processed_clips/train"
test_folder ="/Volumes/My Passport for Mac/Coding Projects/AI-Video-Editor-Da-Vinci/AI_tools/in_game_vs_not_in_game_classification/data/fortnite/processed_clips/test"

# create Dataset Objects
train_dataset = GameDataset(train_folder, clip_duration=5, fps=30, increment=1, transform=None)
test_dataset = GameDataset(test_folder, clip_duration=5, fps=30, increment=1, transform=None)

#train_dataset.__getitem__(200)

# batch size 4 means we take 4 videos represented as tensors of size: [C, T, H, W]
# and combine them as an input by adding a batch dimension: [B, C, T, H, W]
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

# instantiate the model 
model = GameDetectionModel(
    game_name="fortnite",
    model_architecture="Masked AutoEncoder",
    use_pretrained=True,
    num_classes=2,
    loss_type="Cross Entropy",
    learning_rate=0,
    dropout_rate=0,
    batch_size=4
).to(DEVICE)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

best_val_loss = float('inf')

#training loop
for epoch in range(1, EPOCHS + 1):
    print(f"\n=== Epoch {epoch} ===")

    train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, DEVICE)
    val_loss, val_acc = evaluate(model, test_loader, criterion, DEVICE)

    print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2%}")
    print(f"Val   Loss: {val_loss:.4f}, Val   Acc: {val_acc:.2%}")

    # Save best model
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), SAVE_PATH)
        print(f"✅ Saved best model to {SAVE_PATH}")