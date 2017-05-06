import requests
import configparser

config_parser = configparser.ConfigParser()
config_parser.read('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/DataCollection')

id_to_filepath_dict = {
    '10957649': '../Data/brian.txt',
    '31986368': '../Data/nick.txt',
    '31986367': '../Data/craig.txt',
    '24472030': '../Data/logan.txt',
    '27984896': '../Data/mccoy.txt',
    '21438899': '../Data/zach.txt',
    '31986369': '../Data/niel.txt'
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

message_reponse = requests.get(full_message_url, params=parameters)

# 304 tells us that we're out of messages
while message_reponse.status_code != 304:
    message_reponse_json = message_reponse.json()
    message_list = message_reponse_json['response']['messages']

    # writing messages to appropriate files
    for message in message_list:
        user_id = message['user_id']
        if user_id in id_to_filepath_dict:
            file_path = id_to_filepath_dict[user_id]
            with open(file_path, 'a') as user_file:
                message_text = message['text']
                if message_text:
                    user_file.write(message_text + '\n')
    
    # getting last id and updating params to keep looking through history
    last_message_id = message_list[-1]['id']
    parameters['before_id'] = last_message_id
    message_reponse = requests.get(full_message_url, params=parameters)