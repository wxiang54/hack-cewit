from app import app, api
from flask import request, url_for
from flask_restful import Resource, reqparse
from utils import dbUtils, authUtils, apiUtils
import json

with open('data/code_msgs.json') as msgs:
    CODE_MSGS = json.loads(msgs.read())
    
class User(Resource):
    def get(self, email):
        return {email: dbUtils.get_user(email)}

class VCardUser(Resource):
    def get(self, email):
        return dbUtils.get_vcards_by_email(email)
    def post(self, email):
        user_cc_token = dbUtils.get_user(email)['cctoken']
        charge = apiUtils.charge_card_by_token(user_cc_token, request.form.get('limit'))
        if not charge["result"]["status"] == "Authorized":
            return charge
        dbUtils.register_new_vcard(email, \
                                   request.form.get('limit'), \
                                   request.form.get('name'))
        return charge
        #UI should redirect to GET view
        
class VCardView(Resource):
    def get(self, email, referenceID):
        apiUtils.get_vcard_by_refID(referenceID)

    
class Register(Resource):
    def post(self):
        authCode = authUtils.add_user(
            request.form.get('fullname'),\
            request.form.get('email'),\
            request.form.get('password'))
        ret = {"message": CODE_MSGS["register"][str(authCode)]}
        if not authCode: #successful!
            ret["status"] = "success"
            ret["user"] = dbUtils.get_user(request.form.get('email'))
            return ret, 200
        else:
            ret["status"] = "error"
            return ret, 400

    def post(self, email): #adding a token to their acc
        ret = apiUtils.tokenize(ccrm, apiUtils.request_token())
        if ret["status"] == "Authorized":
            dbUtils.tie_token_to_user(ret["token"], email)
        return ret

            
class Login(Resource):
    def post(self):
        authCode = authUtils.verify_user(
            request.form.get('email'),\
            request.form.get('password'))
        ret = {"message": CODE_MSGS["login"][str(authCode)]}
        if not authCode: #successful
            ret["status"] = "success"
            ret["user"] = dbUtils.get_user(request.form.get('email'))
            return ret, 200
        else:
            ret["status"] = "error"
            return ret, 400

    
api.add_resource(User, '/user/<string:email>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(VCardUser, '/user/<string:email>/vcard')
api.add_resource(VCardView, '/user/<string:email>/vcard/<string:refID>')
