from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated user database
users = {
    "john123": "abc123",
    "alice": "pass456"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    
    if intent == 'LoginIntent':
        parameters = req['queryResult']['parameters']
        username = parameters.get('username')
        password = parameters.get('password')

        if username in users and users[username] == password:
            return jsonify({"fulfillmentText": f"✅ Login successful. Welcome, {username}!"})
        else:
            return jsonify({"fulfillmentText": "❌ Invalid username or password. Please try again."})

    return jsonify({"fulfillmentText": "Unhandled intent."})

if __name__ == '__main__':
    app.run(port=5000)
