import unittest
import json
from base import BaseTestCase

def test_register_user(self):
    return self.client.post(
        '/api/v1/user/',
        data = json.dumps( 
            dict(
                first_name = "test",
                sur_name =  "Lyu",
                mail = "test.lyu@gmail.com",
                password_hash =  "Lyu#2022s2",
                registered_on =  "",
                admin =  "0",
                public_id =  "",
                user_level =  "Normal",
                user_name =  "Lyu"
            )
        ),
        content_type='application/json'
    )


def test_login_user(self):
    return self.client.post(
        '/api/v1/auth/login',
        data = json.dumps( 
            dict(
                email =  "test.lyu@gmail.com",
                password =  "Lyu#2022s2",
            )
        ),
        content_type='application/json'
    )

def test_not_registered_login_user(self):
    return self.client.post(
        '/api/v1/auth/login',
        data = json.dumps( 
            dict(
                email =  "test.lyu1@gmail.com",
                password =  "Lyu#2022s2",
            )
        ),
        content_type='application/json'
    )

def test_logout_user(self, auth_token):
    return self.client.post(
        '/api/v1/auth/logout',
        headers=dict(
            Authorization=auth_token
        ),
        content_type='application/json'
    )

class TestAuthRextApi(BaseTestCase):
    def test_register_user(self):
        """ Test for user registration """
        with self.client:
            response = test_register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['code'] == 200)
            self.assertTrue(data['data']['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_register_with_already_registered_user(self):
        """ Test for registeration based on a already registered user """
        response = test_register_user(self)
        with self.client:
            response = test_register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['code'] == 201)
            self.assertTrue(data['message']=="Already exist, please login in or reset new password")
            self.assertTrue(data['data']['Authorization']=='fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login(self):
        """ Test for a registered user login"""
        response = test_register_user(self)
        with self.client:
            response = test_login_user(self)
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['message']=="Successfully logged in.")
            self.assertTrue(data['data']['Authorization']!='fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registed_user_login(self):
        """ Test for a not registered user who try to login """
        with self.client:
            response = test_not_registered_login_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(data['code'], 401)
            self.assertTrue(data['message']=="user is not exist")
            self.assertTrue(data['data']['Authorization']=='fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            #1 register a new user
            response = test_register_user(self)
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['code'] == 200)
            self.assertTrue(data['data']['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            #2 login operation
            response = test_login_user(self)
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['message']=="Successfully logged in.")
            self.assertTrue(data['data']['Authorization']!='fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            #3 logout operation
            auth_token = data['data']['Authorization']
            response = test_logout_user(self,auth_token)
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['message']=="Successfully logout.")
            #self.assertTrue(data['data']['Authorization']=='None')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


    


if __name__ == '__main__':
    unittest.main()