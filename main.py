from random import randint, seed
import hashlib

from flask import Flask, render_template, request, \
    make_response, redirect, url_for
from models import User, db

import uuid

db.create_all()

app = Flask(__name__)


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login_post", methods=["POST"])
def login_post():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    password = hashlib.sha512(password.encode()).hexdigest()
    print(password)
    user = db.query(User).filter_by(email=email).first()
    if user is not None:
        if user.password != password:
            return "<h1>Wrong password</h1>"
    else:
        user = User(name=name, email=email,
                    secret_number=randint(0, 10),
                    password=password,
                    token=str(uuid.uuid4()))
        db.add(user)
        db.commit()

    response = make_response(
        redirect(url_for("index"))
    )
    response.set_cookie("token", user.token)
    return response


@app.route("/")
def index():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response
    print(user.email, user.name)
    return render_template("ugibanje.html")


@app.route("/", methods=["POST"])
def index_post():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response
    vpisana = int(request.form.get("ugibanje"))
    uganil = False
    if vpisana > user.secret_number:
        message = "Ugibana številka je prevelika"
    elif vpisana == user.secret_number:
        uganil = True
        message = "Ugibana številka je pravilna"
    else:
        message = "Ugibana številka je premajhna"
    return render_template("rezultat_ugibanja.html",
                           message=message, uganil=uganil)

@app.route("/reset")
def reset():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response

    user.secret_number = randint(0, 100)
    print(user.secret_number)
    db.add(user)
    db.commit()

    response = make_response(
        redirect(url_for("index"))
    )
    return response


@app.route("/profile/")
def profile_view():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response

    return render_template("profile.html", user=user)

@app.route("/profile/edit", methods=["GET"])
def profile_edit_get():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response

    return render_template("edit.html", user=user)

@app.route("/profile/edit", methods=["POST"])
def profile_edit_post():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response

    # Popravimo
    user.email = request.form.get("email")
    user.name = request.form.get("name")
    # db.delete(user)
    # Shranimo v bazo
    db.add(user)
    db.commit()

    return render_template("edit.html", user=user)

@app.route("/profile/delete", methods=["POST"])
def profile_delete_post():
    token = request.cookies.get("token")
    user = db.query(User).filter_by(token=token).first()
    if user is None:
        response = make_response(
            redirect(url_for("login_get"))
        )
        return response

    db.delete(user)
    db.commit()

    return make_response(
            redirect(url_for("index"))
        )

@app.route("/list", methods=["GET"])
def list_users():
    users = db.query(User).all()

    return render_template("list_users.html",
                    users=users)

if __name__ == '__main__':
    app.run()
