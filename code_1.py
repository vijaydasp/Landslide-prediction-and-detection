from flask import *
import main_1
import time
import threading
import telepot
import random

hum = 0
tem = 0
rain = 0
moi = 0
water_level = 0
vib = 0

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0

val = 0

chat_id = 680088529
bot = telepot.Bot('6101434410:AAFCeiMJP2kwJ-6QPE-Dsaw7Rxrzm9u9mMM')
bot.sendMessage(chat_id, "Welcome")

app = Flask(__name__)

@app.route('/test', methods=['get', 'post'])
def test():
    global hum, tem, rain, moi, water_level, vib
    global flag1, flag2, flag3, flag4, flag5
    global val
    val = request.get_data().decode('utf-8')
    print(val)
    val = val.split(",")
    hum = float(val[0])
    tem = float(val[1])
    rain = float(val[2])
    moi = float(val[3])
    water_level = float(val[4])
    vib = float(val[5])

    # Alert handling for different conditions
    if tem >= 30 and flag1 == 0:
        flag1 = 1
        bot.sendMessage(chat_id, 'Temperature is high')
    elif tem < 30 and flag1 == 1:
        flag1 = 0
    if tem <= 19 and flag2 == 0:
        flag2 = 1
        bot.sendMessage(chat_id, 'Temperature is low')
    elif tem > 19 and flag2 == 1:
        flag2 = 0
    if water_level <= 10 and flag3 == 0:
        flag3 = 1
        bot.sendMessage(chat_id, 'Water level is high')
    elif water_level > 10 and flag3 == 1:
        flag3 = 0
    if hum >= 95 and flag4 == 0:
        flag4 = 1
        bot.sendMessage(chat_id, 'Humidity is high')
    elif hum < 95 and flag4 == 1:
        flag4 = 0
    if hum <= 30 and flag5 == 0:
        flag5 = 1
        bot.sendMessage(chat_id, 'Humidity is low')
    elif hum > 30 and flag5 == 1:
        flag5 = 0
    return "ok"

# Handle Telegram bot commands
def handle(msg):
    global chat_id
    chat_id = msg['chat']['id']
    command = msg['text']
    print(f"Received command: {command}")
    
    if command == 'Roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
    elif command == 'Hi':
        bot.sendMessage(chat_id, 'Hi User')
    else:
        bot.sendMessage(chat_id, "Try something else")

# Detect landslide and send alerts
def detect():
    global tem, hum, rain, moi
    print("Detecting...")
    prediction = main_1.load_data(tem, hum, rain, moi)
    print(prediction)
    if prediction == 'Landslide':
        bot.sendMessage(chat_id, 'Landslide Predicted in http://maps.google.com/maps?q=11.26272695822931,75.7681779755359')

# Main function to start the server and detection
def main():
    global val
    threading.Thread(target=connect).start()
    bot.message_loop(handle)
    while True:
        if val:
            time.sleep(30)
            val=0
            detect()

# Flask server
def connect():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

