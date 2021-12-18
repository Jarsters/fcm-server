from flask import Flask, request as req, render_template

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import json
import datetime

cred = credentials.Certificate("badmintvent-firebase-adminsdk-1gwc0-02bbe75362.json")
app = firebase_admin.initialize_app(cred)
contoh_topic = "badminton"
contoh_token = 'eK6PIHsfS9KQaaIM6KZmIX:APA91bGtMxq4yOphQuIBWulZoy0F7ISeNIOOASmqMEHe0STSWOSheeMTNfgq39SeAYH9kjIoB0unXZcJ5Rd5myDq4uz6srMdnQmB6fx9xlgcgldnrUXHF6NpVaYuP9CEqA-oVkiskl5t'

appf = Flask(__name__)

@appf.route('/')
def index():
    return render_template('index.html')

@appf.route('/privacy')
def private():
    return render_template('privacy.html')

@appf.route('/subs-topic', methods=['POST'])
def subscribe_topic_by_token():
    data_json = req.get_json(force=True)
    print(data_json)
    token = data_json['token'] if data_json['token'] else contoh_token
    topic = data_json['topic'] if data_json['topic'] else contoh_topic
    print(token, topic)
    resp = messaging.subscribe_to_topic(token, topic)
    print(resp.success_count)

    return {"Response": resp.success_count, "Status":"Success!"}

@appf.route('/unsubs-topic', methods=['POST'])
def unsubscribe_topic_by_token():
    data_json = req.get_json(force=True)
    token = data_json['token'] if data_json['token'] else contoh_token
    topic = data_json['topic'] if data_json['topic'] else contoh_topic
    resp = messaging.unsubscribe_from_topic(token, topic)
    print(resp.success_count)

    return {"Response": resp.success_count, "Status":"Success!"}

@appf.route("/send-message-token", methods=['POST'])
def send_message_token():
    data_json = req.get_json(force=True)
    token = data_json['token'] if data_json['token'] else contoh_token
    message = data_json['message']
    title = data_json['title']
    nama = data_json['nama']
    data = {
        "title":title,
        "message":message,
        "nama":nama
    }

    # apns
    alert = messaging.ApsAlert(title = title, body = message)
    aps = messaging.Aps(alert = alert, sound = "default")
    payload = messaging.APNSPayload(aps)


    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        data=data,
        token=token,
        apns = messaging.APNSConfig(payload = payload)
    )
    resp = messaging.send(message)
    print(data)
    print(resp)
    return {"Response": resp, 'Data':data, 'Status':"Success"}

@appf.route("/send-message-topic", methods=['POST'])
def send_message_topic():
    data_json = req.get_json(force=True)
    topic = data_json.get('topic') if data_json.get('topic') else contoh_topic
    message = data_json['message']
    title = data_json['title']
    nama = data_json['nama']
    data = {
        "title":title,
        "message":message,
        "nama":nama,
        "topic":topic
    }

    message = messaging.Message( 
        notification = messaging.Notification( title=title, body=message ), 
        data=data, 
        topic=topic,
        android=messaging.AndroidConfig( priority='max', notification=messaging.AndroidNotification( sound='default' ), ), 
        apns=messaging.APNSConfig( payload=messaging.APNSPayload( aps=messaging.Aps( alert = messaging.ApsAlert(title = title, body = message), sound='default' ), ), ), 
        )

    resp = messaging.send(message)
    print(resp)
    return {"Response": resp, 'Data':data, 'Status':"Success"}