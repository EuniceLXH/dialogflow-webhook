from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database
users = {
    "john123": {"password": "abc123", "address": "123 Yishun Ave 6"},
    "alice": {"password": "pass456", "address": "456 Bishan St 22"}
}

sessions = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    params = req['queryResult'].get('parameters', {})
    session_id = req['session']

    if intent == 'UpdateAddress':
        # Start the flow by asking for username
        return jsonify({"fulfillmentText": "🔒 Please log in first. What is your username?"})

    elif intent == 'CaptureUsername':
        username = params.get('username')
        if username in users:
            sessions[session_id] = {"username": username}
            return jsonify({"fulfillmentText": "Please enter your password"})
        else:
            return jsonify({"fulfillmentText": "❌ Username not found. Please try again."})

    elif intent == 'CapturePassword':
        password = params.get('password')
        username = sessions.get(session_id, {}).get("username")

        if username and users[username]["password"] == password:
            sessions[session_id]["authenticated"] = True
            return jsonify({"fulfillmentText": "✅ Login successful. Please enter your new address"})
        else:
            return jsonify({"fulfillmentText": "❌ Incorrect password. Please try again."})

    elif intent == 'CaptureNewAddress':
        new_address = params.get("address")
        user_session = sessions.get(session_id, {})

        if user_session.get("authenticated"):
            username = user_session.get("username")
            users[username]["address"] = new_address
            return jsonify({"fulfillmentText": f"📍 Address updated to: {new_address} for user {username}"})
        else:
            return jsonify({"fulfillmentText": "❌ Please log in first."})

    # Debug fallback to check intent names received
    return jsonify({"fulfillmentText": f"Unhandled intent: {intent}"})

if __name__ == '__main__':
    app.run()

