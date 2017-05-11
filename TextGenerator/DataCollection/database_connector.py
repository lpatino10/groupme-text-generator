import os
import pyrebase
import configparser

id_to_name_dict = {
    '10957649': 'brian',
    '31986368': 'nick',
    '31986367': 'craig',
    '24472030': 'logan',
    '27984896': 'mccoy',
    '39641269': 'mccoy',
    '21438899': 'zach',
    '31986369': 'niel'
}

# configparser code is for local testing only
config_parser = configparser.ConfigParser()
config_parser.read('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/DataCollection/config.ini')

db_config = {
    #'apiKey': os.environ['FIREBASE_KEY'],
    'apiKey': config_parser.get('keys', 'FirebaseKey'),
    'authDomain': 'groupme-text-generator.firebaseapp.com',
    'databaseURL': 'https://groupme-text-generator.firebaseio.com/',
    'storageBucket': 'groupme-text-generator.appspot.com'
}
firebase = pyrebase.initialize_app(db_config)
db = firebase.database()

def get_db_reference():
    return db

def update_db(message_json):
    user_id = message_json['user_id']
    if user_id in id_to_name_dict:
        name_key = id_to_name_dict[user_id]
        message_text = message_json['text']
        if message_text:
            db_ref = get_db_reference()
            db_ref.child(name_key).push(message_text)