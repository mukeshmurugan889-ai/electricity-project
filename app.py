from flask import Flask, render_template, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# 🔐 Twilio Credentials
account_sid = "ACad2552895e7325a242efa246baa3df81"
auth_token = "32c3ae54a3d42d10a087c4c46b435919"

twilio_number = "+16626232353"
your_number = "+918939097840"

client = Client(account_sid, auth_token)

# 📦 store latest ESP32 data
latest_data = {}

# =========================
# 🌐 HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template("index.html")


# =========================
# 📥 ESP32 SENDS DATA HERE
# =========================
@app.route('/send-data', methods=['POST'])
def send_data():
    global latest_data

    data = request.json
    latest_data = data

    input_current = float(data.get('input_current', 0))
    output_current = float(data.get('output_current', 0))
    temperature = float(data.get('temperature', 0))

    alert_message = ""

    if input_current > output_current:
        alert_message += "⚠️ Theft Detected!\n"

    if input_current > 10:
        alert_message += "⚠️ Overload Detected!\n"

    if temperature > 50:
        alert_message += "⚠️ High Temperature!\n"

    if alert_message != "":
        message = client.messages.create(
            body=alert_message,
            from_=twilio_number,
            to=your_number
        )
        print("SMS Sent:", message.sid)

    return jsonify({"status": "received"})


# =========================
# 📤 ESP32 / WEBSITE READS DATA
# =========================
@app.route('/get-data', methods=['GET'])
def get_data():
    global latest_data

    if not latest_data:
        return jsonify({
            "input_current": 0,
            "output_current": 0,
            "temperature": 0
        })

    return jsonify(latest_data)
# =========================
# 🖥️ MANUAL WEBSITE INPUT (your old system)
# =========================
@app.route('/check', methods=['POST'])
def check():
    global latest_data

    input_current = float(request.form['input_current'])
    output_current = float(request.form['output_current'])
    temperature = float(request.form['temperature'])

    # 🔥 STORE DATA FOR ESP32
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
        message = client.messages.create(
            body=alert_message,
            from_=twilio_number,
            to=your_number
        )
        return f"SMS Sent! SID: {message.sid}"

    return "✅ System Normal"

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
