import os
import copy

import constants as C

from datetime import datetime
# from dateutil.relativedelta import relativedelta

from pymongo import MongoClient

class DB(object):
	def __init__(self):
		self.db = MongoClient(
		                       C.MONGO_DB_CONNECTION,
		                       authSource=C.DANA_WEB_DATABASE
		                  	)
		self.lightform = self.db.light


	def add_user_info(self, data):
		'''
		adding user info on db
		'''
		self.lightform.users.insert_one(data)
		return True


	def get_user_info(self, email_address):
		'''
		adding user info on db
		'''
		query = {'emailAddress': email_address}
		result = self.lightform.users.find_one(query)
		return result


	def add_device(self, **data):
		'''
		adding user info on db
		'''
		self.lightform.devices.insert_one(data)
		return True


	def device_info(self, device_name):
		'''
		get device Info
		'''
		query = {'deviceName': device_name.lower()}
		result = self.lightform.devices.find_one(query)
		return result


	def get_transaction_info(self, transaction_id, user_id):
		'''
		adding user info on db
		'''
		query = {'transaction': transaction_id, 'userId': user_id}
		result = self.lightform.transactions.find_one(query)
		return result


	def delete_device(self, user_id, device_name, transaction_id):
		'''
		adding user info on db
		'''
		default_data = {'deviceName' : device_name, 'userId': user_id, 'transaction': transaction_id}
		data = self.device_info(transaction_id, user_id)
		if not data:
			return False
		data['DeviceDeleted'] = str(datetime.utcnow())
		data = {'$set': data}
		self.pydana.transactions.update_one(default_data, data)
		return True


	def organizations_lst(self, device_name):
		'''
		get organization Info
		'''
		query = {}
		result = self.lightform.users.find_one(query, {"companyName" : 1})
		return result
