from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask(__name__)

# 🔐 Twilio Credentials
account_sid = "ACad2552895e7325a242efa246baa3df81"
auth_token = "684a0b1ef594b0f0c61f21967667ec6b"

twilio_number = "+16626232353"
your_number = "+918939097840"

client = Client(account_sid, auth_token)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check():
    input_current = float(request.form['input_current'])
    output_current = float(request.form['output_current'])
    temperature = float(request.form['temperature'])

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
