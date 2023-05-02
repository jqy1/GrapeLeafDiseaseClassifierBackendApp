#Load librarires
import torch
from torchvision import models, transforms
from skorch import NeuralNetClassifier

from ..config import basedir

#Get the pretrained model
class PretrainedModel(torch.nn.Module):
    def __init__(self, output_features):
        super().__init__()
        model = models.resnet50(pretrained=True) #ResNet50
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, output_features)
        self.model = model
        
    def forward(self, x):
        return self.model(x)

#Instantiate Model
def load_model(model_path,optimizer_path,criterion_path,num_of_classes):
        model = NeuralNetClassifier(
                module=PretrainedModel,
                criterion=torch.nn.CrossEntropyLoss,
                module__output_features=num_of_classes, #Numbers of classes
                device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        )
        model.initialize() 
        model.load_params(f_params=model_path,f_optimizer=optimizer_path,f_criterion=criterion_path) 
        return model

