import re

class Tokenizer(object):
    def __init__(self, n):
        self.starter_tokens = ['{'] * (n - 1)
        self.ending_tokens = ['}'] * (n - 1)

    def tokenize(self, message):
        token_list = []
        token_list.extend(self.starter_tokens)

        inner_tokens = self.get_inner_tokens(message)
        token_list.extend(inner_tokens)
        
        token_list.extend(self.ending_tokens)

        return token_list

class WordTokenizer(Tokenizer):
    def get_inner_tokens(self, message):
        # picks out words of message, keeping certain punctuation (?, ., !, ',')
        # we then filter out None and empty string values that result from using the split function
        return [token for token in re.split("\s|([?.!,])", message.lower()) if token]

class CharacterTokenizer(Tokenizer):
    def get_inner_tokens(self, message):
        return [token for token in list(message.lower()) if token != '\n']