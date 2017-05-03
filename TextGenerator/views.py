from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from TextGenerator.TextGeneration import Vocab, Generator
import json
import requests

@csrf_exempt
def index(request):

    #del request.session['generator']

    # initializes all trigram dicts
    if 'generator' not in request.session:
        generator = Generator.Generator()
        request.session['generator'] = generator

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        post_json = json.loads(body_unicode)

        person = post_json['person'].lower()
        token_type = post_json['tokenType']

        message = request.session['generator'].generate_random_message(person)
        data = {
            'message': message
        }

        return JsonResponse(data)

    return render(request, 'TextGenerator/index.html')