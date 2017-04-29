import re

def tokenize(message):
        # starter tokens
        token_list = ['{', '{']

        # picks out words of message, keeping certain punctuation (?, ., !, ',')
        # we then filter out None and empty string values that result from using the split function
        inner_tokens = [token for token in re.split("\s|([?.!,])", message.lower()) if token]

        # adding message tokens and ending tokens
        token_list.extend(inner_tokens)
        token_list.extend(['}', '}'])

        return token_list