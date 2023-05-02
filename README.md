## 1. Install conda 

The backend service can run on Linux, windows, and Mac, and needs python >= 3.5, pip, and pipenv installed.

For Mac: we can use bulitted Python 3.9.X if your MacOSX is over 11.x, the Mac already bulitted python 3 supported.
For Windows: Go to python.

In UC, conda was already installed on all machine, so go to section 2.

```
python --version
# Python 3.9.7

# Install virtualenv
pip install virtualenv

# create env virtualenv env
virtualenv env

# activate virtualenv env
# in mac, just using command source
source env/bin/activate
# in windows, using 
.\env\Scripts\activate 
# Here is a guide for creating env on Windows. 
# https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html

# we might need to change pip by pip3
pip --version
# pip 9.0.1 ... (python 3.X)
# we also need pipenv for creating virtual and independ enviornment of python

pip install pipenv

pipenv --version
```

## 2. Create virtual enviornment by conda
### 2.1 Create conda enviornment
```
conda create -n flask-py39-restx python=3.9
```

### 2.2 Activate the enviornment 
```
conda activate flask-py39-restx
```


## 3. Set up a Flask enviornment for backend system
### 3.1 Install Flask and requirments

We can install all of them by pipenv, or pip, if we use conda then go to section 3.2 
```

# install flask a dependency on our project
pipenv install -r requirements.txt

```
### 3.2 Install requirments

```

# install flask a dependency on our project
pip install -r requirements.txt

```

## 4. Start service
### 4.1 Start service as debug service
A start shell was located on backend, just open terminal in Mac, or Windows ( Windows Command Prompt Commands, Power Shell, and Windows Terminal )
```
cd cosc680-backend
# Start shell (https)
make run

# Start shell (http)
./start-debug.sh
```
#### 4.1.1 If error, update the library locally
```
Open this file: /csse/users/spc47/anaconda3/envs/flask-py39-restx/lib/python3.9/site-packages/flask_script/__init__.py

At the top, change the 'flask._compat' to 'flask_script._compat'
```
### 4.2 Examate the service
### 4.2.1 invoke service states interface
```
curl http://localhost:8080/service/state
```
### 4.2.2 Examate service states result

If you get the following result, it meams all the developement enviornment was created correctly.
```
[
  {
    "code": 200, 
    "data": {
      "enable": true
    }
  }
]
```
## 5 Testing
### 5.1 Start a unit testing
```
cd cosc680-backend
export FLASK_APP=run.py
python run.py test

```


In unit testing, all codes must be put testing codes into app/test folder with prefix test_. The unit testing can automatically load all test python codes. 

## 6 Using pip freeze generated the requirements.txt ( Option )
```
pip freeze > requirements.txt 
```
