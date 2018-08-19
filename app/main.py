import os

import constants as C

from datetime import timedelta

from flask import Flask, redirect, send_from_directory, session, render_template, request, flash, make_response

from utils import get_unique_id, logger
from carpenter import *

logger = logger(os.path.basename(__file__))

#Flask Server
app = Flask(__name__)
app.secret_key = C.SECRET_KEY

@app.route('/', methods=['POST', 'GET'])
def register():
	response = render_template('register.html')
	if request.method == 'GET':
		return response
	if request.method == 'POST':
		logger.error(request.form)
		fullName = request.form.get('f_name')
		emailAddress = request.form.get('email')
		if not fullName and emailAddress:
			flash('Error: Please Check the Form')
			return response
		userId = get_unique_id()
		companyName = request.form.get('c_name')
		phoneNumber = request.form.get('tel')
		country = request.form.get('country_name')
		address = request.form.get('address')
		city = request.form.get('city')
		state = request.form.get('state')
		postCode = request.form.get('postcode')
		result = add_user(fullName=fullName, userId=userId, emailAddress=emailAddress,\
							companyName=companyName, phoneNumber=phoneNumber, country=country,\
							address=address, city=city, state=state, postCode=postCode)
		if not result:
			flash('Error: User with same Email Address Exists. ')
			return response
		return redirect('/api')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',
          port=5000)