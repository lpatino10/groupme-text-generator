import re

class Tokenizer(object):
    def tokenize(self, message):
        # starter tokens
        token_list = ['{', '{']

        inner_tokens = self.get_inner_tokens(message)

        # adding message tokens and ending tokens
        token_list.extend(inner_tokens)
        token_list.extend(['}', '}'])

        return token_list

class WordTokenizer(Tokenizer):
    def get_inner_tokens(self, message):
        # picks out words of message, keeping certain punctuation (?, ., !, ',')
        # we then filter out None and empty string values that result from using the split function
        return [token for token in re.split("\s|([?.!,])", message.lower()) if token]

class CharacterTokenizer(Tokenizer):
    def get_inner_tokens(self, message):
        return [token for token in list(message.lower()) if token != '\n']