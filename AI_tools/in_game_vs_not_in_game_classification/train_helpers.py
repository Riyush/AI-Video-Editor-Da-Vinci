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
SAVE_PATH = "/Volumes/My Passport for Mac/Coding Projects/AI-Video-Editor-Da-Vinci/AI_tools/models/best_model.pt"

def train_one_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (videos, labels) in enumerate(tqdm(dataloader)):
        videos, labels = videos.to(device), labels.to(device)
        
        optimizer.zero_grad()
        labels = labels.view(-1, 1)  # Converts [B] -> [B, 1]

        outputs = model(videos)  # [B, num_classes]
        loss = criterion(outputs, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP)
        optimizer.step()

        total_loss += loss.item()
        preds = outputs.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

        if batch_idx % LOG_INTERVAL == 0:
            print(f"Train Batch {batch_idx}: Loss = {loss.item():.4f}")

    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    return avg_loss, accuracy


def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for videos, labels in dataloader:
            videos, labels = videos.to(device), labels.to(device)
            outputs = model(videos)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    return avg_loss, accuracy
