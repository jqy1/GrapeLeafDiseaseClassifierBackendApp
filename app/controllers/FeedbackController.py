from flask import request
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask import current_app as app
from typing import Dict, Tuple
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from os import path
from PIL import Image

from flask import current_app as app

from ..utils.decorator import token_required, admin_token_required

from ..config import basedir

feedback_api = Namespace('feedback', description='Grapevine leaf disease feedback and storage')

feedback_model = feedback_api.model('feedback_details', {
    'files': fields.String(required=True, description='Feedback images for future training'),
})

# import paramater parser, it support file storage.
parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files', help='a image from feedback', required=True)

@feedback_api.route('/')
class Diseasefeedback(Resource):
    """
        Plant leaf disease feedback resource
    """
    @feedback_api.doc('Plant leaf disease feedback method')
    #@feedback_api.expect(feedback_model, validate=True)
    @feedback_api.expect(parser)
    @feedback_api.doc(params={'file': 'an image that need to be feedback.'})
    @feedback_api.doc(responses={
        200:'User successfully feebacked.',
        401:"Please upload file.",
        402:"No selected file.",
        403:"Error file type.",
    })
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """ 
            Feedback function of grapevine leaf, this function can invoke by any clients based on restful api. 
            It recieves a image that clients need to store for future training. 
            It response a successful storage of fedback image. 
        
        """
        # get the post data
 
        app.logger.info('successfully invoke disease feedback %s %s', "post", len(request.files))
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
    
        app.logger.info('successfully invoke Disease Feedback %s %s', "post", file.filename)

        # Avoid duplicate in the folder (prior to saving the file)
        def uniquify(file_path):
            filename, extension = path.splitext(file_path) 
            counter = 1
            while path.exists(file_path):
                file_path = filename+"("+str(counter)+")"+extension
                counter += 1
            return file_path

        # Disease varieties
        varieties = ['Black Rot','Black Measles','Healthy','Isariopsis']

        # Check the prefix of filename to categorize the feedbacked image
        def CheckCategory(file_path):
            for type in varieties:
                if file_path.split('_')[0].find(type)>=0:
                    category = type
                    break
                else:
                    category = 'Unknown'
            return category

        # Save new incoming image file to dedicated folder and return full path
        def SaveFile(n_filename):
            category = CheckCategory(n_filename)
            file_path = basedir+'/uploads/feedback/'+category+'/'+n_filename # or secure_filename(n_filename)
            file_path = uniquify(file_path)
            file.save(file_path)
            Image.open(file_path).convert('RGB').save(file_path)
            return file_path

        # Save file
        file_path = SaveFile(file.filename)
        
        response_object = {
            "code":"200",
            "message":"Feedback storage complete.",
            "data": [
                {'Feedback Path': file_path}
            ] 
        }
        return response_object, 200