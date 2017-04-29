from TextGenerator.TextGeneration import Vocab
import sys
import random
import re

def get_message_string(message):
    message_str = ''
    for token in message:
        if token != '{' and token != '}':
            if not re.match('[?.!,]', token):
                message_str += ' '
            message_str += token
    return message_str

def get_next_trigram(vocab, current_trigram):
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

def generate_random_message(vocab):
    # picks random starting point
    starting_trigram = random.choice(vocab.starting_trigrams)
    current_trigram = starting_trigram
    generated_message = list(current_trigram)

    while not current_trigram.__contains__('}'):
        current_trigram = get_next_trigram(vocab, current_trigram)
        generated_message.append(current_trigram[-1])

        if len(generated_message) > 30:
            break

    message = get_message_string(generated_message)
    return message

if __name__ == "__main__":
    input_file = sys.argv[1]
    vocab = Vocab()

    #vocab.generate_vocab_from_corpus(input_file)
    vocab.load_vocab_file(input_file)

    generate_random_message(vocab)