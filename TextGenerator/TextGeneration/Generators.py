from TextGenerator.TextGeneration import Vocabs
import sys
import random
import re
import numpy as np

class Generator(object):
    def __init__(self, person, n):
        # just in case the message generator gets into a loop
        self.max_message_size = 150
        if n == 1:
            # the unigram has no ending token, so we just set a random message size for it to stop
            self.max_message_size = random.randint(3, self.max_message_size)
        self.load_vocab(person, n)

    def get_next_n_gram(self, vocab, current_n_gram):
        # gets all n-grams where the first n-1 tokens matching the current n-gram's last n-1 tokens
        possible_continuations = {n_gram:prob for (n_gram, prob) in vocab.n_gram_dict.items() if current_n_gram[1:] == n_gram[:-1]}

        n_gram_list = []
        prob_list = []
        for (n_gram, prob) in possible_continuations.items():
            n_gram_list.append(n_gram)
            prob_list.append(prob)

        # renormalizing to make sure everything sums to 1
        normalized_probs = np.array(prob_list)
        normalized_probs /= normalized_probs.sum()

        # returns one at random, weighted with trigram probabilities
        index_choice = np.random.choice(len(n_gram_list), p=normalized_probs)
        return n_gram_list[index_choice]

    def generate_random_message(self):

        # picks random starting point
        starting_n_gram = random.choice(self.vocab.starting_n_grams)
        current_n_gram = starting_n_gram
        generated_message = list(current_n_gram)

        while '}' not in current_n_gram and len(generated_message) < self.max_message_size:
            current_n_gram = self.get_next_n_gram(self.vocab, current_n_gram)
            generated_message.append(current_n_gram[-1])

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

    def load_vocab(self, person, n):
        self.vocab = Vocabs.WordVocab(person, n)

class CharacterGenerator(Generator):
    def get_message_string(self, message):
        message_str = ''
        for token in message:
            if token != '{' and token != '}':
                message_str += token
        return message_str

    def load_vocab(self, person, n):
        self.vocab = Vocabs.CharacterVocab(person, n)