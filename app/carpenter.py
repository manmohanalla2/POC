
from db_collections import DB

from functools import wraps

def get_db_connection(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        db = DB()
        kwargs['db'] = db
        r = f(*args, **kwargs)
        return r
    return wrapped


@get_db_connection
def add_user(db, **form_args):
    '''
    adding user info
    '''
    result = db.get_user_info(email_address=form_args['emailAddress'])
    if result:
        return False
    db.add_user_info(data=form_args)
    return True


@get_db_connection
def add_device(device_name, user_id, transaction_id, organization=None):
    '''
    adding device
    '''

    result = db.add_device(deviceName=device_name, userId=userId, transaction_id=transaction_id, companyName=organization)
    return result


@get_db_connection
def delete_device_user(user_id, device_name, transaction_id):
    '''
    delete device
    '''
    result = db.delete_device(user_id=user_id, device_name=device_name, transaction_id=transaction_id)
    return result

@get_db_connection
def get_device_info(device_name):
    '''
    get device Info
    '''
    result = db.device_info(device_name=device_name)
    return result



@get_db_connection
def get_organisations(device_name):
    '''
    get device Info
    '''
    result = db.organations_lst(device_name=device_name)
    return result
