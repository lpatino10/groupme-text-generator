from Tokenizer import tokenize
import math
import os.path 

class Vocab:

    def __init__(self):
        self.trigram_dict = {}
        self.starting_trigrams = []

    def save_trigrams_to_file(self, corpus):
        save_file = corpus[:-4] + '_trigrams.txt'
        with open(save_file, 'w') as file:
            for trigram, trigram_prob in self.trigram_dict.items():
                file.write('{} {} {}%~%{}\n'.format(trigram[0], trigram[1], trigram[2], trigram_prob))

    def generate_vocab_from_corpus(self, corpus):
        bigram_dict = {}

        with open(corpus, 'r') as file:
            for line in file:
                token_list = tokenize(line)

                # 5 is an arbitrary choice for now, but this limit just encourages longer messages to train on
                if (len(token_list) > 5):
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

            # want to keep possible start points for generation later
            if trigram[0] == '{':
                self.starting_trigrams.append(trigram)

        self.save_trigrams_to_file(corpus)

    def load_vocab_file(self, vocab_file):
        with open(vocab_file, 'r') as file:
            for line in file:
                trigram_and_prob = line.split('%~%')

                trigram_tokens = trigram_and_prob[0]
                trigram = tuple(trigram_tokens.split(' '))
                prob = float(trigram_and_prob[1][:-1])

                self.trigram_dict[trigram] = prob
                
                if trigram[0] == '{':
                    self.starting_trigrams.append(trigram)