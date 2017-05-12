from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from TextGenerator.TextGeneration import Generators
from TextGenerator.DataCollection.database_connector import update_db
import json
import requests

@csrf_exempt
def index(request):

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        post_json = json.loads(body_unicode)

        # this is the bot sending a new message to the website
        # we need to update the db
        if 'sender_type' in post_json:
            if post_json['sender_type'] == 'user':
                update_db(post_json)

        # this is someone actually using the app
        else:
            person = post_json['person'].lower()
            token_type = post_json['tokenType'].lower()
            n = post_json['nGram']

            generator = None
            if token_type == 'word':
                generator = Generators.WordGenerator(person, n)
            else:
                generator = Generators.CharacterGenerator(person, n)

            message = generator.generate_random_message()
            data = {
                'message': message
            }

            return JsonResponse(data)

    return render(request, 'TextGenerator/index.html')