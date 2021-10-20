import flask
from flask import request, jsonify
from datetime import datetime

import os
from flask_sqlalchemy import SQLAlchemy

# create flask object and set configuration
app = flask.Flask(__name__)

app.config["DATE_FORMAT"] = "%Y-%m-%d"
if os.environ.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # create SQLAlchemy object
    db = SQLAlchemy(app)
else:
    raise OSError('Please provide SQLALCHEMY_DATABASE_URI environment value')

# db.model class definition for SQLAlchemy - it will create table when called
class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   birthdate = db.Column(db.Date, nullable=False)

# route for flask method GET path /hello/<username>
@app.route('/hello/<username>', methods=['GET'])
def get_hello(username):
    # check if all symbols are letters, else return error
    if username.isalpha():
        try:
            # query for user by username, if not present user = None
            user = Users.query.filter_by(username=username).first()
            if(user):
                # get today's date
                now = datetime.now()
                # changing user's birtdate year to this year, in order to compare days
                formatted_birthday = datetime(now.year, user.birthdate.month, user.birthdate.day)
                # calculating days between user's birtdate and today
                days_to_birthday=abs( ( now.today() - formatted_birthday).days )

                # if days more than 0 return message with days ti birtdate
                if(days_to_birthday == 0):
                    return jsonify(
                        message="Hello, {}! Happy birthday!".format(username)
                    )
                # if days is equal to 0 greet user
                else:
                    return jsonify(
                        message="Hello, {}! Your birthday is in {} day(s)".format(username, days_to_birthday)
                    )
                   
               
            # if user = None return error that user doesn't exist with http code = 400 Bad request
            else:
                return ({"error": "username {} is not presented".format(username)}, 400)
        # if code throws an exception return error with http code = 400 Bad request
        except (Exception) as error:
            print(error)
            return ({"error": "something went wrong"}, 400)
    # if username contains something except letters return error with http code = 400 Bad request
    else:
        return ({"error": "username must contain only letters"}, 400)

@app.route('/hello/<username>', methods=['PUT'])
def put_hello(username):
    # check if all symbols are letters, else return error
    if not username.isalpha():
        # if username contains something except letters and return error with http code = 400 Bad request
        return ({"error": "username must contain only letters"}, 400)

    # check if Content-type is application/json
    if not request.headers.get('Content-Type') == 'application/json':
        # check if request body is json
        # if request body is not json formatted return error with http code 400
        return ({"error": "header 'Content-Type' should be application/json"}, 400)
    
    if request.is_json:
        try:
            # get dateOfBirth from request body
            dateofbirth=datetime.strptime(request.get_json()['dateOfBirth'], app.config["DATE_FORMAT"])
            # check if dateOfBirth doesn't exceed today
            if dateofbirth > datetime.now():
                # return that date must not exceed today with http code 400
                return ({"error": "date must not exceed today"}, 400)
            
            # query table by username
            user = Users.query.filter_by(username=username).first()
            # if user is not None, update birthdate and commit
            if user:
                user.birthdate = dateofbirth
                db.session.commit()
                return ('', 204)
            # if user is None, it means that we need to create user
            else:
                user = Users(username=username, birthdate=dateofbirth)
                db.session.add(user)
                db.session.commit()
                return ('', 204)
            
        # if there is an exception return error with http code 400
        except (Exception) as parseError:
            print(parseError)
            return ({"error": "parsing error: {}".format(parseError)}, 400)

    else:
        return ({"error": "body of PUT request should be json-formatted"}, 400)             
    # if Content-type header is not application/json return error with http code 400

if __name__ == "__main__":
    app.run(host='0.0.0.0')