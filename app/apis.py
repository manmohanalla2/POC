import os

import constants as C

from datetime import timedelta

from flask import Flask, redirect, send_from_directory, session, render_template, request, flash, make_response
from flask_restplus import Api, Resource, fields

from utils import get_unique_id, logger
from carpenter import *


logger = logger(os.path.basename(__file__))


#Flask Server
app = Flask(__name__)
app.secret_key = C.SECRET_KEY

# flask restplus service
api = Api(app, version='1.0', title='POC',\
    description='API', doc='/', base_url='/api')

ns = api.namespace('', description='Restful operations')

user_data = api.model('json_format',{
    'fullName' : fields.String(description='Full Name'),
    'emailAddress' : fields.String(description='Email Address'),
    'companyName' : fields.String(description='Company Name If Any'),
    'phoneNumber' : fields.String(description='Phone Number'),
    'country' : fields.String(description='Country'),
    'address' : fields.String(description='Address'),
    'city' : fields.String(description='City'),
    'state' : fields.String(description='State'),
    'postCode' : fields.String(description='Post Code')
})

device_data = api.model('json_format',{
    'device_name': fields.String(required=True, description='device name'),
    'user_id': fields.String(required=True, description='user name'),
    'organization': fields.String(required=False, description='organization name')
})

delete_device_data = api.model('json_format',{
    'device_name': fields.String(required=True, description='device name'),
    'user_id': fields.String(required=True, description='user name'),
    'transaction_id': fields.String(required=True, description='Transaction Id')
})


@ns.route('/<string:customer_type>/add_device')
class AddDevice(Resource):
    @ns.doc('Api to Add DEvice')
    @ns.marshal_with(device_data)
    def post(self, customer_type):
        '''
        API to ADD USER
        '''
        logger.info("Made an API POST call on AddDevice")
        args = api.payload
        device_name = args.get('device_name')
        organization = args.get('organization')
        user_id = args.get('user_id')
        transaction_id = get_unique_id()
        if not C.CUSTOMER_TYPES.get(customer_type):
            raise Exception('Not a Valid Customer')
        if C.CUSTOMER_TYPES.get(customer_type) == C.CUSTOMER_TYPES['organization']:
            if not organization:
                raise Exception('Please Enter the Organisation Name')
        device_info = get_device_info(device_name=device_name)
        if not device_info:
            raise Exception('Device Not Found')
        try:
            if user_id:
                result = add_device(device_name=device_name, organization=organization,\
                                    user_id=user_id, transaction_id=transaction_id)
            if result:
                logger.info("API POST call responded on AddDevice")
                return {'status': 'success'}, 201
            raise Exception('Device Not added')
        except Exception as e:
            logger.error("Failed to return AddDevice - {e}".format( e=e))
            return {'status': 'fail'}, 200

@ns.route('/delete_device')
class DeleteDevice(Resource):
    @ns.doc('Api to Add DEvice')
    @ns.marshal_with(delete_device_data)
    def delete(self):
        '''
        API to delete USER
        '''
        logger.info("Made an API POST call on DeleteDevice")
        args = param_parser.parse_args()
        param = args.get('device_name')
        transaction_id = args.get('transaction_id')
        user_id = args.get('user_id')
        try:
            if user_id:
                result = delete_device_user(user_id=user_id, device_name=device_name, transaction_id=transaction_id)
            if result:
                logger.info("API POST call responded on DeleteDevice")
                return {'status': 'success'}, 201
            raise Exception('Failed to Delete a Device')
        except Exception as e:
            logger.error("Failed to return DeleteDevice - {e}".format( e=e))
            return {'status': 'fail', 'message': e}, 200


@ns.route('/add_user')
class AddUser(Resource):
    @ns.doc('Api to Add User')
    @ns.marshal_with(user_data)
    def post(self):
        '''
        API to add USER
        '''
        logger.info("Made an API POST call on AddUser")
        args = api.payload
        fullName = args.get('fullName')
        userId = get_unique_id()
        emailAddress = args.get('emailAddress')
        companyName = args.get('companyName')
        phoneNumber = args.get('phoneNumber')
        country = args.get('country')
        address = args.get('address')
        city = args.get('city')
        state = args.get('state')
        postCode = args.get('postCode')
        try:
            result = add_user(fullName=fullName, userId=userId, emailAddress=emailAddress,\
                            companyName=companyName, phoneNumber=phoneNumber, country=country,\
                            address=address, city=city, state=state, postCode=postCode)
            if result:
                logger.info("API POST call responded on AddUser")
                return {'status': 'success'}, 201
            raise Exception('User Already Exists')
        except Exception as e:
            logger.error("Failed to return AddUser - {e}".format( e=e))
            return {'status': 'fail', 'message': e}, 200

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',
          port=5000)