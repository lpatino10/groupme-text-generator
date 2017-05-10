from TextGenerator.TextGeneration import Vocabs
import sys
import random
import re
import numpy as np

class Generator(object):
    def __init__(self, person):
        self.load_vocab(person)

    def get_next_trigram(self, vocab, current_trigram):
        # gets all trigrams where the first two tokens matching the current trigram's last two tokens
        possible_continuations = {trigram:prob for (trigram, prob) in vocab.trigram_dict.items() if current_trigram[1:] == trigram[:-1]}

        trigram_list = []
        prob_list = []
        for (trigram, prob) in possible_continuations.items():
            trigram_list.append(trigram)
            prob_list.append(prob)

        # renormalizing to make sure everything sums to 1
        normalized_probs = np.array(prob_list)
        normalized_probs /= normalized_probs.sum()

        # returns one at random, weighted with trigram probabilities
        index_choice = np.random.choice(len(trigram_list), p=normalized_probs)
        return trigram_list[index_choice]

    def generate_random_message(self):

        # picks random starting point
        starting_trigram = random.choice(self.vocab.starting_trigrams)
        current_trigram = starting_trigram
        generated_message = list(current_trigram)

        while '}' not in current_trigram:
            current_trigram = self.get_next_trigram(self.vocab, current_trigram)
            generated_message.append(current_trigram[-1])

            # arbitrary cutoff length that could be added as option on webpage
            if len(generated_message) > 150:
                break

        message = self.get_message_string(generated_message)
        return message

class WordGenerator(Generator):
    def get_message_string(self, message):
        message_str = ''
        for token in message:
            if token != '{' and token != '}':
                if not re.match('[?.!,]', token):
                    message_str += ' '
                message_str += token
        return message_str

    def load_vocab(self, person):
        self.vocab = Vocabs.WordVocab(person)

class CharacterGenerator(Generator):
    def get_message_string(self, message):
        message_str = ''
        for token in message:
            if token != '{' and token != '}':
                message_str += token
        return message_str

    def load_vocab(self, person):
        self.vocab = Vocabs.CharacterVocab(person)