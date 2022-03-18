from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt,os,datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'DBSTARKGARIN.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "STARKPHBDONE"

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
db.create_all()

class Register(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"Pesan ":"Berhasil Mendaftar"}), 200)
        return jsonify({"Pesan ":"Username/Password tidak boleh KOSONG"})

class Login(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            
            return make_response(jsonify({"HELLO " : dataUsername}), 200)
        return jsonify({"Pesan ":"Login Gagal"}) 

class info(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"A. Username": dataUsername,"B. Password": dataPassword,"C. Token API":token}), 200)
        return jsonify({"Pesan ":"Mengambil Info Gagal, Login Dahulu"}) 

api.add_resource(Register, "/api/v1/register", methods=["POST"])
api.add_resource(Login, "/api/v1/login", methods=["POST"])
api.add_resource(info, "/api/v2/users/info", methods=["POST"])

if __name__ == "__main__":
    app.run(port=4000, debug=True)

