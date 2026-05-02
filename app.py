from flask import Flask, render_template, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# 🔐 Twilio Credentials (PUT NEW TOKEN)
account_sid = "ACad2552895e7325a242efa246baa3df81"
auth_token = "32c3ae54a3d42d10a087c4c46b435919"

twilio_number = "+16626232353"
your_number = "+918939097840"

client = Client(account_sid, auth_token)

# 📦 Store latest data
latest_data = {
    "input_current": 0,
    "output_current": 0,
    "temperature": 0
}

# =========================
# 🌐 HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template("index.html")


# =========================
# 📥 ESP32 SENDS DATA
# =========================
@app.route('/send-data', methods=['POST'])
def send_data():
    global latest_data

    data = request.json or {}

    input_current = float(data.get('input_current', 0))
    output_current = float(data.get('output_current', 0))
    temperature = float(data.get('temperature', 0))

    latest_data = {
        "input_current": input_current,
        "output_current": output_current,
        "temperature": temperature
    }

    alert_message = ""

    if input_current > output_current:
        alert_message += "⚠️ Theft Detected!\n"

    if input_current > 10:
        alert_message += "⚠️ Overload Detected!\n"

    if temperature > 50:
        alert_message += "⚠️ High Temperature!\n"

    if alert_message != "":
        try:
            message = client.messages.create(
                body=alert_message,
                from_=twilio_number,
                to=your_number
            )
            print("SMS Sent:", message.sid)
        except Exception as e:
            print("Twilio Error:", e)

    return jsonify({"status": "received"})


# =========================
# 📤 GET DATA
# =========================
@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(latest_data)


# =========================
# 🖥️ WEBSITE INPUT
# =========================
@app.route('/check', methods=['POST'])
def check():
    global latest_data

    input_current = float(request.form['input_current'])
    output_current = float(request.form['output_current'])
    temperature = float(request.form['temperature'])

    latest_data = {
        "input_current": input_current,
        "output_current": output_current,
        "temperature": temperature
    }

    alert_message = ""

    if input_current > output_current:
        alert_message += "⚠️ Theft Detected!\n"

    if input_current > 10:
        alert_message += "⚠️ Overload Detected!\n"

    if temperature > 50:
        alert_message += "⚠️ High Temperature!\n"

    if alert_message != "":
        try:
            message = client.messages.create(
                body=alert_message,
                from_=twilio_number,
                to=your_number
            )
            print("SMS Sent:", message.sid)
            return "SMS Sent!"
        except Exception as e:
            return str(e)   # 🔥 THIS LINE SHOWS REAL ERROR

    return "✅ System Normal"


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
