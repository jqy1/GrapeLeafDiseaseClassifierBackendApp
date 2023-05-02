from flask import request
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask import current_app as app
from typing import Dict, Tuple
from werkzeug.datastructures import FileStorage

from flask import current_app as app

from ..utils.decorator import token_required, admin_token_required
from ..config import basedir
from ..service.PredictService import PredictService

from datetime import datetime

predict_api = Namespace('predict', description='Grapevine leaf disease classification related operations')

predict_model = predict_api.model('predict_details', {
    'files': fields.String(required=True, description='Input images for classification '),
})

# import paramater parser, it support file storage.
parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files', help='a image that run a classification', required=True)

@predict_api.route('/')
class DiseasePredict(Resource):
    """
        Plant leaf disease predict resource
    """
    @predict_api.doc('Plant leaf disease classification method')
    #@predict_api.expect(predict_model, validate=True)
    @predict_api.expect(parser)
    @predict_api.doc(params={'file': 'a image that need to be classified.'})
    @predict_api.doc(responses={
        200:'User successfully created.',
        401:"Please upload file.",
        402:"No selected file.",
        403:"Error file type.",
    })
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """ 
            classification function of grapevine leaf, this function can invoke by any clients based on restful api. 
            It recieves a image that clients need to classify a protential disease of grapevine leaf. 
            It response a probablities of plant leaf disease for giving images as json format. 
        
        """
        # get the post data
 
        app.logger.info('successfully invoke DiseasePredict %s %s', "post", len(request.files))
        
        # If empty, request a file.
        if 'file' not in request.files:
            return {
                "code":"401",
                "message":"please upload file.",
                "data": {
                    "files":"None"
                }
            }, 401
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return {
                "code":"402",
                "message":"No selected file.", 
                "data": {
                    "files":"None"
                }
            }, 402

        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # If the user selected an incorrect file type, return error.
        if not allowed_file(file.filename):
            return {
                "code":"403",
                "message":"Error file type.",
                "data": {
                    "files":file.filename
                }
            }, 403
    
        app.logger.info('successfully invoke DiseasePredict %s %s', "post", file.filename)

        model_path = basedir+'/uploads/nnModels/ResNet50_model.pt'
        optimizer_path = basedir+'/uploads/nnModels/optimizer.pt'
        criterion_path = basedir+'/uploads/nnModels/criterion.pt'

        # Disease varieties
        varieties = ['Black Rot','Black Measles','Healthy','Isariopsis']

        print('----------------------------------------------------------------------------------------------------')
        print('Start inference time: ',datetime.now())
        response_object,code = PredictService.image_classification(model_path, optimizer_path, criterion_path, varieties, file)
        print('End inference time: ',datetime.now())
        print('----------------------------------------------------------------------------------------------------')

        return response_object, code

        