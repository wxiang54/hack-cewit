from app import app
from flask import render_template, redirect, request, url_for, flash, Markup, abort, session
from utils import dbUtils, authUtils
import json

with open('data/code_msgs.json') as msgs:
    CODE_MSGS = json.loads(msgs.read())

@app.route('/')
def index():
    print session.permanent
    return render_template("index.html")

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
        flash(Markup(CODE_MSGS["login"]["0"]), 'success')
        return redirect(url_for("index"))
    else:
        flash(Markup(CODE_MSGS["login"][str(code)]), 'error')
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
