from database_connector import get_db_reference
import requests
import pyrebase
import configparser

if __name__ == '__main__':
    config_parser = configparser.ConfigParser()
    config_parser.read('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/DataCollection/config.ini')

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

    base_url = 'https://api.groupme.com/v3'
    group_url = '/groups'
    group_id = '/17077713'
    messages_url = '/messages'
    parameters = {
        'token': config_parser.get('keys', 'GroupMeToken'),
        'limit': 100
    }
    full_message_url = base_url + group_url + group_id + messages_url

    db = get_db_reference()

    message_reponse = requests.get(full_message_url, params=parameters)

    # 304 tells us that we're out of messages
    while message_reponse.status_code != 304:
        message_reponse_json = message_reponse.json()
        message_list = message_reponse_json['response']['messages']

        # saving messages to db
        for message in message_list:
            user_id = message['user_id']
            if user_id in id_to_name_dict:
                name_key = id_to_name_dict[user_id]
                message_text = message['text']
                if message_text:
                    db.child(name_key).push(message_text)
        
        # getting last id and updating params to keep looking through history
        last_message_id = message_list[-1]['id']
        parameters['before_id'] = last_message_id
        message_reponse = requests.get(full_message_url, params=parameters)