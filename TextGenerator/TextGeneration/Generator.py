from TextGenerator.TextGeneration import Vocab
import sys
import random
import re

class Generator:

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
        else:
            vocab = self.niel_vocab
        return vocab

    def get_message_string(self, message):
        message_str = ''
        for token in message:
            if token != '{' and token != '}':
                if not re.match('[?.!,]', token):
                    message_str += ' '
                message_str += token
        return message_str

    def get_next_trigram(self, vocab, current_trigram):
        # gets all trigrams where the first two tokens matching the current trigram's last two tokens
        possible_continuations = {trigram:prob for (trigram, prob) in vocab.trigram_dict.items() if current_trigram[1:] == trigram[:-1]}

        # finds max probability in above dict
        max_prob = max(possible_continuations.values())

        # picks out all trigrams with highest prob
        next_list = []
        for (trigram, prob) in possible_continuations.items():
            if prob == max_prob:
                next_list.append(trigram)

        # returns one at random
        return random.choice(next_list)

    def generate_random_message(self, name):
        vocab = self.choose_vocab(name)

        # picks random starting point
        starting_trigram = random.choice(vocab.starting_trigrams)
        current_trigram = starting_trigram
        generated_message = list(current_trigram)

        while not current_trigram.__contains__('}'):
            current_trigram = self.get_next_trigram(vocab, current_trigram)
            generated_message.append(current_trigram[-1])

            if len(generated_message) > 100:
                break

        message = self.get_message_string(generated_message)
        return message

    def __init__(self):
        self.logan_vocab = Vocab.Vocab()
        self.mccoy_vocab = Vocab.Vocab()
        self.nick_vocab = Vocab.Vocab()
        self.brian_vocab = Vocab.Vocab()
        self.zach_vocab = Vocab.Vocab()
        self.craig_vocab = Vocab.Vocab()
        self.niel_vocab = Vocab.Vocab()

        self.logan_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/logan_trigrams.txt')
        self.mccoy_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/mccoy_trigrams.txt')
        self.nick_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/nick_trigrams.txt')
        self.brian_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/brian_trigrams.txt')
        self.zach_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/zach_trigrams.txt')
        self.craig_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/craig_trigrams.txt')
        self.niel_vocab.load_vocab_file('/Users/loganpatino/RandomProjects/GroupMeTextGenerator/TextGenerator/Data/niel_trigrams.txt')