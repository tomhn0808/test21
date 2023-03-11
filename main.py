from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import sqlite3


app = Flask(__name__)
jwt = JWTManager(app)

# Making a Connection with MongoClient
conn = sqlite3.connect('users.db')


# JWT Config
app.config["JWT_SECRET_KEY"] = r"DELETED"

def register_user(conn, user):
    sql = ''' INSERT INTO users(first_name,last_name,email,password)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def check_user(conn, email):
    sql = '''SELECT email from users where email == ?'''
    cur = conn.cursor()
    cur.execute(sql, email)
    conn.commit()
    return cur.lastrowid


@app.route("/dashboard")
@jwt_required
def dasboard():
    return jsonify(message="Welcome! to the to-do app!")


# Not working as we moved from mongodb to sqlite
@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    # test = User.query.filter_by(email=email).first()
    test = check_user(email)
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201

# Not working as we moved from mongodb to sqlite
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


if __name__ == '__main__':
    app.run(host="localhost", debug=True)

