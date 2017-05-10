from TextGenerator.TextGeneration import Tokenizers
from TextGenerator.DataCollection.database_connector import get_db_reference

class Vocab(object):
    def __init__(self):
        self.trigram_dict = {}
        self.starting_trigrams = []

    def generate_vocab(self, person):
        bigram_dict = {}

        db = get_db_reference()
        message_list = db.child(person).get()

        for message in message_list.each():
            token_list = self.tokenizer.tokenize(message.val())

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

        # finally, divide through trigram_dict by corresponding bigram_dict counts to get probabilities
        for trigram, trigram_count in self.trigram_dict.items():
            bigram_count = bigram_dict[trigram[:-1]]
            self.trigram_dict[trigram] = (float(trigram_count) / float(bigram_count))

            # want to keep possible start points for generation later
            if trigram[0] == '{':
                self.starting_trigrams.append(trigram)

class WordVocab(Vocab):
    def __init__(self, person):
        super(WordVocab, self).__init__()
        self.tokenizer = Tokenizers.WordTokenizer()
        self.generate_vocab(person)

class CharacterVocab(Vocab):
    def __init__(self, person):
        super(CharacterVocab, self).__init__()
        self.tokenizer = Tokenizers.CharacterTokenizer()
        self.generate_vocab(person)