#basic flask and REST api framework
from flask import Flask
from flask_restful import reqparse, abort, Resource, Api

#used to authenticate a request
from flask_httpauth import HTTPBasicAuth

#used to interact with postgres
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#specify what database we'll be interacting with. Should we hard-code this? No.
db_string = 'postgresql+psycopg2://$USER_NAME:$PASSWORD@$DOMAIN.$TLD:5432/$DB_NAME'
db = create_engine(db_string)
base = declarative_base()


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

#used for authentication. Should we hard-code this? No.
USER_DATA = {
"$AUTHENTICATED_USERNAME" : "$AUTHENTICATED_PASSWORD"
}

#defines how we check for authenticated request.
@auth.verify_password
def verify(username,password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password



#used to parse the REST information. These are paramters we expect to receive in.
parser = reqparse.RequestParser()
parser.add_argument('location')
parser.add_argument('temperature',type = float)
parser.add_argument('pressure', type = float)
parser.add_argument('humidity', type = float)
parser.add_argument('wetness', type = float)





#Defines out interactions for the REST api. Both require authentication.
#A post request is first authenticated, then parsed, and then the prased values are inserted into the SQL database we made earlier.
#Note that the REST API is authenticating the incoming https request, but then the SQL database is again authenticating to make sure the process has made a valid conenction (defined above in the connection string). Furthermore, it'll make sure the user is eligible for commands like INSERT.
class SQL_Interaction(Resource):
    @auth.login_required
    def get(self):
        return {'message':'Feel free to interact, if you know how'},201
    @auth.login_required
    def post(self):
        args = parser.parse_args()
        humidity = args['humidity']
        temperature = args['temperature']
        pressure = args['pressure']
        wetness = args['wetness']
        location = args['location']
        db.execute("INSERT INTO esp32data (temperature, humidity, pressure, wetness, location) VALUES ({},{},{},{},'{}')".format(temperature, humidity, pressure, wetness, location))

        return 201


api.add_resource(SQL_Interaction,'/SQL_API/')


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
