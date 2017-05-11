from TextGenerator.TextGeneration import Tokenizers
from TextGenerator.DataCollection.database_connector import get_db_reference

class Vocab(object):
    def __init__(self):
        self.n_gram_dict = {}
        self.starting_n_grams = []
        self.total_n_gram_count = 0

    def generate_vocab(self, person, n):
        lesser_gram_dict = {}

        # gets messages from single person or everyone
        db = get_db_reference()
        message_list = []
        if person == 'all':
            for person_key in db.get().each():
                message_list.extend(db.child(person_key.key()).get().each())
        else:
            message_list.extend(db.child(person).get().each())

        for message in message_list:
            token_list = self.tokenizer.tokenize(message.val())

            # 5 is an arbitrary choice for now, but this limit just encourages longer messages to train on
            if (len(token_list) > 5):

                # add n-grams to dictionary
                for i in range(0, len(token_list) - (n-1)):
                    n_gram = tuple(token_list[i:i+n])
                    if n_gram in self.n_gram_dict:
                        self.n_gram_dict[n_gram] += 1
                    else:
                        self.n_gram_dict[n_gram] = 1
                    self.total_n_gram_count += 1
            
                # we don't need to worry about getting (n-1)-grams in the unigram case
                if n == 1:
                    continue

                # add (n-1)-grams as well
                for i in range(0, len(token_list) - (n-2)):
                    lesser_gram = tuple(token_list[i:i+(n-1)])
                    if lesser_gram in lesser_gram_dict:
                        lesser_gram_dict[lesser_gram] += 1
                    else:
                        lesser_gram_dict[lesser_gram] = 1

        # finally, get n-gram probabilities
        for n_gram, n_gram_count in self.n_gram_dict.items():

            # in unigram case, we just divide unigram count by total count other than unigram
            if n == 1:
                self.n_gram_dict[n_gram] = (float(n_gram_count) / float(self.total_n_gram_count - n_gram_count))

            # otherwise, we divide n-gram count by (n-1)-gram count
            else:
                lesser_gram_count = lesser_gram_dict[n_gram[:-1]]
                self.n_gram_dict[n_gram] = (float(n_gram_count) / float(lesser_gram_count))

            # want to keep possible start points for generation later, unigram can start with whatever
            if n_gram[0] == '{' or n == 1:
                self.starting_n_grams.append(n_gram)

class WordVocab(Vocab):
    def __init__(self, person, n):
        super(WordVocab, self).__init__()
        self.tokenizer = Tokenizers.WordTokenizer(n)
        self.generate_vocab(person, n)

class CharacterVocab(Vocab):
    def __init__(self, person, n):
        super(CharacterVocab, self).__init__()
        self.tokenizer = Tokenizers.CharacterTokenizer(n)
        self.generate_vocab(person, n)