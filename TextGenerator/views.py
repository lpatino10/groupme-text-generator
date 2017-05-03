from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from TextGenerator.TextGeneration import Generators
import json
import requests

@csrf_exempt
def index(request):

    #del request.session['word_generator']
    #del request.session['character_generator']

    # initializes all trigram dicts
    if ('word_generator' not in request.session) or ('character_generator' not in request.session): 
        word_generator = Generators.WordGenerator()
        character_generator = Generators.CharacterGenerator()
        request.session['word_generator'] = word_generator
        request.session['character_generator'] = character_generator

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        post_json = json.loads(body_unicode)

        person = post_json['person'].lower()
        token_type = post_json['tokenType'].lower()

        message = None
        if token_type == 'word':
            message = request.session['word_generator'].generate_random_message(person)
        else:
            message = request.session['character_generator'].generate_random_message(person)

        data = {
            'message': message
        }

        return JsonResponse(data)

    return render(request, 'TextGenerator/index.html')