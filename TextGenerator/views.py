from django.shortcuts import render
from django.http import HttpResponse
from TextGenerator.TextGeneration import Vocab, Generator

def index(request):
    vocab = Vocab.Vocab()
    vocab.generate_vocab_from_corpus('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/logan.txt')
    message = Generator.generate_random_message(vocab)
    return render(request, 'TextGenerator/index.html', {'message': message})
