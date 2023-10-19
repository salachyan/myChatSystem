from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234askdfbjh"
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
                code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
            
    return code

@app.route("/", methods=["POST","GET"])

def home():
    session.clear()
    if request.method == "POST":

        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please Enter a Name.", code=code,name=name)
        
        if not code and join != False:
                        return render_template("home.html", error="Please Enter a Room Code.",code=code,name=name)

        room = code

        if create != False:
              room = generate_unique_code(4)
              rooms[room] = {"members":0 , "messages":[]}

        elif code not in rooms:
            return render_template("home.html", error="Room does not Exist.", code=code,name=name)

        session["room"] = room
        session["name"] = name


    return render_template("home.html")


if __name__ == "__main__":
    socketio.run(app,debug=True)