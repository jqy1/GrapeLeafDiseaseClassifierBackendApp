#Load librarires
import torch
from torchvision import models, transforms
import pandas as pd
from torch.utils.data import Dataset
import ntpath
from PIL import Image

#Custom pytorch dataset implementation.
class MyDataset(Dataset):
    def __init__(self,X,y, transform=None):
        self.X = X.reset_index().drop('index',axis=1).path
        self.y = torch.tensor(y.reset_index().drop('index',axis=1).variety.astype('category').cat.codes, dtype=torch.long)
        self.transform = transform

    def __len__(self):
        return len(self.X)

    def __getitem__(self,idx):
        img_path = self.X[idx]
        img = Image.open(img_path)
        if self.transform is not None:
            img = self.transform(img)
        label = self.y[idx]

        return (img,label)

#Settings for image transformation
class Config:
    TRANSFORMS = transforms.Compose([
        #Crop the given PIL Image to random size and aspect ratio.
        transforms.Resize((224,224)),
        #Convert a PIL Image or numpy.ndarray to tensor.
        transforms.ToTensor(),
        #Normalize a tensor image with mean and standard deviation that was used on the pretrained model trained on ImageNet.
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

#Process image to pytorch dataset
def prepare_dataset(img_path):
    #Store image paths and their labels in pandas dataframe.
    meta_new = pd.DataFrame([(path, ntpath.basename(ntpath.dirname(path))) for path in [img_path]], columns = ['path','variety']) 

    #Create pytorch dataset
    NEW_IMAGE = MyDataset(meta_new.path,meta_new.variety,Config.TRANSFORMS)

    return NEW_IMAGE