from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated user database with address
users = {
    "john123": {"password": "abc123", "address": "10 Woodlands Ave"},
    "alice": {"password": "pass456", "address": "5 Clementi Rd"}
}

sessions = {}  # Temporary store to track logged-in users

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    parameters = req['queryResult']['parameters']
    session_id = req['session']

    # LoginIntent
    if intent == 'LoginIntent':
        username = parameters.get('username')
        password = parameters.get('password')
        if username in users and users[username]['password'] == password:
            sessions[session_id] = username  # Save login state
            return jsonify({"fulfillmentText": f"✅ Login successful. Welcome, {username}!"})
        else:
            return jsonify({"fulfillmentText": "❌ Invalid username or password. Please try again."})

    # UpdateAddress
    elif intent == 'UpdateAddress':
        if session_id not in sessions:
            return jsonify({"fulfillmentText": "🔒 Please log in first. What is your username?"})
        else:
            return jsonify({"fulfillmentText": "✅ You are logged in. Please enter your new address."})

    # CaptureNewAddress
    elif intent == 'CaptureNewAddress':
        new_address = parameters.get('address')
        username = sessions.get(session_id)
        if username:
            users[username]['address'] = new_address
            return jsonify({"fulfillmentText": f"📍 Address updated to: {new_address} for user {username}."})
        else:
            return jsonify({"fulfillmentText": "❌ Please log in before updating address."})

    return jsonify({"fulfillmentText": "Unhandled intent."})

if __name__ == '__main__':
    app.run()
