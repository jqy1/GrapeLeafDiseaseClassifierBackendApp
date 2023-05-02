from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Tuple
#from werkzeug.utils import secure_filename
from os import path
from PIL import Image

from ..config import basedir
from .LoadModel import load_model
from .PrepareDataset import prepare_dataset

class PredictService(object):
    """
        PredictService for grapevine leaf disease classification, it will invoke a PyTorch model to classify a protential disease of input images
    """
    def __init__(self):
        pass

    # Avoid duplicate in the folder (prior to saving the file)
    @staticmethod
    def uniquify(file_path):
        filename, extension = path.splitext(file_path) 
        counter = 1
        while path.exists(file_path):
            file_path = filename+"("+str(counter)+")"+extension
            counter += 1
        return file_path

    # Save new incoming image file to dedicated folder and return full path
    @staticmethod
    def save_file(file):
        file_path = basedir+'/uploads/grapevine/'+file.filename # or secure_filename(n_filename)
        file_path = PredictService.uniquify(file_path)
        file.save(file_path)
        Image.open(file_path).convert('RGB').save(file_path)
        return file_path

    # Classify the image(s) and output the result.
    @staticmethod
    def image_classification(model_path, optimizer_path, criterion_path, varieties, file):
        model = load_model(model_path, optimizer_path, criterion_path, len(varieties))
        img_path = PredictService.save_file(file)
        NEW_IMAGE = prepare_dataset(img_path)
        y_proba = model.predict_proba(NEW_IMAGE)
        y_result = model.predict(NEW_IMAGE)
        response_object = {
            "code":"200",
            "message":"Classification complete.",
            "data": [
                {'Classified Type': varieties[y_result[0]]},
                {varieties[0]: str(y_proba[0][0])},
                {varieties[1]: str(y_proba[0][1])},
                {varieties[2]: str(y_proba[0][2])},
                {varieties[3]: str(y_proba[0][3])}
            ] 
        }
        return response_object, 200