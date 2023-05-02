import re

def validate_password(password:str):
    """ 
    validate the input password 
    1. Minimum 8 characters.
    2. The alphabet must be between [a-z]
    3. At least one alphabet should be of Upper Case [A-Z]
    4. At least 1 number or digit between [0-9].
    5. At least 1 character from [ @ # $ % ^ & + = _ ].

    :param password: The string of a new password that need to be validated.

    
    """
  

    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=_]{8,}', password):
        # match
        return True
    else:
        # no match
        return False

    return False


def validate_mail(email:str):
    """ 
    validate the input email address 

    :param password: The email address that need to be validated.

    """

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

    return False

def validate_parameter( valdate_param, regex_express ):
    """ 
    validate the input parameter, we check the policy as below:
    1. Empty
    2. if giving regex_express, the valdate_value must be accepted by regex validation 


    :param valdate_param: The parameter name in the json object.
    :param valdate_value:
    """

    if not valdate_param:
        return False
    
    if len(str(valdate_param)) == 0:
        return False
    
    if not regex_express and len(regex_express)>0:
        if(re.fullmatch(regex, email)):
            return True
        else:
            return False


    return False