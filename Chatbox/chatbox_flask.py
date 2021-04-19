import uuid
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_session import Session
# from bot import botmes
# from sessionManager import sessionManage, newSession, newSessionTwo

# from Chatbox.sessionManager import sessionManage, newSession

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/tutorial", methods=["GET", "POST"])
def tutorial():
    actionList = [{"name":"pointAt", "args":"aspirin"}, {"name":"pointAt", "args":"monday noon"}]
    hintList = ["first click on an aspirin pill to grab", "now click on the highlighted position on a calendar to drop the pill"]

    if request.method == "POST":
        pos = int(request.form["position"])
        response = request.form["response"]
        print(response)
        proceed = False

        if "remove_from_container aspirin" in response or "add_to_grid" in response:
            print("proceed")
            proceed = True

        if pos < len(actionList):
            output = {"action":actionList[pos], "hint":hintList[pos], "proceed":proceed}
        else:
            output = None
        return jsonify(output)

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        print(request.form["botm"])
        message = request.form["botm"]
        action = {}
        hint = ""
        start = ""
        state = "speaking"
        time_mapping = ["none", "morning", "noon", "afternoon", "evening"]
        day_mapping = {"mon":"Monday", "tue":"Tuesday", "wed":"Wednesday", "thu":"Thursday", "fri":"Friday",
"sat":"Saturday", "sun":"Sunday"}

        def numCheck():
            print(session.get("calendar_count"))
            for position, medCount in session.get("calendar_count").items():
                for med, count in medCount.items():
                    if count > 2:
                        return (med, position, count)
            return None
        
        def interactionCheck():
            for position, medCount in session.get("calendar_count").items():
                if "ibuprofen" in medCount and "aspirin" in medCount and medCount["ibuprofen"] + medCount["aspirin"] > 1:
                    return position
            return None
        
        if "hello" in message:
            start = "hello"
        elif "bye" in message or "goodbye" in message:
            state = "sleeping"
            start = "goodbye!"
        elif "thank you" in message:
            start = "you are welcome!"
        elif "add_to_grid" in message:
            messageList = message[1:-1].split(" ")
            med = messageList[1]
            position = messageList[2][:3].lower() + str(time_mapping.index(messageList[-1]))
            if position not in session.get("calendar_count"):
                session.get("calendar_count")[position] = {med: 1}
            else:
                if med in session.get("calendar_count")[position]:
                    session.get("calendar_count")[position][med] += 1
                else:
                    session.get("calendar_count")[position][med] = 1

            if med == "ibuprofen" and messageList[-1] == "morning":
                hint = "ibuprofen should not be used in the morning"
                action = {"name":"pointAt", "args": messageList[2] + " " + messageList[-1]}
            else:
            # check if there are no position with more than 2 pills of any type
                overdose = numCheck()
                if overdose != None:
                    day = day_mapping[overdose[1][:3]]
                    time = time_mapping[int(overdose[1][-1])]
                    hint = "too many " + overdose[0] + " on " + day + " " + time
                    action = {"name":"pointAt", "args":day + " " + time}
                else:
                    incompatible = interactionCheck()
                    if incompatible != None:
                        hint = "ibuprofen and aspirin should not be used together"
                        day = day_mapping[incompatible[:3]]
                        time = time_mapping[int(incompatible[-1])]
                        action = {"name":"pointAt", "args":day + " " + time}
                
        elif "remove_from_grid" in message:
            messageList = message[1:-1].split(" ")
            med = messageList[1]
            position = messageList[2][:3].lower() + str(time_mapping.index(messageList[-1]))
            session.get("calendar_count")[position][med] -= 1

        output = {"start": start, "action": action, "hint": hint, "state":state, "userInput":message}
        return jsonify(output)


@app.route('/', methods=['GET'])
def chatbox():
    # session.pop('user', None)
    # session['user'] = uuid.uuid4()
    # if "calendar_count" not in session:
    session["calendar_count"] = {}
        

    if "events" not in session:
        session["events"] = [{"name": "exercise", "day": "mon", "time":"1"}, {"name":"appointment", "day":"thu", "time":"2"},
                {"name":"work", "day":"sat","time":"3"}]
    
    if "medications" not in session:
        session["medications"] = [{"name":"ibuprofen", "color":"red", "number":"11"}, {"name":"aspirin", "color":"blue", "number":"15"},
    {"name":"albuterol", "color":"green", "number":"7"}]

    # create session, initialize and start the game
    return render_template('index.html', events=session.get("events"), medications=session.get("medications"))

#Session Manager
# @app.route('/processOne', methods=['GET', 'POST'])
# def processOne():
# # Session Manager
# # @app.route('/process', methods=['GET', 'POST'])
# # def process():
#     userm = request.form['botm']
#     botm = sessionManage(userm, session['user'])
#     state = botm['state']
#     hint = botm['hint']

#     return jsonify(botm)

# @app.route('/processTwo', methods=['GET', 'POST'])
# def processTwo():
#     print ("process two being called")
#     message = newSessionTwo(session['user'])
#     output = {'start': message}
#     print (message)
#     return jsonify(output)


# initializes the game at the beginning
@app.route('/startgame', methods=['GET', 'POST'])
def startgame():
    # message = newSession(session['user'])
    message = "Hello, what would you like to do?"
    output = {'start': message}
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
