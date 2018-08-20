import os

import constants as C

from datetime import timedelta

from flask import Flask, redirect, send_from_directory, session, render_template, request, flash, make_response, jsonify
from flask_restplus import Api, Resource, fields, reqparse

from utils import get_unique_id, logger
from carpenter import *


logger = logger(os.path.basename(__file__))


#Flask Server
app = Flask(__name__)
app.secret_key = C.SECRET_KEY

# flask restplus service
api = Api(app, version='1.0', title='POC',\
    description='API', doc='/')

ns = api.namespace('api', description='Restful operations')

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

device_data = reqparse.RequestParser()
device_data.add_argument('device_name', required=True, help='device name')
device_data.add_argument('user_id', required=True, help='user name')
device_data.add_argument('organization', required=False, help='organization name')

delete_device_data = reqparse.RequestParser()
delete_device_data.add_argument('device_name',required=True, help='device name', location='args')
delete_device_data.add_argument('user_id',required=True, help='user name', location='args')
delete_device_data.add_argument('transaction_id',required=True, help='Transaction Id', location='args')


@ns.route('/<string:customer_type>/add_device')
class AddDevice(Resource):
    @ns.doc('Api to Add DEvice')
    @ns.expect(device_data)
    def post(self, customer_type):
        '''
        API to ADD USER
        '''
        logger.info("Made an API POST call on AddDevice")
        # try:
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
        if user_id:
            result = add_device(device_name=device_name, organization=organization,\
                                user_id=user_id, transaction_id=transaction_id)
        if result:
            logger.info("API POST call responded on AddDevice")
            return jsonify({'status': 'success'})
        raise Exception('Device Not added')
        # except Exception as e:
        #     logger.error("Failed to return AddDevice - {e}".format( e=e))
        #     return jsonify({'status': 'fail'})

@ns.route('/delete_device')
class DeleteDevice(Resource):
    @ns.doc('Api to Add DEvice')
    @ns.expect(delete_device_data)
    def delete(self):
        '''
        API to delete USER
        '''
        logger.info("Made an API POST call on DeleteDevice")
        try:
            args = api.payload
            device_name = args.get('device_name')
            transaction_id = args.get('transaction_id')
            user_id = args.get('user_id')
            if user_id:
                result = delete_device_user(user_id=user_id, device_name=device_name, transaction_id=transaction_id)
            if result:
                logger.info("API POST call responded on DeleteDevice")
                return jsonify({'status': 'success'})
            raise Exception('Failed to Delete a Device')
        except Exception as e:
            logger.error("Failed to return DeleteDevice - {e}".format( e=e))
            return jsonify({'status': 'fail'})


@ns.route('/add_user')
class AddUser(Resource):
    @ns.doc('Api to Add User')
    @ns.expect(user_data)
    def post(self):
        '''
        API to add USER
        '''
        logger.info("Made an API POST call on AddUser")
        try:
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
            result = add_user(fullName=fullName, user_id=userId, emailAddress=emailAddress,\
                            companyName=companyName, phoneNumber=phoneNumber, country=country,\
                            address=address, city=city, state=state, postCode=postCode)
            if result:
                logger.info("API POST call responded on AddUser")
                return jsonify({'status': 'success'})
            raise Exception('User Already Exists')
        except Exception as e:
            logger.error("Failed to return AddUser - {e}".format( e=e))
            return jsonify({'status': 'fail'})

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',
          port=5000)