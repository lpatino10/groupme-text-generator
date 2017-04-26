from Tokenizer import tokenize
import math

class Vocab:

    def generate_vocab(self, corpus):
        bigram_dict = {}

        with open(corpus, 'r') as file:
            for line in file:
                token_list = tokenize(line)

                # add trigrams to dictionary
                for i in range(0, len(token_list) - 2):
                    trigram = tuple(token_list[i:i+3])
                    if trigram in self.trigram_dict:
                        self.trigram_dict[trigram] += 1
                    else:
                        self.trigram_dict[trigram] = 1
                    
                # add bigrams as well
                for i in range(0, len(token_list) - 1):
                    bigram = tuple(token_list[i:i+2])
                    if bigram in bigram_dict:
                        bigram_dict[bigram] += 1
                    else:
                        bigram_dict[bigram] = 1          

        # finally, divide through trigram_dict by corresponding bigram_dict counts to get log probabilities
        for trigram, trigram_count in self.trigram_dict.items():
            bigram_count = bigram_dict[trigram[:-1]]
            self.trigram_dict[trigram] = math.log(trigram_count / bigram_count)
            print('Trigram: {}   Log prob: {}'.format(trigram, self.trigram_dict[trigram]))

    #def load_vocab_file(self, vocab_file):

    def __init__(self, corpus=None, vocab_file=None):
        self.trigram_dict = {}
        if vocab_file:
            self.load_vocab_file(vocab_file)
        else:
            self.generate_vocab(corpus)