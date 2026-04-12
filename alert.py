from twilio.rest import Client

# 🔐 Your Twilio Credentials
account_sid = "ACad2552895e7325a242efa246baa3df81"
auth_token = "30648a924e872a528782a1a00512b7cb"

# 📱 Numbers
twilio_number = "+16626232353"      # Your Twilio number
your_number = "+918939097840"     # Your number

client = Client(account_sid, auth_token)

# ⚡ Sensor Values (Example)
input_current = float(input("Enter Input Current: "))
output_current = float(input("Enter Output Current: "))
temperature = float(input("Enter Temperature: "))

# 🚨 Conditions
alert_message = ""

if input_current > output_current:
    alert_message += "⚠️ Theft Detected!\n"

if input_current > 10:
    alert_message += "⚠️ Overload Detected!\n"

if temperature > 50:
    alert_message += "⚠️ High Temperature!\n"

# 📤 Send SMS if any issue
if alert_message != "":
    message = client.messages.create(
        body=alert_message,
        from_=twilio_number,
        to=your_number
    )
    print("SMS Sent! SID:", message.sid)
else:
    print("✅ System Normal")