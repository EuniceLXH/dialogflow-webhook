from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user database
users = {
    "john123": {"password": "abc123", "address": "123 Yishun Ave 6"},
    "alice": {"password": "pass456", "address": "456 Bishan St 22"}
}

# Dummy order data
orders = {
    "S12345G": {"status": "being processed"},
    "A98765Z": {"status": "shipped"},
    "B54321Q": {"status": "delivered"}
}

# Track user sessions
sessions = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    params = req['queryResult'].get('parameters', {})
    session_id = req['session']

    print(f"[Intent] {intent}")
    print(f"[Params] {params}")

    # Ensure session entry
    if session_id not in sessions:
        sessions[session_id] = {}

    # Address update flow
    if intent == 'UpdateAddress':
        sessions[session_id] = {}  # Clear previous data
        return jsonify({"fulfillmentText": "Please log in first. What is your username?"})

    elif intent == 'CaptureUsername':
        username = params.get('username')
        if username in users:
            sessions[session_id]["username"] = username
            return jsonify({"fulfillmentText": "Please enter your password"})
        else:
            return jsonify({"fulfillmentText": "Username not found. Please try again."})

    elif intent == 'CapturePassword':
        password = params.get('password')
        username = sessions[session_id].get("username")

        if username and users[username]["password"] == password:
            sessions[session_id]["authenticated"] = True
            return jsonify({"fulfillmentText": "Login successful. Please enter your new address"})
        else:
            return jsonify({"fulfillmentText": "Incorrect password. Please try again."})

    elif intent == 'CaptureNewAddress':
        new_address = params.get("address")
        session = sessions.get(session_id, {})

        if session.get("authenticated"):
            username = session.get("username")
            users[username]["address"] = new_address
            return jsonify({"fulfillmentText": f"Address updated to: {new_address} for user {username}"})
        else:
            return jsonify({"fulfillmentText": "Please log in first."})

    # Order status flow
    elif intent == 'CheckOrderStatus':
        order_number = params.get("order_number")
        if order_number in orders:
            status = orders[order_number]["status"]
            return jsonify({"fulfillmentText": f"Your order #{order_number} is currently {status}."})
        else:
            return jsonify({"fulfillmentText": "Invalid order number. Please provide a valid one."})

    # Refund flow
    elif intent == 'RequestRefund':
        order_number = params.get("order_number")
        reason = params.get("refund_reason")
        if order_number in orders:
            return jsonify({
                "fulfillmentText": f"Thanks! We've submitted your refund request for order {order_number} due to \"{reason}\". Our team will contact you within 2 business days."
            })
        else:
            return jsonify({"fulfillmentText": "Invalid order number. Please provide a valid one."})

    return jsonify({"fulfillmentText": f"Unhandled intent: {intent}"})


if __name__ == '__main__':
    app.run(debug=True)
