from Vocab import Vocab
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    vocab = Vocab()
    vocab.load_vocab_file(input_file)