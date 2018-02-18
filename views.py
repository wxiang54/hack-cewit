from app import app, api
from flask import request, url_for, flash
from flask_restful import Resource, reqparse
from utils import dbUtils, authUtils, apiUtils
import json

with open('data/code_msgs.json') as msgs:
    CODE_MSGS = json.loads(msgs.read())


class User(Resource):
    def get(self, email):
        return {email: dbUtils.getUserByCol(email)}

class Register(Resource):
    def post(self):
        authCode = authUtils.add_user(
            request.form.get('fullname'),\
            request.form.get('email'),\
            request.form.get('password'))
        ret = {"message": CODE_MSGS["register"][str(authCode)]}
        if not authCode: #successful!
            ret["status"] = "success"
            ret["user"] = dbUtils.getUserByCol(request.form.get('email'))
            return ret, 200
        else:
            ret["status"] = "error"
            return ret, 400

class Login(Resource):
    def post(self):
        authCode = authUtils.verify_user(
            request.form.get('email'),\
            request.form.get('password'))
        ret = {"message": CODE_MSGS["login"][str(authCode)]}
        if not authCode: #successful
            ret["status"] = "success"
            ret["user"] = dbUtils.getUserByCol(request.form.get('email'))
            return ret, 200
        else:
            ret["status"] = "error"
            return ret, 400

    
api.add_resource(User, '/user/<string:email>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')


@app.route('/user', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    code = authUtils.verify_user(email, password)
    if code == 0:
        session["id"] = user["id"]
        if remember:
            user = dbUtils.get_user_by_col(email, 'email');
            print session.permanent
        flash(CODE_MSGS["login"]["0"], 'success')
        return redirect(url_for("index"))
    else:
        flash(CODE_MSGS["login"][str(code)], 'error')
        return redirect(url_for("login"))



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")
    rpassword = request.form.get("rpassword")

    code = authUtils.add_user(fullname, email, password, rpassword)
    if code == 0: #successful registration                                                                    
        flash(Markup(CODE_MSGS["register"]["0"]), 'success')
        return redirect(url_for("login"))
    else:
        flash(Markup(CODE_MSGS["register"][str(code)]), 'error')
        return redirect(url_for("register"))
