from TextGenerator.TextGeneration import Vocabs
import sys
import random
import re
import numpy as np

class Generator(object):
    def __init__(self):
        self.load_vocabs()

    def choose_vocab(self, name):
        vocab = None
        if name == 'logan':
            vocab = self.logan_vocab
        elif name == 'mccoy':
            vocab = self.mccoy_vocab
        elif name == 'nick':
            vocab = self.nick_vocab
        elif name == 'brian':
            vocab = self.brian_vocab
        elif name == 'zach':
            vocab = self.zach_vocab
        elif name == 'craig':
            vocab = self.craig_vocab
        elif name == 'niel':
            vocab = self.niel_vocab
        else:
            vocab = self.all_vocab
        return vocab

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

    def generate_random_message(self, name):
        vocab = self.choose_vocab(name)

        # picks random starting point
        starting_trigram = random.choice(vocab.starting_trigrams)
        current_trigram = starting_trigram
        generated_message = list(current_trigram)

        while '}' not in current_trigram:
            current_trigram = self.get_next_trigram(vocab, current_trigram)
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

    def load_vocabs(self):
        self.all_vocab = Vocabs.WordVocab()
        self.logan_vocab = Vocabs.WordVocab()
        self.mccoy_vocab = Vocabs.WordVocab()
        self.nick_vocab = Vocabs.WordVocab()
        self.brian_vocab = Vocabs.WordVocab()
        self.zach_vocab = Vocabs.WordVocab()
        self.craig_vocab = Vocabs.WordVocab()
        self.niel_vocab = Vocabs.WordVocab()

        self.all_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/all_word_trigrams.txt')
        self.logan_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/logan_word_trigrams.txt')
        self.mccoy_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/mccoy_word_trigrams.txt')
        self.nick_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/nick_word_trigrams.txt')
        self.brian_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/brian_word_trigrams.txt')
        self.zach_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/zach_word_trigrams.txt')
        self.craig_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/craig_word_trigrams.txt')
        self.niel_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/niel_word_trigrams.txt')

class CharacterGenerator(Generator):
    def get_message_string(self, message):
        message_str = ''
        for token in message:
            if token != '{' and token != '}':
                message_str += token
        return message_str

    def load_vocabs(self):
        self.all_vocab = Vocabs.CharacterVocab()
        self.logan_vocab = Vocabs.CharacterVocab()
        self.mccoy_vocab = Vocabs.CharacterVocab()
        self.nick_vocab = Vocabs.CharacterVocab()
        self.brian_vocab = Vocabs.CharacterVocab()
        self.zach_vocab = Vocabs.CharacterVocab()
        self.craig_vocab = Vocabs.CharacterVocab()
        self.niel_vocab = Vocabs.CharacterVocab()

        self.all_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/all_character_trigrams.txt')
        self.logan_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/logan_character_trigrams.txt')
        self.mccoy_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/mccoy_character_trigrams.txt')
        self.nick_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/nick_character_trigrams.txt')
        self.brian_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/brian_character_trigrams.txt')
        self.zach_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/zach_character_trigrams.txt')
        self.craig_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/craig_character_trigrams.txt')
        self.niel_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/niel_character_trigrams.txt')