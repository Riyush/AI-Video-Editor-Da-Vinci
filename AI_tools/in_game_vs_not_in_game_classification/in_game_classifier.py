"""In this file, I create the pytorch class for a model that classifies whether
a 5 second segment of footage is in game or not in game. I finetune 2 model architectures."""

from pathlib import Path
import torch
from transformers import VideoMAEModel, VideoMAEImageProcessor,  AutoModel, AutoConfig
from torchvision.models import resnet50

class GameDetectionModel(torch.nn.Module):
    """Container module that allows testing a CNN architecture and masked autoencoder"""
    def __init__(self, game_name, model_architecture, 
                use_pretrained, num_classes, loss_type,
                learning_rate, dropout_rate, batch_size, 
                save_generated_images=False, convert_to_gray=True):
        """
        params:
            game_name [string]: name of game that we are training on
            model_architecture [string]: base model architecture; should be CNN or masked autoencoder
            dataset_path [string]: obsolete, GameDataset handles this
            frame_dim [tuple] (224,224): obsolete, GameDataset handles this
            clip_length [int]: obsolete, GameDataset handles this
            increment [int]: obsolete, GameDataset handles this
            use_pretrained [boolean]: whether to use pretrained model weights or randomized beginning weights
            num_classes [int]: total possible labels to pick from, This changes depending on classification task
            loss_type [string]: type of loss used, adam, cross entropy, etc
            learning_rate [int]: learning rate - useful hyperparameter
            dropoput_rate [int]: dropout rate - useful hyperparameter
            batch_size [int]: number of images used per backpropogation step
            save_generated_images [path]: Whether to save images that are fed into the neural network.
                This might be useful when applying data augmentation.
            convert_to_gray [boolean]: flag to convert images to gray screen.
        """
        super().__init__()

        self.game_name = game_name
        self.model_architecture = model_architecture
        self.use_pretrained = use_pretrained  #For now, only use True here
        self.num_classes = num_classes
        self.loss_type = loss_type
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.batch_size = batch_size
        self.convert_to_gray = convert_to_gray

        #create a folder to save analyzed images
        Path(self.GENERATOR_IMAGES_FOLDER_NAME).mkdir(parents=True, exist_ok=True) if save_generated_images else None
        
        #create the layers based on model architecture
        if model_architecture == "Masked AutoEncoder":
            self.base_model = VideoMAEModel.from_pretrained("MCG-NJU/videomae-base", torch_dtype=torch.float32)
            self.base_output_dim = 768  # videomae hidden size
            self.feature_adapter = torch.nn.Identity()  # no change needed
        elif model_architecture == "CNN":
            #remove the default linear layer to standardize the hidden layer output
            resnet = resnet50(pretrained=True)
            resnet_output_dim = resnet.fc.in_features  # 2048
            resnet.fc = torch.nn.Identity()
            self.base_model = resnet
            self.base_output_dim = 768  # match VideoMAE
            self.feature_adapter = torch.nn.Linear(resnet_output_dim, self.base_output_dim)  # 2048 -> 768
        else:
            raise("invalid model architecture")
        
        # now we have standardized the output of either resnet50 or the VideoMAE
        # so we can now create a custom pipeline of layers to go through
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(self.base_output_dim, 256), #linear layer to transform from 768 dimensions down to 256
            torch.nn.LayerNorm(256), # Batch Size = 1, so must uses layerNorm
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),  # need to read about dropout a little bit
            torch.nn.Linear(256, 1) #for BCE with logits loss
        )

    def forward(self,x):
        """
        x: Tensor of shape
            [B, N, C, T, H, W]  VideoMAE expects this input tensor format (as per VideoMAE expectation)
            [B, C, T, H, W]     Resnet50 must work on individual frames, so this will be reshaped
        B = Batch Size, N = Number of subclips per clip, T = Number of Frames, C = Color channels, H = Height, W = Width

        Note, due to difference in expected input dimensions, we configure the Dataset
        object to prepare input samples based on the model we are using.

        Returns:
            torch.Tensor: Output logits of shape [B, 1]

        """
        # the default output for VideoMAE is: [B, num_batches, hidden_dim]
        # We convert to [B, hidden_dim] by taking an average of each frame which is num_batches dim
        # results in [B, 768]
        if self.model_architecture == "Masked AutoEncoder":
            # VideoMAE expects input shape: [B*N, T=16, C=3, H=224, W=224]
            x = x.permute(0, 1, 3, 2, 4, 5)  # [B, N, T, C, H, W]
            B, N, T, C, H, W = x.shape
            x = x.view(B * N, T, C, H, W)  # flatten subclips into batch dimension
            
            outputs = self.base_model(x)  # output: {'last_hidden_state': [B*N, num_tokens, hidden_dim]}
            token_embeddings = outputs['last_hidden_state'].mean(dim=1)  # [B*N, hidden_dim]
            clip_embeddings = token_embeddings.view(B, N, -1).mean(dim=1)  # [1, hidden_dim]

            base_model_outputs = clip_embeddings  # [B, 768]
        
        # For the CNN, we need to first convert [B,C,T,H,W] to the expected tensor shape: [B,C,H,W]
        # We do this by taking B x T as first dimension which is the total number of frames in the batch
        #  Now, the resnet50 can process each frame by taking individual slices of B x T the first dimension
        elif self.model_architecture == "CNN":
            # CNN (e.g., ResNet50) expects input shape: [B*T, C, H, W]
            B, C, T, H, W = x.shape
            x = x.permute(0, 2, 1, 3, 4).reshape(B * T, C, H, W)  # [B*T, C, H, W]

            hidden_state_outputs = self.base_model(x)  # [B*T, 2048]
            lower_dim_representation = self.feature_adapter(hidden_state_outputs) # [B*T, 768]
            base_model_outputs = lower_dim_representation.view(B, T, self.base_output_dim).mean(dim=1)  # [B, 768]

        else:
            raise ValueError(f"Unsupported model architecture: {self.model_architecture}")
        
        final_classification = self.classifier(base_model_outputs) # [B, 1]
        return final_classification