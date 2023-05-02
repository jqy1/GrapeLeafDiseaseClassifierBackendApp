import io
import unittest
import json
from base import BaseTestCase
import base64
from pathlib import Path
import os




basedir = os.path.abspath(os.path.dirname(__file__))





def get_authToken(self):
    """get the correct token when logging in"""
    response = self.client.post(
        '/api/v1/auth/login',
        data = json.dumps( 
            dict(
                email =  "cun.lyu@gmail.com",
                password =  "Cun#2022s2",
            )
        ),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    auth_token = data['data']['Authorization']
    return auth_token


def test_predict_function(self, auth_token):
    # with open('static/images/grapevine/test_2.jpg') as test:
    #         imgStringIO = StringIO(test.read())
    auth_token = get_authToken(self)
    with open('/csse/users/jyu28/Desktop/COSC680/cosc680-backend/app/static/images/grapevine/test_2.jpg', "rb") as img:
        string = base64.b64encode(img.read()).decode('utf-8')

    with open('/csse/users/jyu28/Desktop/COSC680/cosc680-backend/app/static/images/grapevine/test_2.jpg', 'rb') as img1:
        imgStringIO1 = io.BytesIO(img1.read())

        test_path = Path(__file__).parent/ "resources"

        data = {
            "file":(img1, 'test.pdf'),
            'key' :"ok"
        }

        return self.client.post(
            '/api/v1/predict/',
            headers=dict(
                Authorization=auth_token,
            ),
            data=data,
            buffered=True,
            content_type='multipart'
        )


class TestPredictApi(BaseTestCase):
    def test_predict_function(self):
        """ Test for predict functionality """
        auth_token = get_authToken(self)
        with self.client:
            response = test_predict_function(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            



if __name__ == '__main__':
    unittest.main()